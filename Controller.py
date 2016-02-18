# Tutorials: http://docs.opencv.org/master/dd/d43/tutorial_py_video_display.html#gsc.tab=0
#            http://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
import cv2, colorsys
import numpy as np
from matplotlib import pyplot as plt
import time

host = "192.168.0.108"
portI, portO, vport = 23451, 12345, 8081

def getVideo(host, port):
    vhost = "http://"+host+":"+str(vport)+"/video?x.mjpeg"
    cap = cv2.VideoCapture()
    cap.open(vhost)
    print("Video Feed Established.")
    return cap

def getComm(host, portI, portO):
    i, o = socket.socket(), socket.socket()         # Create a socket object
    o.connect((host, portO))

    i.bind(('', portI))
    i.listen(5)
    c, addr = i.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')

    return c, o

def testComm():

    i, o = getComm(host, portI, portO)

    o.send("set_rgb, 55, 85, 55")
    print str(i.recv(1024))
    o.send("get_rgb, 0, 0, 0")
    print str(i.recv(1024))
    time.sleep(100)
    o.close                     # Close the socket when done
    i.close

testComm()
