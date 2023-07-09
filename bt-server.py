import pygame
import controller
import math

pygame.init()
pygame.joystick.init()

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
    if axis2_value == 0 and axis3_value == 0:
        return 0
    
    angle = math.atan2(axis2_value, axis3_value)

    degrees = math.degrees(angle)
    degrees = (degrees + 360) % 360

    return degrees

def hround(number):
    return round(number * 2) / 2

if pygame.joystick.get_count() <= 0:
    print("< no joysticks found, stopping... >")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

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
            
            rotation["x"] = hround(value) if event.axis == 2 else rotation["x"]
            rotation["y"] = -hround(value) if event.axis == 3 else rotation["y"]

        
    if movement != drone_controller.last_movement:
        # print(f"moving from {movement} to {drone_controller.last_movement}")

        drone_controller.move(movement["x"], movement["y"], movement["z"])
    elif rotation != drone_controller.last_rotation:
        print(rotation["x"], rotation["y"])

        final_rotation = joystick_to_degrees(rotation["x"], rotation["y"])
        drone_controller.rotate(final_rotation, rotation)
