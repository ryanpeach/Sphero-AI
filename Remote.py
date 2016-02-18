#http://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
from sphero import *

def getComm(host, portI, portO):
    i, o = socket.socket(), socket.socket()         # Create a socket object

    i.bind(('', portI))
    i.listen(5)
    c, addr = i.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')

    o.connect((host,portO))
    print o.recv(1024)

    return c, o

# Initialize Sphero
robot = core.Sphero("/dev/rfcomm0")
robot.connect()

# Initialize Socket
host = '192.168.0.103'                   # Get local machine name
portI, portO = 12345, 23451                # Reserve a port for your service.
i, o = getComm(host,portI,portO)

# Initialize Commands
Commands = {"get_rgb"    : lambda x,y,z: robot.get_rgb(),
            "set_rgb"    : lambda x,y,z: robot.set_rgb(int(x),int(y),int(z),True),
            "ping"       : lambda x,y,z: robot.ping(),
            "set_heading": lambda x,y,z: robot.set_heading(int(x)),
            "set_speed"  : lambda x,y,z: robot.set_rotation_rate(int(x))}

while True:                   # Runs forever
    cmd = i.recv(1024)   # Receive the command
    print(cmd)    
    cmd,v1,v2,v3 = cmd.replace(' ','').split(',') 
    print(cmd,v1,v2,v3)

    Commands[cmd](v1,v2,v3)
    o.send("Done!")

c.close()                # Close the connection
