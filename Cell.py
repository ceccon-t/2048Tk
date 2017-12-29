try:
    from Tkinter import *  # Python 2
except ImportError:
    try:
        from tkinter import *  # Python 3
    except ImportError:
        raise ImportError("This program requires Tkinter, please make sure you have it installed.")

_CELL_COLORS = {
        2: "linen",
        4: "antique white",
        8: "light salmon",
        16: "dark salmon",
        32: "salmon",
        64: "tomato",
        128: "pale goldenrod",
        256: "light goldenrod",
        512: "khaki",
        1024: "gold",
        2048: "yellow"
}


class Cell:
    def __init__(self, master, row, col):
        self.value = 0
        self.font = ("Verdana", 15)
        self.fr = Frame(master, padx=5, pady=5)
        self.lb = Label(self.fr, width=8, height=4, bg='gray', text="", font=self.font)
        self.lb.pack()
        self.fr.grid(row=row, column=col)

    def get_value(self):
        """
            Returns the value of the cell
        """
        return self.value

    def set_value(self, val):
        """
            Changes the value of the cell to be param val and updates it visually
        """
        self.value = val
        if val != 0:
            self.lb.config(text=str(self.value))
        else:
            self.lb.config(text="")
        if val in _CELL_COLORS:
            self.lb.config(bg=_CELL_COLORS[val])
        else:
            self.lb.config(bg="gray")
        if val > 4 and val < 128:
            self.lb.config(fg="white")
        else:
            self.lb.config(fg="black")
