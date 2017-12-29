try:
    from Tkinter import *  # Python 2
except ImportError:
    try:
        from tkinter import *  # Python 3
    except ImportError:
        raise ImportError("This program requires Tkinter, please make sure you have it installed.")

from Board import *


# FUNCTIONS

def keydown(event):
    """
        Processes user input
    """
    global board, playing, statusMessage
    if playing:
        if event.char == 'w' or event.keysym == "Up":
            board.move(UP)
        if event.char == 's' or event.keysym == "Down":
            board.move(DOWN)
        if event.char == 'a' or event.keysym == "Left":
            board.move(LEFT)
        if event.char == 'd' or event.keysym == "Right":
            board.move(RIGHT)

        if board.has_won():
            playing = False
            statusMessage["text"] = "YOU WON!"
        if playing and not board.has_valid_move():
            playing = False
            statusMessage["text"] = "There are no more valid movements. Try again!"

    # TODO: Decide if Esc should close the game or restart it
    # if event.keysym == 'Escape':
    #     new_game()


def new_game():
    """
        Start a new game
    """
    global board, statusMessage, playing
    board.reset()
    statusMessage["text"] = " "
    playing = True


# SETTING THINGS UP

# Main window
root = Tk()

# Base frame for everything
topFrame = Frame(root, padx=10, pady=10)

# Frames for each section
titleFrame = Frame(topFrame)
gameFrame = Frame(topFrame)
interactionFrame = Frame(topFrame)

# Title section
titleFontSpec = '-family "Times New Roman" -size 35 -weight bold'
titleLabel = Label(titleFrame, text="2048", font=titleFontSpec, pady=30)
titleLabel.pack()

# Game section
board = Board(gameFrame, 4, 4)

# Interaction section
statusMessage = Label(interactionFrame, text=" ", pady=30)
statusMessage.pack()
newGameButton = Button(interactionFrame, text="New game", command=new_game)
newGameButton.pack()

# Pushing frames into display
titleFrame.pack()
gameFrame.pack()
interactionFrame.pack()

topFrame.pack()

# Bindings
root.bind('<Key>', keydown)

# Initialization of game
playing = True


# START GAME

root.geometry("+400+75")
root.mainloop()
