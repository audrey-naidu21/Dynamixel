# import necessary packages
from imutils.object_detection import non_max_suppression
from imutils import paths
from collections import deque
import math
import numpy as np
import argparse
import imutils
import cv2
from ax12a import *

motor1 = AX_12A(id = 1)
motor1.connect()
i = AX_12A.listInstances()
print(i)
pos = AX_12A.getAll('getPresentPosition')
print(pos)
speed = AX_12A.setAll('setMovingSpeed', 100)
print(motor1.getMovingSpeed()) 

xone = 0
yone = 0
xtwo = 0
ytwo = 0

#LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python3 pedestriandetection.py
#command to fix error

ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--images", required=True, help="path to images directory")
#args = vars(ap.parse_args())
ap.add_argument("-v", "--video", help = "path to the (optional) video file")
args = vars(ap.parse_args())

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

recx = 0
recy = 0
#initialize person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

boxes = []
numframe = 0
maxframe = 8
multboxes = []

#list of lists where pedestrians[i] is a list of pedestrian i's previous positions
pedestrians = []

#center of previousframe
previouscenter = 0

#center of window
centerx = 0
centery = 0

#distance between previous center in pedestrian and current center
centerdifference = 0

#flag to check if pedestrian was assigned and matched
assigned = False

#center of drawn rectangle
reconex =0
rectwox= 0
centerboxeslist = []
prev = 0
now = 0
numtotal = 0

assignedPedestrians = {} #map off which pedestrians are already assigned
notUpdatedPedestrians = []



def calcdist(xa, ya, xb, yb):
    rectanglex = (xa + xb)/2
    rectangley = (ya + yb)/2
    print("Center of rectangle: ({}, {})".format(rectanglex, rectangley))
    disty = abs(rectangley - centery)
    distx = abs(rectanglex - centerx)
    return distx

def calcangle(xa, ya, xb, yb):
    rectanglex = (xa + xb)/2
    rectangley = (ya + yb)/2
    angleofpedestrian = math.atan2((rectangley - centery),(rectanglex - centerx))
    return angleofpedestrian


def calccenterx(xa, ya, xb, yb):
    return (xa+xb)/2

def calccentery(xa, ya, xb, yb):
    return (ya+yb)/2

while True:
    (grabbed, frame) = camera.read()


    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)


    centerx = width/2
    centery = height/2

    print("Center: ({}, {})".format(centerx, centery))
        
    if args.get("video") and not grabbed:
        break
    
    frame = imutils.resize(frame, width = 300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#loop over the image paths
    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    
    orig = frame.copy()

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(orig, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    #if numframe >= 8:




            # draw the final bounding boxes
    for i, (xA, yA, xB, yB) in enumerate(pick):

        # go through our list of lists data structure
        centeronex = (xA + xB)/2
        distancex = calcdist(xA, yA, xB, yB)
        xone = xA
        yone = yA
        xtwo = xB
        ytwo = yB
        print("The pedestrian is {} pixels away.".format(distancex))
        #angle = math.atan2((recy - centery),(recx - centerx))
        angle = calcangle(xA, yA, xB, yB)
        print("Angle: {}".format(angle))
        assigned = False
        for pedIndex, pedestrian in enumerate(pedestrians):
            previouscenter = calccenterx( *pedestrian[-1]) #get center of last frame in pedestrian
            centerdifference= abs(previouscenter - centeronex)
            # if the box is within 100px horizontally of the average of the current pedestrian's past positions and we haven't already added a different box to this pedestrian from this frame
            # add box to the end of our structure[i]
            if centerdifference <= 100: 
                pedestrian.append((xA, yA, xB, yB))
                assigned = True
                assignedPedestrians[pedIndex] = True






    for pedestrian in pedestrians:
        while len(pedestrian) > 8: 
            pedestrian.pop(0)
        if len(pedestrian) < 8:
            cv2.rectangle(orig, (xA, yA), (xB, yB), (0, 255, 0), 2)
            distancex = calcdist(xA, yA, xB, yB)
            print("The pedestrian is {} pixels away.".format(distancex))
            #angle = math.atan2((recy - centery),(recx - centerx))
            angle = calcangle(xA, yA, xB, yB)
            print("Angle: {}".format(angle))
            #numframe = numframe + 1
        if len(pedestrian) >= 8:
            avga= int(np.mean( [a for (a,_,_,_) in pedestrian] ))
            avgb= int(np.mean( [b for (_,b,_,_) in pedestrian] ))
            avgc= int(np.mean( [c for (_,_,c,_) in pedestrian] ))
            avgd= int(np.mean( [d for (_,_,_,d) in pedestrian] ))
            print("Averages: {}, {}, {}, {}".format(avga, avgb, avgc, avgd))
            
            distancex = calcdist(avga, avgb, avgc, avgd)
            reconex = distancex
            print("The pedestrian is {} pixels away.".format(distancex))
            angle = calcangle(avga, avgb, avgc, avgd)
            print("Angle: {}".format(angle))
            cv2.rectangle(orig, (avga, avgb), (avgc, avgd), (0, 255, 0), 2)

    centerofrectanglex = calccenterx(xone, xtwo, yone, ytwo)
    centerofrectangley = calccentery(xone, xtwo, yone, ytwo)
    windowwidth = width
    print(windowwidth)
    
    while centerofrectanglex > centerx:
        pos = AX_12A.getAll('getPresentPosition')
        print(pos)
        nowpos = pos[0]
        speed = AX_12A.setAll('setMovingSpeed', 70)
        print(motor1.getMovingSpeed())
        nowpos = nowpos+10
        if nowpos > 1014:
            nowpos = 1014
            break
        motor1.setGoalPosition(nowpos)
        
    while centerofrectanglex < centerx:
        pos = AX_12A.getAll('getPresentPosition')
        print(pos)
        nowpos = pos[0]
        speed = AX_12A.setAll('setMovingSpeed', 70)
        print(motor1.getMovingSpeed())
        nowpos = nowpos-10
        if nowpos < 0:
            nowpos = 0
            break
        motor1.setGoalPosition(nowpos)


        

        
    # show some information on the number of bounding boxes
    #filename = imagePath[imagePath.rfind("/") + 1:]
    filename = "one"
    print("[INFO] {}: {} original boxes, {} after suppression".format(
        filename, len(rects), len(pick)))

    # width = camera.get(3)
    # height = camera.get(4)


    

    

    # show the output images
    #cv2.imshow("Before NMS", frame)
    cv2.imshow("After NMS", orig)
    
    cv2.waitKey(1)
 

    
    
camera.release()
cv2.destroyAllWindows()