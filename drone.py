import pygame
import time
import cv2
import os

from threading import Thread
from controller import DroneController, \
    log, replace_at_index, snap_axis, turn_to_tertiary

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    log("no joysticks found, stopping...", "error")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

drone_controller = DroneController(joystick, verbose=True, mock=True)
drone_controller.connect()
drone_controller.set_speed(40)

clock = pygame.time.Clock()
alive = True
recording = False

action_map = {
    "buttons": {
        2: [8, "1"],
        1: [8, "0"],
    },
    "joysticks": {
        5: [snap_axis, "pos", 2],
        4: [snap_axis, "neg", 2],

        0: [round, "pos", 0],
        1: [round, "neg", 4],
        2: [round, "pos", 6]
    }
}

def camera_loop():
    global drone_controller, recording

    tello_video = cv2.VideoCapture("udp://@0.0.0.0:11111")
    drone_controller.streamon()

    while recording and drone_controller.is_flying:
        returned, frame = tello_video.read()

        if returned:
            cv2.imshow("tello feed", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    
    tello_video.release()
    drone_controller.streamoff()

while alive:
    clock.tick(60)

    new_state = drone_controller.current_state

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 15:
                recording = not recording

                if recording:
                    log("started recording!", "success")
                    Thread(target=camera_loop).start()
                else:
                    log("stopped recording!", "success")
                
                continue

            mapped_value = action_map["buttons"].get(event.button)
            
            if not mapped_value: continue

            place_to_change = mapped_value[0]
            new_value = mapped_value[1]

            new_state = new_state[:place_to_change] + new_value + new_state[place_to_change + 1:]
        elif event.type == pygame.JOYAXISMOTION:
            mapped_value = action_map["joysticks"].get(event.axis)

            if not mapped_value: continue
            
            function_to_run = mapped_value[0]
            sign = mapped_value[1]
            place_to_change = mapped_value[2]

            new_value = function_to_run(event.value) if sign == "pos" else -function_to_run(event.value)
            new_value = turn_to_tertiary(new_value)
            new_state = replace_at_index(new_state, place_to_change, str(new_value))
    
    if new_state != drone_controller.current_state:
        drone_controller.move_state(new_state)