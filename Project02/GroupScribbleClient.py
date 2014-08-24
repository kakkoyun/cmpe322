#!/usr/bin/python
#-*- coding: utf-8 -*-

# CMPE 322 - Project 02
# Author: Gizem Gür and Kemal Akkoyun
# A Client program for Group Scribble.

import os
import select
import socket
import sys
import threading
import thread
import GroupScribbleGUI


class Client:

    HELP = """
    Commands:

    - HELP = See this message whenever you want !

    - GROUPS = See active 'named' groups.

    - MYGROUPS = See groups that you joined.

    - JOIN : |group_name| = Join an existing group or create a new one.

    - EXIT = Close service.

    - USERS = Get connected users of groups.
    """

    active_groups = {}
    gui_connection_list = []

    def __init__(self, address, port, name):
        self.network_server_address = address
        self.network_server_port = port
        self.nickname = name
        self.gui_server_address = ("/tmp/%s" % self.nickname)

        self.network_client_socket = socket.socket(socket.AF_INET,
                                                   socket.SOCK_STREAM)
        self.gui_server_socket = socket.socket(socket.AF_UNIX,
                                               socket.SOCK_STREAM, 0)
        self.gui_connection_list.append(self.gui_server_socket)

    def connect_to_server(self):
        """
        Try to connet to chat service with name,
        waits for positive message otherwise gives error.
        """
        try:
            # Connect to server.
            self.network_client_socket.connect((self.network_server_address,
                                                self.network_server_port))
            self.network_client_socket.send(self.nickname)
            # Wait for response.
            response = self.network_client_socket.recv(2048).strip()
            response = response.split("|")
            if(response[0].strip() == "accept"):
                message = ("Welcome to scribble, %s\n" % response[1].strip())
                self.initialize_gui_server()
            else:
                message = "Cannot connect to server ! Try again later."
            print(message)
        except:
            print("Server Connection Error :", sys.exc_info())
            self.quit()

    def initialize_gui_server(self):
        try:
            self.gui_server_socket.bind(self.gui_server_address)
            # Allow upto 20 connection of gui groups.
            self.gui_server_socket.listen(20)
        except:
            print("GUI Server Error :", sys.exc_info())
            self.quit()

    def send(self, msg):
        # Send Message.
        if (msg != '\n'):
            self.network_client_socket.send('%s' % msg)

    def send_service(self):
        while True:
            msg = raw_input("=>> ")
            # Listen command.
            if msg == "EXIT":
                self.send("EXIT")
                thread.interrupt_main()
                self.quit()
                break
            elif msg == "MYGROUPS":
                print(self.active_groups.keys)
            elif msg == "HELP":
                print(self.HELP)
            else:
                self.send(msg)

    def receive_service(self):
        # Receive data from server.
        while True:
            try:
                # Recieve Message.
                line = self.network_client_socket.recv(2048)
                if (line != '\n'):
                    if((len(line.split(":")) >= 2) and
                       (line.split(":")[0].strip().startswith("LINE"))):
                        self.gui_send_service(line)
                    elif((len(line.split(":")) == 2) and
                         (line.split(":")[0].strip() == "JOINED")):
                        self.create_group_gui(line.split(":")[1].strip())
                    else:
                        print("\n %s" % line)

                if not line:
                    print("Server closed connection, thread exiting.")
                    thread.interrupt_main()
                    self.quit()
                    break
            except:
                print("Recieve Error: Thread exiting.")
                thread.interrupt_main()
                self.quit()
                break

    def gui_service(self):
        # Wait for gui client connection.
        print('gui service routine started!')
        while True:
            # Get the list sockets which are ready to be read through select
            read_sockets, write_sockets, error_sockets = select.select(self.gui_connection_list, [], [])
            for socket in read_sockets:
                if socket == self.gui_server_socket:
                    sockfd, addr = self.gui_server_socket.accept()
                    # Add new connections socket to connection queue.
                    self.gui_connection_list.append(sockfd)
                    print("Connection accepted")
                else:
                    try:
                        line = socket.recv(1024).strip()
                    except:
                        print("Gui group %s is closed" % addr)
                        group_name = self.get_gui_group_name(socket)
                        self.gui_connection_list.remove(socket)
                        socket.close()
                        del self.active_groups[group_name]
                        continue
                    if line:
                        self.gui_service_handler(line)

    def start_services(self):
        # Routine for listening and sending message.
        self.sender = threading.Thread(target=self.send_service)
        self.sender.setDaemon(True)

        self.receiver = threading.Thread(target=self.receive_service)
        self.receiver.setDaemon(True)

        self.gui_server = threading.Thread(target=self.gui_service)
        self.gui_server.setDaemon(True)

        self.sender.start()
        self.receiver.start()
        self.gui_server.start()

        # To handle interrupts for threads.
        try:
            while True:
                self.sender.join(100)
                self.receiver.join(100)
                self.gui_server.join(100)
        except (KeyboardInterrupt, SystemExit):
            print("\n! Received interrupt, quitting threads.\n")
            self.quit()
        except:
            print(" Client exit! ")
            self.quit()

    def create_group_gui(self, group_name):
        print("Creating GUI group...")
        try:
            group = GroupScribbleGUI.Scribble(self.gui_server_address, group_name)
            print("GUI created!")
            # Register group's socket to active group list.
            self.active_groups[group_name] = group.client_socket
            print("Active Groups added")
        except:
            print("Create gui", sys.exc_info())

    def get_gui_group_name(self, socket):
        for name, client_socket in self.active_groups.iteritems():
            if client_socket == socket:
                return name

    def gui_service_handler(self, line):
        if (line != '\n'):
            self.o.send(line)

    def gui_send_service(self, line):
        response = line.split(":")
        if(response[0] == "LINE"):
            group = response[5]
            self.send_gui(group, line)
        elif(response[0] == "LINE_END"):
            group = response[1]
            self.send_gui(group, line)
            print("get a line end!!!!")

    def send_gui(self, group, line):
        gui_socket_of_group = self.active_groups[group]
        gui_socket_of_group.send(line)

    def quit(self):
        os.remove(self.gui_server_address)
        self.gui_server_socket.close()
        self.network_client_socket.close()
        sys.exit(1)


def get_commandline_arguments():
    """
    Controls command line arguments and returns
    server_adress, server_port and client_nickname which had
    been read from command line.
    """
    if (len(sys.argv) <= 3):
        print("Error: Invalid number of arguments." +
              "Three argument expected: Server address," +
              "server port and nickname !")
        sys.exit(1)
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        client_nickname = sys.argv[3]
        return (server_address, server_port, client_nickname)
    except:
        print("Argument Error :", sys.exc_info())
        sys.exit(1)


def main():
    try:
        address, port, nickname = get_commandline_arguments()
        client = Client(address, port, nickname)
        client.connect_to_server()
        print(client.HELP)
        client.start_services()
    except:
        print("ERROR :", sys.exc_info())
        sys.exit(1)

if __name__ == '__main__':
    main()
