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

    if event.keysym == "F1":
        help_gameplay()

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
        Starts a new game
    """
    global board, statusMessage, playing
    board.reset()
    statusMessage["text"] = " "
    playing = True


def set_board_size(num_rows, num_cols):
    """
        Changes the size of the board to be num_rows x num_cols.
        Game is reset after the change.
    """
    global rows, columns, board, gameFrame, playing
    if num_rows != rows or num_cols != columns:
        rows = num_rows
        columns = num_cols
        board.clear()
        board = Board(gameFrame, rows, columns)
        statusMessage["text"] = " "
        playing = True


# Helper functions for menus
# Game menu functions
def game_change_size():
    """
        Opens interface to allow player to choose the size of the board
    """
    global rows, columns
    game_change_size_window = Toplevel(root, padx=10, pady=10)
    game_change_size_window.title("Change dimensions")
    game_change_size_window.transient(root)
    game_change_size_window.resizable(False, False)

    instruction_msg = "Enter the desired value below, valid values are integers between 2 and 9.\n" \
                      "Please consider that the game window can become quite big for large enough values."
    Label(game_change_size_window, text=instruction_msg, pady=10).pack()

    var_rows = IntVar(game_change_size_window)
    var_rows.set(rows)
    var_cols = IntVar(game_change_size_window)
    var_cols.set(columns)

    opt_frame = Frame(game_change_size_window, padx=5, pady=15)
    row_lb = Label(opt_frame, text="Rows: ", pady=5)
    row_lb.grid(row=0, column=0, sticky=E)
    row_sbox = Spinbox(opt_frame, from_=2, to=9, width=1, textvariable=var_rows)
    row_sbox.grid(row=0, column=1)
    col_lb = Label(opt_frame, text="Columns: ", pady=5)
    col_lb.grid(row=1, column=0, sticky=E)
    col_sbox = Spinbox(opt_frame, from_=2, to=9, width=1, textvariable=var_cols)
    col_sbox.grid(row=1, column=1)
    opt_frame.pack()

    def validate_size(new_rows, new_cols):
        """
            Helper function to validate player input
        """
        try:
            r = int(new_rows)
            c = int(new_cols)
            are_ints = True
        except ValueError:
            are_ints = False
        if are_ints:
            if (r >= 2 and r <= 9) and (c >= 2 and c <= 9):
                set_board_size(r, c)
                game_change_size_window.destroy()

    buttons_frame = Frame(game_change_size_window)
    Button(buttons_frame, text="OK", command=lambda: validate_size(var_rows.get(), var_cols.get())).grid(row=0, column=0)
    Button(buttons_frame, text="Cancel", command=game_change_size_window.destroy).grid(row=0, column=1)
    buttons_frame.pack()


# Help menu functions
def help_gameplay():
    """
        Shows window with information on how to play
    """
    msg_gameplay = "W or Up arrow: move tiles up\n" \
                   "S or Down arrow: move tiles down\n" \
                   "A or Left arrow: move tiles to the left\n" \
                   "D or Right arrow: move tiles to the right\n" \
                   "\nBoard starts with two tiles with values 2 or 4, you can\n" \
                   "slide tiles up, down, left or right with the keys listed above.\n" \
                   "Each time two tiles with the same value 'slide next to one another'\n" \
                   "they merge, with the final tile receiving the sum of both tiles.\n" \
                   "If no tile can move in the specified direction, move is ignored.\n" \
                   "If a move is processed, an empty tile receives a value (either 2 or 4).\n" \
                   "Your goal is to produce a tile with the value 2048.\n" \
                   "Game is over when either the goal is achieved or no more moves are possible."
    help_gameplay_window = Toplevel(root, padx=10, pady=10)
    help_gameplay_window.title("How to")
    help_gameplay_window.transient(root)
    help_gameplay_window.resizable(False, False)
    Label(help_gameplay_window, text=msg_gameplay, padx=25, pady=25).pack()
    Button(help_gameplay_window, text="OK", command=help_gameplay_window.destroy).pack()


def help_about():
    """
        Shows window with information about the program
    """
    msg_about = "Tkinter clone of the game 2048, made to explore this library's ins and outs."
    help_about_window = Toplevel(root, padx=10, pady=10)
    help_about_window.title("About")
    help_about_window.transient(root)
    help_about_window.resizable(False, False)
    Label(help_about_window, text=msg_about, padx=25, pady=25).pack()
    Button(help_about_window, text="Ok", command=help_about_window.destroy).pack()


# SETTING THINGS UP

# Game variables
rows = 4     # starts with a 4x4 board
columns = 4

# Main window
root = Tk()

# Menus
menu_bar = Menu(root)

# Game Menu
game_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Game", menu=game_menu)
game_menu.add_command(label="New game", command=new_game, underline=0)
game_menu.add_separator()
game_menu.add_command(label="Change board size", command=game_change_size, underline=0)

# Help Menu
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="How to play", command=help_gameplay, accelerator='F1', underline=0)
help_menu.add_command(label="About", command=help_about, underline=0)

# End of Menus
root.config(menu=menu_bar)

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
board = Board(gameFrame, rows, columns)

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
root.title("2048Tk")
root.mainloop()
