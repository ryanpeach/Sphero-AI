import time
from sphero import core
from Camera import Camera

# Initialize Sphero
s = core.Sphero("/dev/rfcomm0")
s.connect()

# Initialize Camera
CM1 = Camera(s)

while True:

    CM1.capture((40,40,40))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

#s.set_heading(0)
#s.roll(speed,a)
#s.get_rgb()
#s.set_rgb
