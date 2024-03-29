from threading import Thread
from datetime import datetime
from datetime import datetime

import os
import cv2
import pygame
import atexit

import numpy as np

from controller import DroneController, \
    log, replace_at_index, snap_axis, turn_to_tertiary

from modeler import Model

pygame.init()
pygame.joystick.init()

# to visualize data, run python tests/data-visualizer.py

if pygame.joystick.get_count() == 0:
    log("no joysticks found, stopping...", "error")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

drone_controller = DroneController(joystick, verbose=True, mock=False)
drone_controller.connect()
drone_controller.set_speed(25)

model = Model("models/LIMVA80_10-9-23", True)

who = input("who's using this session?")
session_id = f"{who}--{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

clock = pygame.time.Clock()
alive = True
recording = False
self_driving = False

latest_predictions = "0_0_0_0_1"

action_map = {
    "buttons": {
        2: [8, "1"],
        0: [8, "0"],

        8: [2, "1"],
        7: [2, "2"],
    },
    "joysticks": {
        0: [round, "pos", 4],
        1: [round, "neg", 0],
        2: [round, "pos", 6]
    }
}


def process_button(event):
    global recording, self_driving

    if event.button == 9:
        recording = True
        log("started recording!", "success")
        # Thread(target=joystick.rumble, args=(3000, 3000, 1)).start()

        return True
    elif event.button == 10:
        recording = False
        log("stopped recording!", "success")

        return True
    elif event.button == 4:
        recording = False
        self_driving = not self_driving

        if self_driving:
            log("STARTED SELF DRIVING", "warning")
        else:
            log("STOPPED SELF DRIVING", "warning")

        return True

    return False


def camera_loop():
    global drone_controller, recording, session_id, self_driving, model, latest_predictions

    drone_controller.stream_on()
    tello_video = cv2.VideoCapture(
        "udp://@0.0.0.0:11111?overrun_nonfatal=1&fifo_size=50000000")

    frame_num = 0
    amount_of_data = 0

    os.makedirs(f"data/{session_id}", exist_ok=True)

    while True:
        if (not drone_controller.is_flying or
                (not recording and not self_driving)):
            continue

        returned, frame = tello_video.read()
        frame_num += 1

        # print(returned, frame_num % 10, drone_controller.current_state ==
        #       "0_0_0_0_1", drone_controller.is_flying)

        if (returned
            and frame_num % 10 == 0
            and ((not drone_controller.current_state == "0_0_0_0_1") or self_driving)
                and drone_controller.is_flying):

            height, width, layers = frame.shape

            resize = cv2.resize(frame, (256, 144))

            if self_driving:
                image_array = np.asarray(resize)
                latest_predictions = model.infer(image_array)
            else:
                current_time = datetime.now().strftime("%H-%M-%S")
                final_name = f"data/{session_id}/{amount_of_data}_{current_time}_{drone_controller.current_state}.png"

                if not cv2.imwrite(final_name, resize):
                    log(f"failed to save picture @ {final_name}", "error")
                else:
                    amount_of_data += 1

                    if drone_controller.verbose:
                        log(f"{amount_of_data} | saved image @ {final_name}", "normal")
        # except cv2.error as e:
        #     log(f"decoding error: {str(e)}", "error")
        #     continue

        # except Exception as ex:
        #     log(f"an error occurred: {str(ex)}", "error")
        #     continue


def exit_handler():
    global self_driving, recording, alive

    self_driving = False
    recording = False
    alive = False

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

            new_state = new_state[:place_to_change] + \
                new_value + new_state[place_to_change + 1:]
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 8 or event.button == 7:
                place_to_change = mapped_value[0]
                new_value = "0"

                new_state = new_state[:2] + \
                    new_value + new_state[2 + 1:]

        elif event.type == pygame.JOYAXISMOTION:
            mapped_value = action_map["joysticks"].get(event.axis)

            if not mapped_value:
                continue

            function_to_run = mapped_value[0]
            sign = mapped_value[1]
            place_to_change = mapped_value[2]

            new_value = function_to_run(
                event.value) if sign == "pos" else -function_to_run(event.value)
            new_value = turn_to_tertiary(new_value)
            # print(f"changing place {place_to_change} to {new_value}")

            new_state = replace_at_index(
                new_state, place_to_change, str(new_value))

    if self_driving and latest_predictions != drone_controller.current_state:
        drone_controller.move_state(latest_predictions)
    elif new_state != drone_controller.current_state and not self_driving:
        drone_controller.move_state(new_state)
