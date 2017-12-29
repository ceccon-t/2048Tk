try:
    from Tkinter import *  # Python 2
except ImportError:
    try:
        from tkinter import *  # Python 3
    except ImportError:
        raise ImportError("This program requires Tkinter, please make sure you have it installed.")

from Board import *


def keydown(event):
    global board
    if event.char == 'w' or event.keysym == "Up":
        board.move(UP)
    if event.char == 's' or event.keysym == "Down":
        board.move(DOWN)
    if event.char == 'a' or event.keysym == "Left":
        board.move(LEFT)
    if event.char == 'd' or event.keysym == "Right":
        board.move(RIGHT)
    if event.keysym == 'Escape':
        board.reset()



root = Tk()

board = Board(root, 4, 4)

root.bind('<Key>', keydown)

root.geometry("+400+75")
root.mainloop()