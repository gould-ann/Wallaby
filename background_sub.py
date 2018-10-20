import numpy as np
import cv2 as cv
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils

cap = cv.VideoCapture('/Users/devinuner/Desktop/ann2.mov')
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

fgbg = cv.createBackgroundSubtractorMOG2()
MIN_CONTOUR_AREA = 50
NUM_MOVING_AVGS = 5



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
 
    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)
 
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





    # image, contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) 
    # large_countors = []
    # all_x = []
    # all_y = []

    # # getting all contours and adding the large ones average positions to an array 
    # for contour in contours:
    #     if cv.contourArea(contour) > MIN_CONTOUR_AREA:
    #         large_countors.append(contour)
    #         M = cv.moments(contour)
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         # print cX, cY
    #         all_x += [cX]
    #         all_y += [cY]

    # legs = []
    # arms = []

    # # slopes = []

    # if len(all_x) > 0:
    #     avg = [sum(all_x)/len(all_x), sum(all_y)/len(all_y)]
    #     for contour in contours:
    #         if cv.contourArea(contour) > MIN_CONTOUR_AREA:
    #             M = cv.moments(contour)
    #             cX = int(M["m10"] / M["m00"])
    #             cY = int(M["m01"] / M["m00"])

    #             if abs(cX - avg[0]) < 100 and abs(cY - avg[1]) < 100:
    #                 if cY > avg[1]:
    #                     legs.append(contour)
    #                     # rows,cols = res.shape[:2]
    #                     # [vx,vy,x,y] = cv.fitLine(contour, cv.DIST_L2,0,0.01,0.01)
    #                     # slopes += [vy/vx]
    #                     # # lefty = int((-x*vy/vx) + y)
    #                     # # righty = int(((cols-x)*vy/vx)+y)
    #                     # # cv.line(res,(cols-1,righty),(0,lefty),(0,0,255),3)
    #                 else:
    #                     arms.append(contour)


    # # if len(slopes) > 0:
    # #     avg_slope = sum(slopes)/len(slopes)
    # #     avgs += [avg_slope]


    # #     if(len(avgs) > NUM_MOVING_AVGS):
    # #         avg_slope = sum(avgs[-NUM_MOVING_AVGS:])/NUM_MOVING_AVGS
    # #         lefty = int((-x*avg_slope) + y)
    # #         righty = int(((cols-x)*avg_slope)+y)
    # #         cv.line(res,(cols-1,righty),(0,lefty),(0,0,255),3)

    # # find the left

    # cv.drawContours(res,legs,-1,(0,255,0),3)
    # cv.drawContours(res,arms,-1,(255,0,0),3)

    cv.imshow('frame',image)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()