import cv2
import numpy as np
 
cap = cv2.VideoCapture(0)
 
while(1):
 
    # Take each frame
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # define range of blue color in HSV
    lower_blue = np.array([170,150,60])
    upper_blue = np.array([179,255,255])
 
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
 
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    moments = cv2.moments(mask)
    area = moments['m00']
    if area > 100000:
        print "Es azul"
    else:
        print "No es azul"

    

 
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
cv2.destroyAllWindows()