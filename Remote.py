#http://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
import sphero

# Initialize Sphero
robot = core.Sphero("/dev/rfcomm0")
robot.connect()

# Initialize Socket
net = socket.socket()         # Create a socket object
host = ''                   # Get local machine name
port = 12345                # Reserve a port for your service.
net.bind((host, port))        # Bind to the port

# Initialize Commands
Commands = {"get_rgb": lambda x,y: robot.get_rgb()}

net.listen(5)                 # Now wait for client connection.
while True:                   # Runs forever
    # Establish connection with client.
    c, addr = net.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')

    while True:                # Runs until broken by error
       try:
           cmd = s.recv(1024)   # Receive the command
           p1  = s.recv(1024)   # Receive p1
           p2  = s.recv(1024)   # Receive p2

           Commands[cmd](p1,p2)

       except:
           break

    c.close()                # Close the connection
