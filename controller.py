from djitellopy import tello
import cv2

class DroneController:
    def __init__(self):
        super().__init__()
        self.drone = None
        self.stream_display = False
        self.speed = 0
        self.last_movement = { "x": 0, "y": 0, "z": 0 }
        self.last_rotation = { "x": 0, "y": 0 }

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

    def get_drone(self, is_streaming=False):
        self.connect()

        if is_streaming:
            self.drone.streamon()
            self.stream_display = True

        return self.drone

    def takeoff(self):
        print(f"< {self.drone.get_battery()}% battery left >")
        print(f"< taking off... >")

        self.drone.takeoff()

    def move(self, x=0, y=0, z=0, yaw=0):
        self.drone.send_rc_control(int(x * self.speed), int(z * self.speed), int(y* self.speed), yaw)
        self.last_movement = { "x": x, "y": y, "z": z }
    
    def rotate(self, degrees, last_rotation):
        if degrees >= 180 and degrees <= 360:
            self.drone.rotate_counter_clockwise(360 - round(degrees))
        else:
            self.drone.rotate_clockwise(round(degrees))
        
        self.last_rotation = { "x": last_rotation["x"], "y": last_rotation["y"]}
        self.last_movement = { "x": 0, "y": 0, "z": 0 }

    def land(self):
        print(f"< landing... >")

        self.drone.send_rc_control(0, 0, 0, 0)
        self.drone.land()

    def start_video(self):
        while self.stream_display:
            img = self.drone.get_frame_read().frame
            cv2.imshow("live feed", img)
            cv2.waitKey(1)

    def end_video(self):
        self.stream_display = False