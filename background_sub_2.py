import numpy as np
import cv2 as cv
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils

cap = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()
LOWER_BOUND = 127

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)

    res = cv.bitwise_and(frame,frame,mask = fgmask)
    imgray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    ret,thresh = cv.threshold(imgray,LOWER_BOUND,255,0)
    image, contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) 
    cv.drawContours(res,contours,-1,(0,255,0),3)

    cv.imshow('frame',res)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()
