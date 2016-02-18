#http://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
from sphero import *

def getComm(host, port):
    i, o = socket.socket(), socket.socket()         # Create a socket object
    o.connect((host, port))
    print o.recv(1024)

    i.connect(('', port))
    i.listen(5)
    c, addr = i.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')

    return c, o

# Initialize Sphero
robot = core.Sphero("/dev/rfcomm0")
robot.connect()

# Initialize Socket
host = ''                   # Get local machine name
port = 12345                # Reserve a port for your service.
i, o = getComm(host,port)

# Initialize Commands
Commands = {"get_rgb"    : lambda x,y,z: robot.get_rgb(),
            "set_rgb"    : lambda x,y,z: robot.set_rgb(int(x),int(y),int(z),True),
            "ping"       : lambda x,y,z: robot.ping(),
            "set_heading": lambda x,y,z: robot.set_heading(int(x)),
            "set_speed"  : lambda x,y,z: robot.set_rotation_rate(int(x))}

while True:                   # Runs forever
    cmd = i.recv(1024)   # Receive the command
    v1  = i.recv(1024)   # Receive v1
    v2  = i.recv(1024)   # Receive v2
    v3  = i.recv(1024)   # Receive v3

    Commands[cmd](v1,v2,v3)
    o.send("Done!")

c.close()                # Close the connection
