import pygame
import controller
import math
import time

from threading import Thread

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() <= 0:
    print("< no joysticks found, stopping... >")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# prep the drone
drone_controller = controller.DroneController("FAKESESSIONID")
drone_controller.connect()
drone_controller.set_speed(30)

clock = pygame.time.Clock()
alive = True
stall_thread = None

movement = { "x": 0, "y": 0, "z": 0 }
rotation = 0

image_interval = 10
last_image_time = 0

button_map = {
    "2": drone_controller.takeoff,
    "1": drone_controller.land,
}

def hround(number):
    return round(number * 2) / 2

def turn_to_tertiary(x):
    if x == -1:
        return 2
    
    return x

drone_controller.streamon()

while alive:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            mapped_value = button_map.get(str(event.button))

            if mapped_value:
                mapped_value()
        elif event.type == pygame.JOYAXISMOTION:
            value = event.value
            rounded_value = round(value)

            if event.axis == 5:
                movement["y"] = 1 if value > 0 else 0
            elif event.axis == 4:
                movement["y"] = -1 if value > 0 else 0
            
            if event.axis == 0 and not (drone_controller.last_x_request == rounded_value):
                movement["x"] = rounded_value
                drone_controller.set_last_x_request(rounded_value)

            if event.axis == 1 and not (drone_controller.last_z_request == rounded_value):
                movement["z"] = -rounded_value
                drone_controller.set_last_z_request(-rounded_value)
            
            if event.axis == 2:
                rotation = round(event.value)
        
    if movement != drone_controller.last_movement or rotation != drone_controller.last_rotation:
        drone_controller.move(movement["x"], movement["y"], movement["z"], rotation)

        converted_movement = dict(map(lambda x: (x[0], turn_to_tertiary(x[1])), movement.items()))
        converted_rotation = turn_to_tertiary(rotation)

        movement_string = f"{converted_movement['x']}_{converted_movement['y']}_{converted_movement['z']}_{converted_rotation}"
        
        with open("drone_stream.txt", "w") as file:
            file.write(movement_string)
