#!/usr/bin/python

#-*- coding: utf8-*-#

import socket
import threading
import random
import sys
import datetime
import os

# List of connected users.
USERS = {}


def service_handler(socket):
    commad_no = 0
    line = socket.recv(2048).strip()
    print("Recieved (%d): %s\n" % (commad_no, line))
    if (line.startswith("name")):
        line = line.split(">>")
        sender = line[1].strip()
        USERS[sender] = socket
        socket.send("accept|%s" % sender)
    while True:
        line = socket.recv(2048).strip()
        commad_no += 1
        print("Recieved (%d): %s\n" % (commad_no, line))
        if line == "\n":
            continue
        elif line == "time":
            socket.send(str(datetime.datetime.now()))
            print(str(datetime.datetime.now()))
        elif line == "users":
            user_list = "Connected Users:\n"
            for name in USERS:
                user_list += "%s\n" % name
            socket.send(user_list)
            print(user_list)
        elif len(line.split(">>")) >= 2:
            line = line.split(">>")
            command = line[0].strip()
            argument = line[1].strip()
            if command == "everyone":
                for reciever, clientsocket in USERS.iteritems():
                    clientsocket.send("Broadcast | %s says : %s " % (sender, argument))
            elif command == "random":
                clientsocket = random.choice(USERS.values())
                clientsocket.send("Private | %s says : %s" % (sender, argument))
            else:
                if (command in USERS):
                    clientsocket = USERS[command]
                    clientsocket.send("Private | %s says : %s" % (sender, argument))
                    print("%s %s" % (command, argument))
                else:
                    socket.send("User not connected!")
                    print("User not connected!")
        else:
            print(line)
            if (line != '\n'):
                socket.send("Unknown command : %s " % line)


def get_arguments():
    """
    Controls command line arguments and returns
    serverAdress which had been read from command line.
    """
    if (len(sys.argv) < 2):
        print("Error: Invalid number of arguments. " +
              "Argument expected: Server address !")
        sys.exit(1)
    try:
        serverAdress = sys.argv[1]
        return serverAdress
    except:
        print("Error :", sys.exc_info())
        sys.exit(1)


def initialize_service(socketAdress):
    try:
        # Create server socket.
        serversocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        serversocket.bind(socketAdress)
        serversocket.listen(20)
        return serversocket
    except:
        print("Error :", sys.exc_info())
        sys.exit(1)


def run_service(serversocket):
    # Wait for client connection.
    while True:
        clientConnection, clientAddress = serversocket.accept()
        print("Client connection accepted at %s, from %s"
              % (str(datetime.datetime.now()), str(clientAddress)))
        t = threading.Thread(target=service_handler, args=[clientConnection])
        t.setDaemon(True)
        t.start()


def main():
    try:
        address = get_arguments()
        serversocket = initialize_service(address)
        run_service(serversocket)
    except KeyboardInterrupt:
        print(" KeyboardInterrupt. Exit!")
        os.remove(address)
        serversocket.close()
        sys.exit(0)


if __name__ == '__main__':
    main()
