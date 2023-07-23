import cv2
from time import sleep
from datetime import datetime

telloVideo = cv2.VideoCapture("udp://@0.0.0.0:11111")

ret = False
scale = 2
frame_num = 0

while(True):
    ret, frame = telloVideo.read()
    frame_num += 1

    if ret and frame_num % 60 == 0:
        height, width, layers = frame.shape

        new_h = int(height / scale)
        new_w = int(width / scale)

        resize = cv2.resize(frame, (new_w, new_h))
        cv2.imshow("tello feed", resize)

        final_time = f"{datetime.second}_{datetime.minute}"

        if not cv2.imwrite(f"data/{final_time}.png", resize):
            print(f"failed to save picture @ data/{final_time}.png")
        else:
            print(f"saved image @ data/{final_time}.png")
        
    # if cv2.waitKey(1) & 0xFF == ord('s'):
    #     cv2.imwrite("test.jpg", resize)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

telloVideo.release()
cv2.destroyAllWindows()