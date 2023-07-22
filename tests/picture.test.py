import cv2
from time import sleep

telloVideo = cv2.VideoCapture("udp://@0.0.0.0:11111")

ret = False
scale = 3
frame_num = 0

while(True):
    ret, frame = telloVideo.read()
    frame_num += 1

    if ret and frame_num % 60 == 0:
        print(ret)
        height , width , layers =  frame.shape
        new_h=int(height/scale)
        new_w=int(width/scale)
        resize = cv2.resize(frame, (new_w, new_h))
        cv2.imshow('Tello',resize)
        
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("test.jpg", resize)
        print("Take Picture")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
telloVideo.release()
cv2.destroyAllWindows()