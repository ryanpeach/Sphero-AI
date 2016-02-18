#http://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
from sphero import *

# Initialize Sphero
robot = core.Sphero("/dev/rfcomm0")
robot.connect()

# Initialize Socket
net = socket.socket()         # Create a socket object
host = ''                   # Get local machine name
port = 12345                # Reserve a port for your service.
net.bind((host, port))        # Bind to the port

# Initialize Commands
Commands = {"get_rgb"    : lambda x,y,z: robot.get_rgb(),
            "set_rgb"    : lambda x,y,z: robot.set_rgb(int(x),int(y),int(z),True),
            "ping"       : lambda x,y,z: robot.ping(),
            "set_heading": lambda x,y,z: robot.set_heading(int(x)),
            "set_speed"  : lambda x,y,z: robot.set_rotation_rate(int(x))}

net.listen(5)                 # Now wait for client connection.
while True:                   # Runs forever
    # Establish connection with client.
    c, addr = net.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')

    while True:                # Runs until broken by error
       try:
           cmd = s.recv(1024)   # Receive the command
           v1  = s.recv(1024)   # Receive v1
           v2  = s.recv(1024)   # Receive v2
           v3  = s.recv(1024)   # Receive v3

           Commands[cmd](v1,v2,v3)
           c.send("Done!")

       except:
           break

    c.close()                # Close the connection
