# import colorama

from time import sleep
from djitellopy import tello
# from colorama import Fore, Back

state_map = {
    0: "x",
    1: "y",
    2: "z",
    3: "rotation",
    4: "is_flying"
}

# colorama.init(autoreset=True)  


def turn_to_tertiary(x):
    if x == -1:
        return 2
    
    return x


def snap_axis(x):
    return 1 if x > 0 else 0


def replace_at_index(input_string, index, replace):
    if 0 <= index < len(input_string):
        new_string = input_string[:index] + replace + input_string[index + 1:]
        return new_string
    else:
        raise IndexError("requested index is out of range")


def turn_to_negative(x):
    if x == 2:
        return -1
    
    return x


def log(message, log_type="normal"):
    if log_type == "error":
        print(f"!!! {message}")
    elif log_type == "warning":
        print(f"~~~ {message}")
    elif log_type == "success":
        print(f">>> {message}")
    else:
        print(f">>> {message}")  


class DroneController:
    def __init__(self, joystick, verbose=False, mock=False):
        super().__init__()

        self.drone = None
        self.is_flying = False

        self.verbose = verbose
        self.mock = mock

        self.speed = 0
        self.battery = 0

        self.current_state = "0_0_0_0_0"

        self.joystick = joystick
        self.rumble_intensity = 6000
    
    def set_speed(self, speed):
        self.speed = speed
    
    def stream_on(self):
        if self.mock:
            log("MOCK MODE: stream started!", "success")
            return
        
        self.drone.streamon()
    
    def stream_off(self):
        if self.mock:
            log("MOCK MODE: stream ended!", "success")
            return
        
        self.drone.streamoff()

    def connect(self):
        if self.mock:
            log("MOCK MODE: drone connected!", "success")
            return
        
        self.drone = tello.Tello()
        self.drone.connect()

        log("drone connected!", "success")
    
    def takeoff(self):
        if self.is_flying:
            log("attempted to takeoff while already flying!", "warning")
            return
        
        if self.mock:
            log("MOCK MODE: drone took off!", "success")
            self.is_flying = True
            return
        
        self.battery = self.drone.get_battery()
        log(f"{self.battery}% battery left", "normal")

        if self.battery <= 10:
            # give warning to the pilot
            self.joystick.rumble(self.rumble_intensity, self.rumble_intensity, 1)
            sleep(1)
            self.joystick.rumble(self.rumble_intensity, self.rumble_intensity, 1)
        
        self.drone.takeoff()
        self.is_flying = True

        log("drone has taken off!", "success")
        self.joystick.rumble(self.rumble_intensity, self.rumble_intensity, 1)
    
    def move(self, x=0, y=0, z=0, rotation=0):
        if not self.is_flying and self.verbose:
            log("attempted to move while not flying!", "warning")
            return
        
        if self.mock:
            log(f"MOCK MODE: drone moved to {x}, {y}, {z}, {rotation}", "success")
            return
        
        self.drone.send_rc_control(int(x * self.speed), int(z * self.speed), int(y * self.speed), int(rotation * self.speed))

        if self.verbose:
            log(f"drone moved to {x}, {y}, {z}, {rotation}", "normal")

    def move_state(self, new_state):        
        new_state = new_state.split("_")
        old_state = self.current_state.split("_")

        movements = [int(old_state[0]), int(old_state[1]), int(old_state[2]), int(old_state[3])]

        for i in range(len(new_state)):
            if new_state[i] != old_state[i]:
                if i == 4:
                    if new_state[i] == "1":
                        self.takeoff()
                    else:
                        self.land()
                else:
                    movements[i] = new_state[i]
        
        self.current_state = "_".join(new_state)

        movements = [turn_to_negative(int(movement)) for movement in movements]
        self.move(*movements)

    def land(self):
        if not self.is_flying:
            log("attempted to land while not flying!", "warning")
            return
        
        if self.mock:
            self.is_flying = False
            log("MOCK MODE: drone landed!", "success")
            return

        self.is_flying = False
        self.drone.land()

        log("drone has landed!", "success")
        self.joystick.rumble(self.rumble_intensity, self.rumble_intensity, 1)
    
    
