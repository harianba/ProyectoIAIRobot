import cv2
import numpy as np
import serial
from time import sleep

def serialCom(int):
    ser =  serial.Serial(port = "/dev/ttyACM0", baudrate=9600)
    x = ser.readline()
    ser.write(int)
    x = ser.readline()
    print 'Enviado: ', x
    #sleep(2)

def contornos(frame):
    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(frame,contours,-1,(0,0,255),3) #Detecta contorno
    #cv2.drawContours(frame,contours,-1,(0,255,0),-1) # Inverso al contorno
    cnt = contours[0]
    #cv2.drawContours(frame,[cnt],0,(255,0,0),-1)

    approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
    if len(approx)==4:
        print "square"
        cv2.drawContours(frame,contours,-1,(0,0,255),3) #Detecta contorno
        cv2.drawContours(frame,[cnt],0,(0,0,255),-1)

    return imgray

def areaRed(img):
    x = img.shape[0] - 1
    y = img.shape[1] - 1
    xC = x / 2 # Centro de la imagen
    yC = y / 2
    area = []
    pixeles = []
    c = 0
    rojo = 255
    xI, xF, yI, yF = xC - (xC / 4), xC + (xC / 4), yC - (yC / 4), yC + (yC / 4)

    zonaIzqX = [0, x / 3]
    #zonaIzqY = [0, y / 3]
    zonaCentroX = [zonaIzqX[1], zonaIzqX[1] * 2]
    #zonaCentroY = [zonaIzqY[1], zonaIzqY[1] * 2]
    zonaDerX = [zonaCentroX[1], x]
    #zonaDerY = [zonaCentroX[1], y]

    for i in range(xI, xF):
        for j in range(yI, yF):
            if img[i][j] == rojo:
                area.append(img[i][j])
                pixeles.append([i, j])
                c += 1

    '''
    print 'Resolucion', x, ' x ', y
    print 'Area de deteccion', (xF - xI) * (yF - xI)
    print 'Pixeles rojos', c, ' de ', x * y
    if len(pixeles) > 0:
        print 'Punto inicial de la mascara: ', pixeles[0]
        print 'Punto final de la mascara: ', pixeles[len(pixeles) - 1]
    print 'Coordenadas de rojo', pixeles
    #raw_input()
    '''

    return c


def reconoce(lower_re, upper_re, lower_gree, upper_gree, lower_ble, upper_ble):
    cap = cv2.VideoCapture(1)

    while(1):

        # Take each frame
        _, frame = cap.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
        hsv3 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_re, upper_re)
        maskBlue = cv2.inRange(hsv2, lower_ble, upper_ble)
        maskGreen = cv2.inRange(hsv3, lower_gree, upper_gree)
        #canny = cv2.Canny(frame, 100, 200)

        # Bitwise-AND mask and original image
        #res = cv2.bitwise_and(frame,frame, mask= mask)

        moments = cv2.moments(mask)
        area = moments['m00']
        blueMoment = cv2.moments(maskBlue)
        blueArea = blueMoment['m00']
        greenMoment = cv2.moments(maskGreen)
        greenArea = greenMoment['m00']

        d = areaRed(mask)
        if d > 8000: # 25724 es el numero de pixeles en el area central
            print 'Detecto rojo'
            #serialCom("1")
            #serialCom("3") # Manda  2 para indicar al robot que se detenga al encontrar el objeto rojo que debera agarrar
            #sleep(20)
            if greenArea > 10000000:
                #serialCom("1") # Manda 1 para indicar al robot que se mueva mientras se encuentra en el area de trabajo
                print 'Encontre rojo y esta en el area'
                cv2.destroyAllWindows()
                serialCom("1") #Se detiene
                return mask
            else:
                serialCom("3")
        else:
            #serialCom("3")
            print "No hay rojo :v"

        cv2.imshow('frame',frame)
        cv2.imshow('rojo',mask)
        #cv2.imshow('verde', maskGreen)
        #cv2.imshow('res',res)
        #cv2.imshow('Canny', canny)
        #cv2.imshow('gray',imgray)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


#reconoce()

# define range of blue color in HSV
lower_red = np.array([170,150,50])
upper_red = np.array([179,255,255])
lower_green = np.array([85,80,150])
upper_green = np.array([95,255,255])
lower_blue = np.array([100,100,100])
upper_blue = np.array([120,255,255])
#serialCom("1")
#serialCom("1")
while True:
    img = reconoce(lower_red, upper_red, lower_green, upper_green, lower_blue, upper_blue)
    cv2.imshow('Congelada', img)
    #areaRed(img)
    cv2.waitKey(10000)
    #serialCom("2")
    #serialCom("1")
    cv2.destroyAllWindows()
