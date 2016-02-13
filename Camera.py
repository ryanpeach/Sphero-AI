# Source1: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces

import cv2
import colorsys
import numpy as np

class Camera:
    def __init__(self,S,c=0):
        self.C = cv2.VideoCapture(c)
        self.S = S
        self.Color = self.S.get_rgb()

    def capture(self,colorRange):
        ret, frame = self.C.read()

        # Get color
        r,g,b = s.get_rgb()
        h,s,v = colorsys.rgb_to_hsv(r,g,b)

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        dh, ds, dv = colorRange
        lower = np.array([h-dh/2.,s-ds/2.,v-dv/2.])
        upper = np.array([h+dh/2.,s+ds/2.,v+dv/2.])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv,lower,upper)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        # Show
        cv2.imshow("Frame",frame)
        cv2.imshow("Mask",res)

        # Get the circle

        # Get the location, and radius
        x, y, r = 0, 0, 0

        return x,y,r
