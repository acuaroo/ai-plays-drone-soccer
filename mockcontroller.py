from djitellopy import tello
import cv2

class DroneController:
    def __init__(self):
        super().__init__()
        self.stream_display = False
        self.speed = 0
        self.last_movement = { "x": 0, "y": 0, "z": 0 }
        self.last_rotation = { "x": 0, "y": 0 }

        self.last_z_request = None
        self.last_x_request = None

    def connect(self):
        print("MOCK CONNECT")
    
    def set_speed(self, speed):
        print(f"MOCK SET SPEED {speed}")
    
    def set_last_x_request(self, new_value):
        self.last_x_request = new_value
    
    def set_last_z_request(self, new_value):
        self.last_z_request = new_value

    # def get_drone(self, is_streaming=False):
    #     self.connect()

    #     if is_streaming:
    #         self.drone.streamon()
    #         self.stream_display = True

    #     return self.drone

    def takeoff(self):
        print(f"MOCK TAKEOFF...")

    def move(self, x=0, y=0, z=0, yaw=0):
        print(f"MOCK RC CONTROL: {int(x * self.speed), int(z * self.speed), int(y* self.speed), yaw}")
        self.last_movement = { "x": x, "y": y, "z": z }
    
    def rotate(self, degrees, last_rotation):
        if degrees >= 180 and degrees <= 360:
            print(f"MOCK ROTATION CCW {360 - round(degrees)}")
        else:
            print(f"MOCK ROTATION CW {round(degrees)}")
        
        self.last_rotation = { "x": last_rotation["x"], "y": last_rotation["y"]}

    def land(self):
        print(f"MOCK LANDING")

    # def start_video(self):
    #     while self.stream_display:
    #         img = self.drone.get_frame_read().frame
    #         cv2.imshow("live feed", img)
    #         cv2.waitKey(1)

    # def end_video(self):
    #     self.stream_display = False