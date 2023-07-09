import pygame
from pygame.locals import *

pygame.init()
pygame.joystick.init()
intensity = 5000

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    joystick.rumble(intensity, intensity, 2)

# Quit Pygame
pygame.quit()
