import os
import socket

socket1, socket2 = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
if os.fork() == 0:
    socket1.send(b'Hello')
    print("Child Reading:", socket1.recv(10))
else:
    print("Parent Reading:", socket2.recv(5))
    socket2.send(b'Hello back')
