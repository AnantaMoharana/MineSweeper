import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)



class Cell:
    def __init__(self, isMine, surroundingMines):
        self.isMine = isMine
        self.surroundingMines = surroundingMines


    def setSurroundingMines(self, m):
        self.surroundingMines = m



# mineGrid is a 2D matrix of Cells, where we can also store future information

class MineGrid:

    def __init__(self, d, n):
        self.dimension = d
        self.probability = n
        self.mineGrid = []

        # Instantiate our minesweeper grid with 0's
        for i in range(self.dimension):
            col = []
            for j in range(self.dimension):
                col.append(Cell(False, 0))
            self.mineGrid.append(col)

        self.mineGrid = np.array(self.mineGrid)

        # Fill our grid with mines, represented as -1
        for i in range(self.dimension):
            for j in range(self.dimension):
                if random.random() < self.probability:
                    self.mineGrid[i][j] = Cell(True, -1)
                else:
                    self.mineGrid[i][j] = Cell(False, 0)

        # Add surrounding mine numbers to board
        self.putNumbersOnBoard()

        # Show us the board
        self.display()


    def putNumbersOnBoard(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.mineGrid[i][j].isMine is False:
                    mines = 0
                    if i - 1 >= 0 and j - 1 >= 0 and self.mineGrid[i - 1][j - 1].isMine:
                        mines += 1
                    if j - 1 >= 0 and self.mineGrid[i][j - 1].isMine:
                        mines += 1
                    if j - 1 >= 0 and i + 1 < self.dimension and self.mineGrid[i + 1][j - 1].isMine:
                        mines += 1
                    if i - 1 >= 0 and self.mineGrid[i - 1][j].isMine:
                        mines += 1
                    if j + 1 < self.dimension and self.mineGrid[i][j + 1].isMine:
                        mines += 1
                    if i - 1 >= 0 and j + 1 < self.dimension and self.mineGrid[i - 1][j + 1].isMine:
                        mines += 1
                    if i + 1 < self.dimension and self.mineGrid[i + 1][j].isMine:
                        mines += 1
                    if i + 1 < self.dimension and j + 1 < self.dimension and self.mineGrid[i + 1][j + 1].isMine:
                        mines += 1

                    self.mineGrid[i][j].setSurroundingMines(mines)

    def display(self):
        # Create a temp grid of just numbers (so we can show colors too)

        tmp = []

        for i in range(self.dimension):
            col = []
            for j in range(self.dimension):
                col.append(self.mineGrid[i][j].surroundingMines)
            tmp.append(col)

        # Add colors to grid
        _, ax = plt.subplots()
        ax.imshow(tmp, cmap=colors.ListedColormap(['black', 'blue', 'purple', 'pink', 'orange', 'red']))

        # Add numbers to grid
        for i in range(self.dimension):
            for j in range(self.dimension):
                ax.text(j, i, tmp[i][j], ha="center", va="center", color="white")  # ,  bbox=dict(facecolor='blue'))

        plt.axis('off')
        plt.show()










if __name__ == '__main__':
    grid = MineGrid(10, .05)
    print('Testing ... ')
