from djitellopy import tello
from time import sleep
from pygame.locals import *

import pygame

pygame.init()
pygame.joystick.init()

class DroneController:
    def __init__(self):
        super().__init__()
        self.drone = None
        self.stream_display = False
        self.speed = 0
        self.is_flying = 0
        self.landing = False

        self.last_movement = { "x": 0, "y": 0, "z": 0 }
        self.last_rotation = 0

        self.rumble_intensity = 6000

        self.last_z_request = None
        self.last_x_request = None

    def connect(self):
        self.drone = tello.Tello()
        self.drone.connect()
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_last_x_request(self, new_value):
        self.last_x_request = new_value
    
    def set_last_z_request(self, new_value):
        self.last_z_request = new_value

    def takeoff(self):
        print(f"< {self.drone.get_battery()}% battery left >")
        print(f"< taking off... >")

        self.drone.takeoff()
        self.is_flying = 1

        if pygame.joystick.get_count() > 0:
            # rumble controller to let pilot know they can know move
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            joystick.rumble(self.rumble_intensity, self.rumble_intensity, 2)

    def move(self, x=0, y=0, z=0, yaw=0):
        self.drone.send_rc_control(int(x * self.speed), int(z * self.speed), int(y* self.speed), int(yaw * self.speed * 1.2))
        self.last_movement = { "x": x, "y": y, "z": z }
        self.last_rotation = yaw
    
    # def rotate(self, degrees, last_rotation):
    #     if degrees >= 180 and degrees <= 360:
    #         self.drone.rotate_counter_clockwise(360 - round(degrees))
    #         self.last_rotation_dr = -1
    #     else:
    #         self.drone.rotate_clockwise(round(degrees))
            
    #         if round(degrees) == 0:
    #             self.last_rotation_dr = 0
    #         else:
    #             self.last_rotation_dr = 1
        
    #     self.last_rotation = { "x": last_rotation["x"], "y": last_rotation["y"]}
    #     self.last_movement = { "x": 0, "y": 0, "z": 0 }

    def land(self):
        print("< landing... >")

        self.is_flying = 0
        self.landing = True

        movement_string = "0_0_0_0_2"
        
        with open("drone_stream.txt", "w") as file:
            print("writing", movement_string, "to drone_stream.txt")
            file.write(movement_string)

        self.drone.send_rc_control(0, 0, 0, 0)
        self.drone.land()

        print("< stalling... >")
        sleep(5)
        print("< resetting >")
        
        self.landing = False

    def streamon(self):
        self.drone.streamon()