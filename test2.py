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
motor1.setGoalPosition(500)
pos = AX_12A.getAll('getPresentPosition')
print(pos)
speed = AX_12A.setAll('setMovingSpeed', 200)
print(motor1.getMovingSpeed()) 
