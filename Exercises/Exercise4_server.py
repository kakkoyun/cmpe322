import os
import socket
import threading
import io
import random
import sys
import datetime


def service(readsocket):
    commad_no = 0
    textWrapper = readsocket.makefile(mode="rw")
    while True:
        try:
            line = textWrapper.readline().strip()
            commad_no += 1
            print("Recieved (%d):" % commad_no, line)
            if line == "zaman":
                textWrapper.write(str(datetime.datetime.now()) + "\n")
            elif line == "rasgele":
                textWrapper.write(str(random.random()) + "\n")
            else:
                textWrapper.write("bilinmeyen komut! " + line + "\n")
            textWrapper.flush()
        except:
            print("Hata oluştu !!!: ", sys.exc_info())

serversocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
serversocket.bind("/tmp/server")
serversocket.listen(5)
while True:
    clientConn, clientAddr = serversocket.accept()
    print("Client connection accepted :", clientAddr)
    t = threading.Thread(target=service, args=[clientConn])
    t.setDaemon(True)
    t.start()
