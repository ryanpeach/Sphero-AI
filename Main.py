import time
from sphero_driver import Sphero
from Camera import *
import colorsys

MAC = "68:86:E7:02:AB:C1"
r, g, b = 255, 0, 0

def connectSphero(target_addr):
    """ Initializes Sphero """
    s = Sphero(target_addr = target_addr)
    s.connect()
    con = False
    while not con:
        try:
            con = s.connect()
        except:
            continue
    return s

# Initialize Camera
#s = connectSphero(MAC)
#c = s.set_rgb(r,g,b,1,1)
h,s,v = colorsys.rgb_to_hsv(r,g,b)
print(h,s,v)
testFilter()


#s.set_heading(0)
#s.roll(speed,a)
#s.get_rgb()
#s.set_rgb
