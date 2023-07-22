from djitellopy import tello
from time import sleep
from pygame.locals import *

import pygame
import cv2
import random

pygame.init()
pygame.joystick.init()

class DroneController:
    def __init__(self, session_id):
        super().__init__()
        self.drone = None
        self.stream_display = False
        self.speed = 0
        self.last_movement = { "x": 0, "y": 0, "z": 0 }
        self.last_rotation = { "x": 0, "y": 0 }

        self.rumble_intensity = 6000

        self.last_z_request = None
        self.last_x_request = None
        self.future_command = None
        self.last_rotation_dr = None
        self.processing = False
        self.stream = None

        self.session_id = session_id

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
        if pygame.joystick.get_count() > 0:
            # rumble controller to let pilot know they can know move
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            joystick.rumble(self.rumble_intensity, self.rumble_intensity, 2)

    def move(self, x=0, y=0, z=0, yaw=0):
        self.drone.send_rc_control(int(x * self.speed), int(z * self.speed), int(y* self.speed), yaw)
        self.last_movement = { "x": x, "y": y, "z": z }
    
    def rotate(self, degrees, last_rotation):
        if degrees >= 180 and degrees <= 360:
            self.drone.rotate_counter_clockwise(360 - round(degrees))
            self.last_rotation_dr = -1
        else:
            self.drone.rotate_clockwise(round(degrees))
            
            if round(degrees) == 0:
                self.last_rotation_dr = 0
            else:
                self.last_rotation_dr = 1
        
        self.last_rotation = { "x": last_rotation["x"], "y": last_rotation["y"]}
        self.last_movement = { "x": 0, "y": 0, "z": 0 }

    def land(self):
        print(f"< landing... >")

        self.drone.send_rc_control(0, 0, 0, 0)
        self.drone.land()

    def streamon(self):
        self.drone.streamon()

    def start_video(self):
        while self.stream_display:
            img = self.drone.get_frame_read().frame
            cv2.imshow("live feed", img)
            cv2.waitKey(1)

    def end_video(self):
        self.stream_display = False
    
    def get_last_movement(self):
        return self.last_movement
    
    def record_picture(self):
        if self.last_movement == { "x": 0, "y": 0, "z": 0 } and self.last_rotation == { "x": 0, "y": 0 }:
            return
        
        if self.stream == None:
            self.stream = cv2.VideoCapture("udp://@0.0.0.0:11111")
        
        self.processing = True

        x = self.last_movement["x"]
        y = self.last_movement["y"]
        z = self.last_movement["z"]
        r = self.last_rotation_dr or 0

        ret, frame = self.stream.read()

        if(ret):
            height , width , layers = frame.shape

            new_h=int(height/3)
            new_w=int(width/3)

            resize = cv2.resize(frame, (new_w, new_h))
            cv2.imshow("tello",resize)

        # img = self.drone.get_frame_read().frame
        # payload = fr"data/{self.session_id}/{x}_{y}_{z}_{r}_{random.getrandbits(16)}.png"

        # print("saving image to", payload)
        # cv2.imwrite(payload, img)

        self.processing = False