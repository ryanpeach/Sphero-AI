# Source1: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces

import cv2
import colorsys
import numpy as np

class Camera:
    def __init__(self, cap = None):
        if cap is None:
            cap = cv2.VideoCapture(0)
        self.C = cap
        #self.S = robot
        #self.Color = self.S.get_rgb()
        
    def next(self):
        ret, frame = self.C.read()
        while not ret:
            ret, frame = self.C.read()
        return frame
    
    def filter(self, frame, min_color, max_color):
        # Get color
        r1,g1,b1 = min_color
        h1,s1,v1 = colorsys.rgb_to_hsv(r1,g1,b1)
        #print("Frame",type(frame))
    
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # define range of blue color in HSV
        h2, s2, v2 = max_color
        lower = np.array([h1,s1,v1],dtype=np.uint8)
        upper = np.array([h2,s2,v2],dtype=np.uint8)
    
        # Threshold the HSV image to get only blue colors
        if h1 < h2 and s1 < s2 and v1 < v2:
            mask = cv2.inRange(hsv,lower,upper)
            res = cv2.bitwise_and(frame, frame, mask= mask)
            #mask = cv2.Canny(mask, min_canny, max_canny)
        else:
            mask = np.zeros(hsv.shape[0:1],dtype=np.uint8)
            res = frame
    
        #print("Mask",str(mask.dtype))
        #print("Res",str(res.dtype))
        return mask, res

    def circles(self, data, frame, dp = 2, sz = .5, min_canny = 100, max_canny = 200):
        # Get the circle
        # http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
        #print("Circles",type(frame))
        circles = cv2.HoughCircles(data, cv2.HOUGH_GRADIENT, dp = dp, minDist = len(data)*sz, param1 = min_canny, param2 = max_canny)
        if circles is None:
            #print("None found")
            return frame
        else:
            print(circles)
    
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
    
    # Source: http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
    def motion(self, res, firstFrame, secondFrame, min_area):
        # compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, secondFrame)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
        out = res.copy()
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < min_area:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
        
        return out
		
def testFilter():
    #cap = getVideo(host, vport)
    cap = cv2.VideoCapture(0)
    c = Camera(cap)

    # Create GUI
    nothing = lambda x: None
    cv2.namedWindow('mask')
    cv2.createTrackbar('minH','mask',0,255,nothing)
    cv2.createTrackbar('minS','mask',200,255,nothing)
    cv2.createTrackbar('minV','mask',200,255,nothing)
    cv2.createTrackbar('maxH','mask',40,255,nothing)
    cv2.createTrackbar('maxS','mask',255,255,nothing)
    cv2.createTrackbar('maxV','mask',255,255,nothing)
    cv2.createTrackbar('minArea','mask',5,100,nothing)
    #cv2.createTrackbar('maxCanny','mask',200,255,nothing)
    #cv2.createTrackbar('dp','mask',100,200,nothing)
    #cv2.createTrackbar('p','mask',500,1000,nothing)

    ret, firstFrame = cap.read()
    Mask1, Res1 = c.filter(firstFrame,(0,200,200),(40,255,255))
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Get GUI values
        h1 = cv2.getTrackbarPos('minH','mask')
        s1 = cv2.getTrackbarPos('minS','mask')
        v1 = cv2.getTrackbarPos('minV','mask')
        h2 = cv2.getTrackbarPos('maxH','mask')
        s2 = cv2.getTrackbarPos('maxS','mask')
        v2 = cv2.getTrackbarPos('maxV','mask')
        minArea = cv2.getTrackbarPos('minArea','mask')
        #maxCanny = cv2.getTrackbarPos('maxCanny','mask')
        #dp = cv2.getTrackbarPos('dp','mask')
        #p = cv2.getTrackbarPos('p','mask')

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        Mask2, Res2 = c.filter(frame,(h1,s1,v1),(h2,s2,v2))
        C = c.motion(frame,Mask1,Mask2,minArea/100.*len(Mask1))
        Mask1 = Mask2

        # Display the resulting frame
        cv2.imshow("canny", Mask2)
        cv2.imshow("mask", Res2)
        cv2.imshow("cirles", C)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    # When everything done, release the capture
    s.release()
    cv2.destroyAllWindows()
