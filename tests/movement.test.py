# ref guide: https://djitellopy.readthedocs.io/en/latest/tello/

from djitellopy import tello
from time import sleep
import threading

import cv2

drone = tello.Tello()
drone.connect()

print(f"< {drone.get_battery()}% battery left >")
input("< press enter to take off >")

drone.streamon()

def routine(x):
    x.takeoff()
    sleep(2)
    x.flip_forward()
    sleep(1)
    x.flip_back()
    sleep(1)
    x.send_rc_control(0, 0, 0, 50)
    sleep(16)
    x.send_rc_control(0, 0, 0, 0)
    x.land()

while True:
    img = drone.get_frame_read().frame
    cv2.imshow("live feed", img)

    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        thread = threading.Thread(target=routine, args=(drone,))
        thread.start()
    elif key == ord('w'):
        drone.streamoff()
        break