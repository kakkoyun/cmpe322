import socket
import os
import threading


def reader(name, readsocket, size=10):
    while True:
        print(name + "reading:", readsocket.recv(size))

socket1, socket2 = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
if os.fork() == 0:
    t = threading.Thread(target=reader, args=("A", socket1, 6))
    t.setDaemon(True)
    t.start()
    socket1.send(b"Hello1")
    socket2.send(b"Hello2")
    t.join(timeout=1)
else:
    t = threading.Thread(target=reader, args=("B", socket2, 6))
    t.setDaemon(True)
    t.start()
    socket2.send(b"hello1")
    socket2.send(b"hello2")
    t.join(timeout=1)
