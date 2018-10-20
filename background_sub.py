import numpy as np
import cv2 as cv
cap = cv.VideoCapture('ann1.mov')
fgbg = cv.createBackgroundSubtractorMOG2()
while(1):
    ret, frame = cap.read()
    ret = cv.blur(ret,(5,5))
    fgmask = fgbg.apply(frame)
    res = cv.bitwise_and(frame,frame,mask = fgmask)

    imgray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    # blur = cv.blur(imgray,(10,10))
    ret,thresh = cv.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(res,contours,-1,(0,255,0),3)

    cv.imshow('frame',res)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()