import numpy as np
import cv2 as cv
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils

cap = cv.VideoCapture('/Users/anngould/Desktop/Wallaby/ann2.mov')
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

fgbg = cv.createBackgroundSubtractorMOG2()
MIN_CONTOUR_AREA = 50
NUM_MOVING_AVGS = 5
lowerbody_cascade = cv.CascadeClassifier('haarcascade_lowerbody.xml')  



avgs = []
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)


    

    res = cv.bitwise_and(frame,frame,mask = fgmask)


    # imgray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    # ret,thresh = cv.threshold(imgray,127,255,0)

    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    image = imutils.resize(res, width=min(400, res.shape[1]))
    orig = image.copy()
    arrLower_body = lowerbody_cascade.detectMultiScale(image)
 
    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)
    for (x, y, w, h) in arrLower_body:
        cv.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
 
    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)


    cv.imshow('frame',image)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()