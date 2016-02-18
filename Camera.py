# Source1: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces

import cv2
import colorsys
import numpy as np

class Camera:
    def __init__(self,robot,cap):
        self.C = cap
        #self.S = robot
        #self.Color = self.S.get_rgb()

    
