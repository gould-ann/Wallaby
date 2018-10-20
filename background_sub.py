import numpy as np
import cv2 as cv
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils

cap = cv.VideoCapture("/Users/devinuner/Desktop/michael1.mov")
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

fgbg = cv.createBackgroundSubtractorMOG2()
MIN_CONTOUR_AREA = 25
LOWER_BOUND = 127


trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
multiTracker = cv.MultiTracker_create()
colors = []

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]: 
    tracker = cv.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)
     
  return tracker

seen_butt, seen_shoes, seen_knee = False, False, False
multiTracker = cv.MultiTracker_create()

points = []
foot = None
boxes = []
avgs = []
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)


    

    res = cv.bitwise_and(frame,frame,mask = fgmask)



    imgray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    ret,thresh = cv.threshold(imgray,LOWER_BOUND,255,0)

    # # load the image and resize it to (1) reduce detection time
    # # and (2) improve detection accuracy
    # image = imutils.resize(res, width=min(400, res.shape[1]))
    # orig = image.copy()
 
    # # detect people in the image
    # (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
    #     padding=(8, 8), scale=1.05)
 
    # # draw the original bounding boxes
    # for (x, y, w, h) in rects:
    #     cv.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
    # # apply non-maxima suppression to the bounding boxes using a
    # # fairly large overlap threshold to try to maintain overlapping
    # # boxes that are still people
    # rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
 
    # # draw the final bounding boxes
    # for (xA, yA, xB, yB) in pick:
    #     cv.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)





    image, contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) 
    large_countors = []
    all_x = []
    all_y = []

    # getting all contours and adding the large ones average positions to an array 
    for contour in contours:
        if cv.contourArea(contour) > MIN_CONTOUR_AREA:
            large_countors.append(contour)
            M = cv.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # print cX, cY
            all_x += [cX]
            all_y += [cY]

    legs = []
    arms = []




    # slopes = []

    if len(all_x) > 0:
        avg = [sum(all_x)/len(all_x), sum(all_y)/len(all_y)]
        for contour in contours:
            if cv.contourArea(contour) > MIN_CONTOUR_AREA:
                M = cv.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                if abs(cX - avg[0]) < 100 and abs(cY - avg[1]) < 100:
                    if cY > avg[1]:
                        legs.append(contour)


                        # BUTT TRACKING
                        if cY -50 < avg[1] and cX +50 < avg[0] and not seen_butt:
                            seen_butt = True
                            x,y,w,h = cv.boundingRect(contour)
                            cv.rectangle(res,(x,y),(x+w,y+h),(255,255,0),2)
                            bbox = (x,y,w,h)
                            # Specify the tracker type
                            trackerType = "CSRT"   
                                                         
                            multiTracker.add(createTrackerByName(trackerType), res, bbox)
                        # FOOT TRACKING
                        if cY - 30 > avg[1] and cX > avg[0] + 30 and not seen_knee and seen_butt:
                            seen_knee = True
                            x,y,w,h = cv.boundingRect(contour)
                            cv.rectangle(res,(x,y),(x+w,y+h),(255,255,0),2)
                            bbox = (x,y,w,h)
                            # Specify the tracker type
                            trackerType = "CSRT"   
                             
                            # Create MultiTracker object
                            multiTracker.add(createTrackerByName(trackerType), res, bbox)
                        if seen_knee and seen_butt and not seen_shoes and len(boxes) == 2:
                            diff_x = abs(boxes[0][0] - boxes[1][0])
                            if diff_x < 40:
                                seen_shoes = True
                                foot_x = (boxes[0][0] + boxes[1][0])/2
                                foot_y = 1.9*boxes[1][1] - boxes[0][1]
                                foot = [foot_x, foot_y]
                                # multiTracker.add(createTrackerByName(trackerType), res, (foot_x-10, foot_y-10, 20, 20))


                        # rows,cols = res.shape[:2]
                        # [vx,vy,x,y] = cv.fitLine(contour, cv.DIST_L2,0,0.01,0.01)
                        # slopes += [vy/vx]
                        # # lefty = int((-x*vy/vx) + y)
                        # # righty = int(((cols-x)*vy/vx)+y)
                        # # cv.line(res,(cols-1,righty),(0,lefty),(0,0,255),3)
                    else:
                        arms.append(contour)




        


    # DRAW ALL BOXES AROUND ALL TRACKED OBJECTS
    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(res)
    # draw tracked objects
    # for i, newbox in enumerate(boxes):
    #     print "here:", newbox
    #     cv.circle(res, (int(newbox[0]+newbox[2]/2), int(newbox[1]+newbox[3]/2)), 10, (0,0,255), thickness=-1)
        # cv.rectangle(res, p1, p2, (255,0,255), 2, -1)
    if len(boxes) >= 2:
        for i, newbox in enumerate(boxes):
            cv.circle(res, (int(newbox[0]+newbox[2]/2), int(newbox[1]+newbox[3]/2)), 10, (0,0,255), thickness=-1)
            if i+1 < len(boxes):
                cv.line(res, (int(boxes[i][0]+boxes[i][2]/2), int(boxes[i][1]+boxes[i][3]/2)), (int(boxes[i+1][0]+boxes[i+1][2]/2), int(boxes[i+1][1]+boxes[i+1][3]/2)), (255,100,50), 5)
            elif foot:
                cv.circle(res, (int(foot[0]), int(foot[1])), 10, (0,0,255), thickness=-1)
                cv.line(res, (int(boxes[i][0]+boxes[i][2]/2), int(boxes[i][1]+boxes[i][3]/2)), (int(foot[0]), int(foot[1])), (255,100,50), 5)


    # if len(slopes) > 0:
    #     avg_slope = sum(slopes)/len(slopes)
    #     avgs += [avg_slope]


    #     if(len(avgs) > NUM_MOVING_AVGS):
    #         avg_slope = sum(avgs[-NUM_MOVING_AVGS:])/NUM_MOVING_AVGS
    #         lefty = int((-x*avg_slope) + y)
    #         righty = int(((cols-x)*avg_slope)+y)
    #         cv.line(res,(cols-1,righty),(0,lefty),(0,0,255),3)

    # find the left

    cv.drawContours(res,legs,-1,(0,255,0),3)
    # cv.drawContours(res,arms,-1,(255,0,0),3)

    cv.imshow('frame',res)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()