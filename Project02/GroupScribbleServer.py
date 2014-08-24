#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import socket
import select

# CMPE 322 - Project 02
# Author: Gizem Gür and Kemal Akkoyun
# A Server program for Group Scribble.


class Server():
    group_list = {}
    connection_list = []
    user_list = {}

    def is_group_exists(self, group):
        for group_name in self.group_list.keys():
            if group_name == group:
                return True
        return False

    def join_group(self, group, sock_name):
        for group_name in self.group_list.keys():
            if group_name == group:
                self.group_list[group_name].append(sock_name)
                return

    def create_group(self, group_name):
        self.group_list[group_name] = []

    def remove_from_groups(self, sock_name):
        for group, socks in self.group_list.iteritems():
            if sock_name in socks:
                socks.remove(sock_name)
                if not socks:
                    del self.group_list[group]

    def send_specific_group(self, group, client, message):
        for group_name, clients in self.group_list.iteritems():
            if group_name == group:
                for client_name in clients:
                    if client_name != client:
                        self.user_list[client_name].send(message)
                    else:
                        print("heeeeeeey")
                break

    def send_group(self, sock_name, message):
        for group, socks in self.group_list.iteritems():
            if sock_name in socks:
                self.send_specific_group(group, sock_name, message)

    def find_socket(self, user_name):
        return self.user_list[user_name]

    def send_everyone(self, user_name, message):
        for user in self.user_list:
            if user_name:
                if user == user_name:
                    continue
                else:
                    self.user_list[user].send("from-"+user_name+":"+message)
            else:
                self.user_list[user].send(message)
        return

    def get_client_name(self, sock):
        for name, client_socket in self.user_list.iteritems():
            if client_socket == sock:
                return name


def response_to_line(server, sock, sock_name, line):

    if line == "EXIT":
        server.send_group(sock_name, "Client %s exits. \n" % sock_name)
        print("Client %s quits" % sock_name)
        sock.close()
        server.connection_list.remove(sock)
        del server.user_list[sock_name]
        server.remove_from_groups(sock_name)
    elif line == "GROUPS":
        group_list = server.group_list.keys()
        sock.send("Available groups \n%s" % group_list)
    elif line == "USERS":
        sock.send("Group\tUser List\n")
        for group_name, users in server.group_list.iteritems():
            sock.send("%s\t%s\n" % (group_name, users))
    else:
        print("Recieved message from %s : %s" % (sock_name, line))
        command_message = line.split(":")
        if len(command_message) == 2:
            command = command_message[0]
            group = command_message[1]
            if command == "QUIT":
                server.send_specific_group(group, sock_name, "Client %s left the group." % sock_name)
                server.remove_from_group(group, sock_name)
            elif command == "JOIN":
                is_group = server.is_group_exists(group)
                if is_group:
                    server.join_group(group, sock_name)
                else:
                    server.create_group(group)
                    server.join_group(group, sock_name)
                sock.send("JOINED:%s" % group)
                print("JOINED:%s" % group)
            elif command == "LINE_END":
                server.send_specific_group(group, sock_name, "LINE_END:%s" % group)
                print("sadasdasdas")
            else:
                sock.send("Not a valid command. Please see the valid commands with HELP")
        elif len(command_message) == 6:
            try:
                group = command_message[5]
                server.send_specific_group(group, sock_name, line)
            except:
                sock.send("Not a valid command. Please see the valid commands with HELP")
        else:
            sock.send("Not a valid command. Please see the valid commands with HELP")


def run_server(server, server_socket):
    while True:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(server.connection_list, [], [])

        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                server.connection_list.append(sockfd)
                print("Client connected")
                while True:
                    user_name = sockfd.recv(1024)
                    if not user_name == "\n":
                        break
                server.user_list[user_name] = sockfd
                sockfd.send("accept|%s" % user_name)
                server.send_everyone("", ("Client %s connected." % user_name))
            else:
                try:
                    line = sock.recv(1024)
                    sock_name = server.get_client_name(sock)
                except:
                    server.send_group(sock_name, "Client %s is offline. \n" % sock_name)
                    print("Client %s is offline" % addr)
                    sock.close()
                    server.connection_list.remove(sock)
                    del server.user_list[sock_name]
                    server.remove_from_groups(sock_name)
                    continue

                if line:
                    response_to_line(server, sock, sock_name, line)


def get_commandline_arguments():
    """
    Controls command line arguments and returns
    server_adress, server_port.
    """
    if (len(sys.argv) <= 2):
        print("Error: Invalid number of arguments." +
              "Three argument expected: Server address," +
              "server port !")
        sys.exit(1)
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        return (server_address, server_port)
    except:
        print("Argument Error :", sys.exc_info())
        sys.exit(1)


def main():
    print "Runned"
    address, port = get_commandline_arguments()
    """
    NOTE TO GIZEM !!!!
    PLEASE MAKE THIS CLASS INSTANCE METHOD OF SERVER CLASS
    In order to maintain and keep convention !!
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(10)

    server = Server()
    print "Created Server"
    server.connection_list.append(server_socket)

    try:
        run_server(server, server_socket)
    except:
        print("ERROR :", sys.exc_info())
        server_socket.close()
        sys.exit(1)

if __name__ == '__main__':
    main()
