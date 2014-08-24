#!/usr/bin/python

import socket
import sys
import threading
import thread

HELP = """
Commands:

- help : see this message whenever you want.

- everyone >> |message| : Send a message to everyone

- |nickname| >> |message| : Send a message to individual.

- random >> |message| : Send a message to random individual.

- terminate : Close service.

- users : Get connected users
"""


def get_arguments():
    """
    Controls command line arguments and returns
    serverAdress and clientName which had been read from command line.
    """
    if (len(sys.argv) <= 2):
        print("Error: Invalid number of arguments." +
              "Two argument expected: Server address and nickname !")
        sys.exit(1)
    try:
        serverAdress = sys.argv[1]
        clientName = sys.argv[2]
        return (serverAdress, clientName)
    except:
        print("Error :", sys.exc_info())
        sys.exit(1)


def connect_to_service(address, name):
    """
    Try to connet to chat service with name,
    waits for positive message otherwise gives error.
    """
    # try:
        # Create client socket.
        clientsocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        # Connect to server.
        clientsocket.connect(address)
        clientsocket.send("name>>" + name)
        # Wait for response.
        response = clientsocket.recv(2048).strip()
        response = response.split("|")
        if(response[0].strip() == "accept"):
            result = True
            message = "Welcome to chat service, %s" % response[1].strip()
        else:
            result = False
            message = "Cannot connect to server ! Try again later."
        return(result, message, clientsocket)
    except:
        print("Error :", sys.exc_info())
        sys.exit(1)


def start_service(clientsocket):
    """
    Routine for listening and sending message.
    """
    sender = threading.Thread(target=receive_service, args=[clientsocket])
    sender.setDaemon(True)

    receiver = threading.Thread(target=send_service, args=[clientsocket])
    receiver.setDaemon(True)

    sender.start()
    receiver.start()

    # To handle interrupts for threads.
    try:
        while True:
            sender.join(100)
            receiver.join(150)
    except (KeyboardInterrupt, SystemExit):
        print("\n! Received interrupt, quitting threads.\n")
    except:
        print(" Client exit! ")
        socket.close()


def send_service(clientsocket):
    while True:
        msg = raw_input("=>> ")
        # Listen command.
        if msg == "terminate":
            thread.interrupt_main()
            clientsocket.close()
            sys.exit(1)
            break
        elif msg == "help":
            print(HELP)
            continue
        elif len(msg.split(">>")) > 2:
            print("Message cannot include '>>' !")
            continue
        else:
            # Send Message.
            if (msg != '\n'):
                clientsocket.send('%s' % msg)
            continue


def receive_service(clientsocket):
    "Receive data from other clients connected to server"
    while True:
        try:
            # Recieve Message.
            line = clientsocket.recv(2048)
            if (line != '\n'):
                print("\n<<= %s" % line)
            if not line:
                print("Server closed connection, thread exiting.")
                thread.interrupt_main()
                break
        except:
            print("Error, thread exiting.")()
            thread.interrupt_main()
            clientsocket.close()
            break
            sys.exit(1)


def main():
    address, name = get_arguments()
    result, message, socket = connect_to_service(address, name)
    if(result):
        print(HELP)
        print(message)
        start_service(socket)
    else:
        print(message)
        sys.exit(1)

if __name__ == '__main__':
    main()
