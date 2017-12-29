import random

try:
    from Tkinter import *  # Python 2
except ImportError:
    try:
        from tkinter import *  # Python 3
    except ImportError:
        raise ImportError("This program requires Tkinter, please make sure you have it installed.")

from Cell import *

# Used to be an Enum, but changed to constants for Python 2 compatibility
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Steps to walk through board in each specific direction while setting list of values in the format
# expected by the merge method
STEPS = {
    UP: (1, 0),
    DOWN: (-1, 0),
    LEFT: (0, 1),
    RIGHT: (0, -1)
}


class Board:
    def __init__(self, master, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.hasReached2048 = False
        self.initials = {
            UP: [(0, col) for col in range(self.width)],
            DOWN: [(self.height - 1, col) for col in range(self.width)],
            LEFT: [(row, 0) for row in range(self.height)],
            RIGHT: [(row, self.width - 1) for row in range(self.height)]
        }
        self.fr = Frame(master)
        self.cells = []
        self.reset()
        self.fr.pack()

    def reset(self):
        """
            Resets the board to be empty except for two initial cells.
        """
        self.hasReached2048 = False
        self.cells = [ [Cell(self.fr, row, col) for col in range(self.width)] for row in range(self.height) ]
        self.new_cell()
        self.new_cell()

    def new_cell(self):
        """
            Generates a new cell, with 90% chances of having a value of 2 and 10% chances for 4
        """
        ok = False
        while not ok:
            row = random.randrange(0, self.height)
            col = random.randrange(0, self.width)
            if self.get_cell(row, col) == 0:
                ok = True
        if random.randint(0, 9) == 9:
            val = 4
        else:
            val = 2
        self.set_cell(row, col, val)

    def get_cell(self, row, col):
        """
            Gets the value of the cell at given position
        """
        return self.cells[row][col].get_value()

    def set_cell(self, row, col, val):
        """
            Sets the value of the cell at given position to be val
        """
        self.cells[row][col].set_value(val)

    def merge(self, line):
        """
            Processes a movement on a single row/column of cells
            Receives a list (param line) consisting of the values of the cells on the given row/column,
             set up so that the leftmost position (index 0) is the first destination on the direction of
             the desired movement (i.e. while moving a column DOWN, index 0 would be the value of the cell
             on index height-1 of given column [col, height-1]; likewise, moving a row LEFT means index 0 is the value of
             cell on index 0 of given row [row,0]
            Proceeds to move everything towards the start of the list, merging cells when possible
            Returns the final list, which represents the new state of given row/column after movement (using same
             setting of the input, with direction of movement as index 0)
        """
        result = [0 for e in line]  # initiates a zeroed list of same length as the input
        pos_result = 0  # keeps track of index of the last number added to the new list
        merged = False  # flag to avoid merging same element twice
        for i in range(len(line)):
            if line[i] != 0:
                if pos_result > 0 and line[i] == result[pos_result - 1] and not merged:
                    result[pos_result - 1] = 2 * line[i]
                    merged = True
                else:
                    result[pos_result] = line[i]
                    pos_result += 1
                    merged = False
        return result

    def move(self, direction):
        """
            Tries to move all cells in the given direction and adds a new cell if any did move
            Param direction is one of UP, DOWN, RIGHT, LEFT - constants created on this file
        """
        cells_moved = False  # if a cell is moved needs to create a new one

        # sets boundaries of loop (board not necessarily is square)
        if direction == UP or direction == DOWN:
            bound = self.height  # will stop at len of ROWS - 1
        else:
            bound = self.width  # will stop at len of COLS - 1

        for initial in self.initials[direction]:
            temp_line = []  # temp line with values to be sent to merge method
            for i in range(bound):
                row = initial[0] + (i * STEPS[direction][0])
                col = initial[1] + (i * STEPS[direction][1])
                val = self.get_cell(row, col)
                temp_line.append(val)
            new_line = self.merge(temp_line)  # processes the movement
            for i in range(bound):  # sets processed line back on the board
                row = initial[0] + (i * STEPS[direction][0])
                col = initial[1] + (i * STEPS[direction][1])
                if new_line[i] != self.get_cell(row, col):  # something has moved
                    cells_moved = True
                self.set_cell(row, col, new_line[i])  # sets the value on the cell
                if new_line[i] == 2048:
                    self.hasReached2048 = True
        if cells_moved:
            self.new_cell()

    def is_valid_move(self, direction):
        """
            Checks if a movement in the given direction is valid by
            calculating the new state of the board and checking if
            anything has changed. Logic mimics that of move method
        """
        # sets boundaries of loop (board not necessarily is square)
        if direction == UP or direction == DOWN:
            bound = self.height  # will stop at len of ROWS - 1
        else:
            bound = self.width  # will stop at len of COLS - 1

        for initial in self.initials[direction]:
            temp_line = []  # temp line with values to be sent to merge method
            for i in range(bound):
                row = initial[0] + (i * STEPS[direction][0])
                col = initial[1] + (i * STEPS[direction][1])
                val = self.get_cell(row, col)
                temp_line.append(val)
            new_line = self.merge(temp_line)  # gets new state
            for i in range(bound):  # goes through each cell checking if something has moved
                row = initial[0] + (i * STEPS[direction][0])
                col = initial[1] + (i * STEPS[direction][1])
                if new_line[i] != self.get_cell(row, col):  # something has moved
                    return True
        return False

    def has_valid_move(self):
        """
            Checks if board still has a valid move
        """
        return self.is_valid_move(UP) or self.is_valid_move(DOWN) or self.is_valid_move(RIGHT) or self.is_valid_move(LEFT)



