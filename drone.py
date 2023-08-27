from threading import Thread
from datetime import datetime

import pygame

from controller import DroneController, \
    log, replace_at_index, snap_axis, turn_to_tertiary, camera_loop

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

session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

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

Thread(target=camera_loop, args=(drone_controller, recording, session_id)).start()


while alive:
    clock.tick(60)

    new_state = drone_controller.current_state

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 6:
                recording = True
                log("started recording!", "success")
                
                continue
            elif event.button == 4:
                recording = False
                log("stopped recording!", "success")

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
            new_state = replace_at_index(new_state, place_to_change, str(new_value))
    
    if new_state != drone_controller.current_state:
        drone_controller.move_state(new_state)
