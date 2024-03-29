import cv2
import time
import os

from datetime import datetime

session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs(f"data/{session_id}", exist_ok=True)

tello_video = cv2.VideoCapture("udp://@0.0.0.0:11111")

returned = False
scale = 2
frame_num = 0
skip = False

amount_of_data = 0

while True:
    returned, frame = tello_video.read()
    frame_num += 1

    if returned and frame_num % 10 == 0:
        height, width, layers = frame.shape

        new_h = int(height / scale)
        new_w = int(width / scale)

        resize = cv2.resize(frame, (new_w, new_h))
        cv2.imshow("tello feed", resize)

        if os.path.exists("drone_stream.txt") and os.path.getsize("drone_stream.txt") > 0:
            with open("drone_stream.txt", "r") as file:
                content = file.read().strip()
            
            if skip:
                if content != "0_0_0_0_2":
                    print("drone has taken off again!")
                    skip = False
                else:
                    print("drone is on the ground, skipping...")

            if content != "0_0_0_0_0" and not skip:
                current_time = datetime.now().strftime("%H-%M-%S")

                final_name = f"{amount_of_data}_{current_time}_{content}.png"
                if not cv2.imwrite(f"data/{session_id}/{final_name}", resize):
                    print(f"failed to save picture @ data/{session_id}/{final_name}")
                else:
                    amount_of_data += 1

                    print(f"{amount_of_data} | saved image @ data/{session_id}/{final_name}")
                
                if content == "0_0_0_0_2":
                    print("landed! waiting for drone to take off again...")
                    skip = True

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

tello_video.release()
cv2.destroyAllWindows()