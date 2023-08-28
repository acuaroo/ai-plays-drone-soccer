import math
import pygame

# axis 0 : leftjoy : left=-1 right=1
# axis 1 : leftjoy : up=-1 down=1
# axis 2 : rightjoy : left=-1 right=1
# axis 3 : rightjoy : up=-1 down=1

# axis 5 & 5 : ZL & ZR : up=-1 down=1

pygame.init()
joysticks = []

clock = pygame.time.Clock()
alive = True

rotation = { "x": 0, "y": 0 }

def joystick_to_degrees(axis2_value, axis3_value):
    angle = math.atan2(axis2_value, axis3_value)

    degrees = math.degrees(angle)    
    degrees = (degrees + 360) % 360

    return degrees

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

    print("joystick found")

while alive:
    clock.tick(10)

    for event in pygame.event.get():
        print(event)
