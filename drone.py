from threading import Thread
from datetime import datetime
from datetime import datetime

import os
import cv2
import pygame
import atexit

from controller import DroneController, \
    log, replace_at_index, snap_axis, turn_to_tertiary

from modeler import Model

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    log("no joysticks found, stopping...", "error")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

drone_controller = DroneController(joystick, verbose=True, mock=False)
drone_controller.connect()
drone_controller.set_speed(40)

model = Model("models/VERSION_HERE", verbose=True)

who = input("who's recording this session?")
session_id = f"{who}__{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

clock = pygame.time.Clock()
alive = True
recording = False
self_driving = False

action_map = {
    "buttons": {
        2: [8, "1"],
        1: [8, "0"],
    },
    "joysticks": {
        5: [snap_axis, "pos", 2],
        4: [snap_axis, "neg", 2],

        0: [round, "pos", 4],
        1: [round, "neg", 0],
        2: [round, "pos", 6]
    }
}

def process_button(event):
    global recording

    if event.button == 6:
        recording = True
        log("started recording!", "success")
        Thread(target=joystick.rumble, args=(3000, 3000, 1)).start()

        return True
    elif event.button == 4:
        recording = False
        log("stopped recording!", "success")

        return True
    # elif event.button == 15:
    #     recording = False
    #     self_driving = True

    #     log("STARTED SELF DRIVING", "warning")

    #     return True

    return False

def camera_loop():
    global drone_controller, recording, session_id

    drone_controller.stream_on()
    tello_video = cv2.VideoCapture("udp://@0.0.0.0:11111")

    frame_num = 0
    amount_of_data = 0

    os.makedirs(f"data/{session_id}", exist_ok=True)

    while True:
        if not drone_controller.is_flying or not recording: 
            continue
        
        returned, frame = tello_video.read()
        frame_num += 1

        if (returned
                and frame_num % 10 == 0
                and not drone_controller.current_state == "0_0_0_0_1"
                and drone_controller.is_flying):

            height, width, layers = frame.shape

            new_height = int(height / 2)
            new_width = int(width / 2)

            resize = cv2.resize(frame, (new_width, new_height))
            current_time = datetime.now().strftime("%H-%M-%S")

            final_name = f"data/{session_id}/{amount_of_data}_{current_time}_{drone_controller.current_state}.png"

            if not cv2.imwrite(final_name, resize):
                log(f"failed to save picture @ {final_name}", "error")
            else:
                amount_of_data += 1

                if drone_controller.verbose:
                    log(f"{amount_of_data} | saved image @ {final_name}", "normal")

def exit_handler():
    if drone_controller.is_flying:
        drone_controller.land()
    
    if drone_controller.streaming:
        drone_controller.stream_off()

Thread(target=camera_loop).start()
atexit.register(exit_handler)

while alive:
    clock.tick(60)

    new_state = drone_controller.current_state

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if process_button(event):
                continue
            
            mapped_value = action_map["buttons"].get(event.button)
            
            if not mapped_value:
                continue

            place_to_change = mapped_value[0]
            new_value = mapped_value[1]

            new_state = new_state[:place_to_change] + new_value + new_state[place_to_change + 1:]
        elif event.type == pygame.JOYAXISMOTION:
            mapped_value = action_map["joysticks"].get(event.axis)

            if not mapped_value:
                continue
            
            function_to_run = mapped_value[0]
            sign = mapped_value[1]
            place_to_change = mapped_value[2]

            new_value = function_to_run(event.value) if sign == "pos" else -function_to_run(event.value)
            new_value = turn_to_tertiary(new_value)
            # print(f"changing place {place_to_change} to {new_value}")

            new_state = replace_at_index(new_state, place_to_change, str(new_value))
    
    if new_state != drone_controller.current_state:
        drone_controller.move_state(new_state)
