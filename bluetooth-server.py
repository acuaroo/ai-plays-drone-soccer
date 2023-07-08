import pygame
import controller
import math

pygame.init()
joysticks = []

# prep the drone
drone_controller = controller.DroneController()
drone_controller.connect()
drone_controller.set_speed(20)

clock = pygame.time.Clock()
alive = True

movement = { "x": 0, "y": 0, "z": 0 }
rotation = { "x": 0, "y": 0 }

button_map = {
    "2": drone_controller.takeoff,
    "1": drone_controller.land,
}

def joystick_to_degrees(axis2_value, axis3_value):
    angle = math.atan2(axis2_value, axis3_value)

    degrees = math.degrees(angle)    
    degrees = (degrees + 360) % 360

    return degrees

# look and get all joysticks
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

while alive:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            mapped_value = button_map.get(str(event.button))

            if mapped_value:
                mapped_value()
        elif event.type == pygame.JOYAXISMOTION:
            # y motion
            if event.axis == 5:
                movement["y"] = 1 if event.value > 0 else 0
            elif event.axis == 4:
                movement["y"] = -1 if event.value > 0 else 0
            
            if event.axis == 0 and not (drone_controller.last_x_request == round(event.value)):
                rounded_value = round(event.value)

                movement["x"] = rounded_value
                drone_controller.set_last_x_request(rounded_value)

            if event.axis == 1 and not (drone_controller.last_z_request == round(event.value)):
                rounded_value = -round(event.value)

                movement["z"] = rounded_value
                drone_controller.set_last_z_request(rounded_value)
            
            if event.axis == 2:
                rotation["x"] = round(event.value * 2) / 2

            if event.axis == 3:
                rotation["y"] = -round(event.value * 2) / 2

        
    if movement != drone_controller.last_movement:
        # print(f"moving from {movement} to {drone_controller.last_movement}")

        drone_controller.move(movement["x"], movement["y"], movement["z"])
    elif rotation != drone_controller.last_rotation:
        final_rotation = joystick_to_degrees(rotation["x"], rotation["y"])
        drone_controller.rotate(final_rotation, rotation)
