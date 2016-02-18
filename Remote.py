#http://www.tutorialspoint.com/python/python_networking.htm

import socket               # Import socket module
import sphero

s = socket.socket()         # Create a socket object
host = ''                   # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print(s)
s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send('Thank you for connecting')
   c.close()                # Close the connection
