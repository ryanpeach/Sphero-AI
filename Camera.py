# Source1: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces

import cv2
import colorsys
import numpy as np

class Camera:
    def __init__(self, cap):
        self.C = cap
        #self.S = robot
        #self.Color = self.S.get_rgb()

    
    def filter(self, frame, color, colorRange):
        # Get color
        r,g,b = color
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
        return res


    def circles(self, frame):
        # Get the circle
        # http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
        if circles is None:
            print("None found")
            return frame
    
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        output = frame.copy()
    
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    
        return output
        
    def release(self):
        return self.C.release()

def testFilter():
    #cap = getVideo(host, vport)
    cap = cv2.VideoCapture(0)
    s = Camera(cap)

    # Create GUI
    nothing = lambda x: None
    cv2.namedWindow('image')
    cv2.createTrackbar('H','image',0,255,nothing)
    cv2.createTrackbar('S','image',0,255,nothing)
    cv2.createTrackbar('V','image',0,255,nothing)
    cv2.createTrackbar('dH','image',0,255,nothing)
    cv2.createTrackbar('dS','image',0,255,nothing)
    cv2.createTrackbar('dV','image',0,255,nothing)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Get GUI values
        h = cv2.getTrackbarPos('H','image')
        s = cv2.getTrackbarPos('S','image')
        v = cv2.getTrackbarPos('V','image')
        dh = cv2.getTrackbarPos('dH','image')
        ds = cv2.getTrackbarPos('dS','image')
        dv = cv2.getTrackbarPos('dV','image')

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        Mask = s.filter(frame,(h,s,v),(dh,ds,dv))
        C = s.circles(mask)

        # Display the resulting frame
        cv2.imshow("mask", Mask)
        cv2.imshow("cirles", C)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    # When everything done, release the capture
    s.release()
    cv2.destroyAllWindows()
