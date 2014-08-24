# !/usr/bin/python3
import socket
import os
import threading
import io

clientsocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
clientsocket.connect("/tmp/server")
textWrapper = clientsocket.makefile(mode="rw")
while True:
    tmp = input("Enter Command: ")
    if tmp == "yeter":
        clientsocket.close()
        break
    textWrapper.write(tmp + "\n")
    textWrapper.flush()
    print("Reply: ", textWrapper.readline())
