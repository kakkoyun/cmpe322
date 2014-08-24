#!/usr/bin/python
#-*- coding: utf-8 -*-

# CMPE 322 - Project 02
# Author: Gizem Gür and Kemal Akkoyun
# A simple scribble program in Python which can draw on the canvas along mouse drags.
# See http://www.pythonware.com/library/tkinter/introduction/

import socket
import sys
import thread
import threading
import Tkinter


class Scribble(threading.Thread):

    x, y = None, None
    count = 0

    def __init__(self, address, name):

        threading.Thread.__init__(self)

        self.gui_server_address = address
        self.group_name = name
        self.connect_to_service()

        self.start_service()
        self.start()

    def run(self):

        master = Tkinter.Tk()
        self.title = Tkinter.Label(master,
                                   text=("Group Scribble of %s"
                                         % self.group_name))
        self.title.pack()

        self.canvas = Tkinter.Canvas(master)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.drag_end)
        self.canvas.pack()

        self.button = Tkinter.Button(master, text="Quit")
        self.button.bind("<Button-1>", quit)
        self.button.pack()

        # Status label
        self.status_text = Tkinter.StringVar()
        self.status_text.set('Status Message')
        self.status = Tkinter.Label(master,
                                    textvariable=self.status_text)
        self.status.pack()

        master.protocol("WM_DELETE_WINDOW", self.exit)
        master.mainloop()

    def drag(self, event):
        newx, newy = event.x, event.y
        if self.x is None:
            self.x, self.y = newx, newy
            return
        self.count += 1
        self.draw_line(self.x, self.y, newx, newy)
        self.send_line(self.x, self.y, newx, newy)
        self.x, self.y = newx, newy

    def drag_end(self, event):
        self.line_end()
        self.client_socket.send("LINE_END:%s" % self.group_name)

    def send_line(self, fx, fy, tx, ty):
        self.client_socket.send("LINE:%s:%s:%s:%s:%s" %
                                (fx, fy, tx, ty, self.group_name))

    def draw_line(self, fx, fy, tx, ty):
        self.canvas.create_line(((fx, fy), (tx, ty)))

    def line_end(self):
        self.x, self.y = None, None

    def receive_service(self):
        while True:
            try:
                line = self.client_socket.recv(2048).strip()
                if (line != '\n'):
                    response = line.split(":")
                    if(response[0] == "LINE"):
                        x1 = response[1]
                        y1 = response[2]
                        x2 = response[3]
                        y2 = response[4]
                        self.draw_line(x1, y1, x2, y2)
                    elif(response[0] == "LINE_END"):
                        self.line_end()
                if not line:
                    self.client_socket.send("NO LINE RECEIVED:%s" % self.group_name)
                    thread.interrupt_main()
                    self.exit()
                    break
            except:
                self.client_socket.send("RECEIVE ERROR:%s" % self.group_name)
                thread.interrupt_main()
                self.exit()
                break

    def connect_to_service(self):
        try:
            self.client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
            self.client_socket.connect(self.gui_server_address)
        except:
            self.exit()

    def start_service(self):
        """
        Routine for listening lines as messages.
        """
        self.receiver = threading.Thread(target=self.receive_service)
        self.receiver.setDaemon(True)
        self.receiver.start()

    def quit(self, event):
        self.exit()

    def exit(self):
        self.client_socket.send("GUI EXIT:%s" % self.group_name)
        self.client_socket.close()
        thread.interrupt_main()
        sys.exit(0)
