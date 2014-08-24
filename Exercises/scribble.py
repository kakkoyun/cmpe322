#!/usr/bin/python3
"""
A simple scribble program in Python which can draw on the canvas along mouse drags.
See http://www.pythonware.com/library/tkinter/introduction/
Author: Mehmet Gencer
"""
import sys
from tkinter import *
x,y=None,None
count=0
def quit(event):
    sys.exit()

def drag(event):
    global x,y, count
    newx,newy=event.x,event.y
    if x is None:
        x,y=newx,newy
        return
    count+=1
    sys.stdout.write("\revent count %d"%count)
    c.create_line(((x,y),(newx,newy)))
    x,y=newx,newy

def drag_end(event):
    global x,y
    x,y=None,None

root = Tk()
c=Canvas(root)
c.bind("<B1-Motion>",drag)
c.bind("<ButtonRelease-1>",drag_end)
c.pack()
b=Button(root,text="Quit")
b.pack()
b.bind("<Button-1>",quit)
root.mainloop()
