import cv2
import numpy as np

cam=cv2.VideoCapture(0)
n=0

while True:
    returnVal,frame=cam.read()

    img=cv2.GaussianBlur(frame, (5,5), 0)
    img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower=np.array([0,150,0],np.uint8)
    red_upper=np.array([10,255,255],np.uint8)
    red=cv2.inRange(img,red_lower,red_upper)

    cv2.imshow('img',red)

    key = cv2.waitKey(10) % 0x100
    if key == 27: break #ESC 