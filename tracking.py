from __future__ import print_function
import urllib2
import sys
import cv2
from random import randint
from os import listdir
from os.path import isfile, join
 
trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
 
def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]: 
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)
         
    return tracker


mypath = "."
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and ".mov" in f]
videoPath = onlyfiles[0]
print("Path: ", videoPath)
name = videoPath.split(".")[0].split("-")[0]
type = videoPath.split(".")[0].split("-")[1]
date = videoPath.split(".")[0].split("-")[2]
# Set video to load
# videoPath = "/Users/devinuner/Desktop/ann1.mov"
 
# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)
 
# Read first frame
success, frame = cap.read()
# quit if unable to read the video file
if not success:
    print('Failed to read video')
    sys.exit(1)

## Select boxes
bboxes = []
colors = [] 
 
# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects
# while True:
# draw bounding boxes over objects
# selectROI's default behaviour is to draw box starting from the center
# when fromCenter is set to false, you can draw box starting from top left corner
for i in range(3):
    bbox = cv2.selectROI('MultiTracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
# print("Press q to quit selecting boxes and start tracking")
# print("Press any other key to select next object")
# k = cv2.waitKey(0) & 0xFF
# if (k == 113):  # q is pressed
    # break
 
print('Selected bounding boxes {}'.format(bboxes))









# Specify the tracker type
trackerType = "CSRT"   
 
# Create MultiTracker objectf
multiTracker = cv2.MultiTracker_create()
 
# Initialize MultiTracker 
for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox)


good = True
in_rep = False
num_reps = 0
angle_2s = []
# Process video and track objects
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
     
    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame)
 
    # draw tracked objects
    centers = [None, None, None]
    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        centers[i] = [newbox[0] + newbox[2]/2, newbox[1], newbox[3]/2]
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

    angle_1 = abs((centers[2][1]-centers[1][1]) / (centers[2][0] - centers[1][0]))
    angle_2 = abs((centers[1][1]-centers[0][1]) / (centers[1][0] - centers[0][0]))
    angle_2s.append(angle_2)
    if len(angle_2s) > 5 and sum(angle_2s[-5:])/5.0 < 2 and not in_rep:
        num_reps += 1
        in_rep = True
        print(num_reps)
    if sum(angle_2s[-5:])/5.0 > 2:
        in_rep = False

    # print(angle_1)
    if angle_1 < 3 and good and in_rep:
        good = False
        print("BAD JOB!!!")
        num_reps -= 1
    if angle_1 > 5 and not good:
        good = True
 
    # show frame
    cv2.imshow('MultiTracker', frame)
     
 
    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break

print(num_reps)
contents = urllib2.urlopen("http://ec2-18-222-115-164.us-east-2.compute.amazonaws.com/cgi-bin/webhook.cgi?name=Ann%20Gould&reps=" + str(num_reps) + "&exercise=squats&date=17830").read()