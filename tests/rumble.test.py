import pygame
from pygame.locals import *

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    joystick.rumble(intensity, intensity, 2)
else:
    print("No joystick/gamepad found.")

# Quit Pygame
pygame.quit()
