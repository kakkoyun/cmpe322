import socket
import os
import threading


def reader(name, readsocket, size=10):
    while True:
        data, address = readsocket.recv(size)
        print(name + "read from " + address, ", message :", data)

socket1, socket2 = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
if os.fork() == 0:
    socket1.bind("/tmp/A")
    t = threading.Thread(target=reader, args=("A", socket1, 6))
    t.setDaemon(True)
    t.start()
    socket1.sendto(b"Hello1", "/tmp/B")
    socket1.sendto(b"Hello2", "/tmp/B")
    t.join(timeout=1)
    print("BYE! Please remove /tmp/A")
else:
    socket2.bind("/tmp/B")
    t = threading.Thread(target=reader, args=("B", socket2, 6))
    t.setDaemon(True)
    t.start()
    socket2.sendto(b"hello1", "/tmp/A")
    socket2.sendto(b"hello2", "/tmp/A")
    t.join(timeout=1)
    print("BYE! Please remove /tmp/B")
