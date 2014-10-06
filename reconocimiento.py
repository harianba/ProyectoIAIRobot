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

# Reconoce la catidad de rojo en una zona determinada por los parametros
def areaRed(img, xI, xF, yI, yF): 
    
    # Contara los pixeles rojos
    c = 0 
    # Define 255 como rojo, para evitar confuciones
    rojo = 255 

    for i in range(xI, xF):
        for j in range(yI, yF):
            if img[i][j] == rojo:
                c += 1

    return c


def reconoce(lower_re, upper_re, lower_gree, upper_gree, lower_ble, upper_ble):
    cap = cv2.VideoCapture(1)

    while(1):
        # Toma cada frame de la imagen
        _, frame = cap.read()

        # Convertimos de BGR a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
        hsv3 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_re, upper_re)
        maskBlue = cv2.inRange(hsv2, lower_ble, upper_ble)
        maskGreen = cv2.inRange(hsv3, lower_gree, upper_gree)

        # Cálculo de "moments" para saber si esta detectando el color
        moments = cv2.moments(mask)
        area = moments['m00']
        blueMoment = cv2.moments(maskBlue)
        blueArea = blueMoment['m00']
        greenMoment = cv2.moments(maskGreen)
        greenArea = greenMoment['m00']

        # Determina los limites de la mascara
        x = mask.shape[0] - 1
        y = mask.shape[1] - 1

        # Determina el punto central de la imagen
        xC = x / 2
        yC = y / 2

        x3 = (x/3)/2
        y3 = y/2

        # Define las variables para los valores centrales de la camara
        xI, xF, yI, yF = xC - (xC / 4), xC + (xC / 4), yC - (yC / 4), yC + (yC / 4)

        # Definimos los rangos de la mascara para el lado izq y der
        derecha = areaRed(mask, xI + (x/4), xF + (x/4), yI + (x/4), yF + (x/4))
        izquierda = areaRed(mask, xI - (x/4), xF - (x/4), yI - (x/4), yF - (x/4))
        
        # Manda a llamar a la funcion de deteccion del objeto con los valores centrales de la imagen
        centro = areaRed(mask, xI, xF, yI, yF)

        if derecha > 700:
            serialCom ("4")
            print "girando izquierda"
            return mask
        if izquierda > 700:
            serialCom("5")
            print "girando derecha"
            return mask
        
        # Si existen mas de 5000 pixeles rojos en la zona entonces existe rojo
        if centro > 5000: 
            print 'Detecto rojo'
            if greenArea > 10000000:
                #Se detiene
                serialCom("1") 
                print 'Encontre rojo y esta en el area'
                cv2.destroyAllWindows()
                return mask
            else:
                serialCom("3")
                print ''
        else:
            print "No hay rojo :v"


        # Impresiones de las ventanas de video
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


# Se definen el rango de los colores para el HSV
lower_red = np.array([170,150,50])
upper_red = np.array([179,255,255])
lower_green = np.array([85,80,150])
upper_green = np.array([95,255,255])
lower_blue = np.array([100,100,100])
upper_blue = np.array([120,255,255])


while True:
    img = reconoce(lower_red, upper_red, lower_green, upper_green, lower_blue, upper_blue)
    cv2.imshow('Congelada', img)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()
