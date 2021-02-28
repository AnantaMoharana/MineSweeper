import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)



class Cell:
    def __init__(self, mine, surrounding_mines):
        self.mine = mine
        self.surroundingMines = surrounding_mines


class MineGrid:

    def __init__(self, d, n):
        self.dimension = d
        self.probability = n
        self.mineGrid = []

        # Instantiate our minesweeper grid
        for i in range(self.dimension):
            col = []
            for j in range(self.dimension):
                col.append(Cell(False, 0))
            self.mineGrid.append(col)

        # Fill our grid with mines, represented as -1
        for i in range(self.dimension):
            for j in range(self.dimension):
                choice = random.choices([0, -1], [1 - self.probability, self.probability])
                self.mineGrid[i][j] = Cell((choice == -1), 0)
        self.mineGrid = np.array(self.mineGrid)

        self.putNumbersOnBoard()

    def putNumbersOnBoard(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if not self.mineGrid[i][j].mine:
                    mines = 0
                    if i - 1 >= 0 and j - 1 >= 0 and self.mineGrid[i - 1][j - 1].mine:
                        mines += 1
                    if j - 1 >= 0 and self.mineGrid[i][j - 1] == -1:
                        mines += 1
                    if j - 1 >= 0 and i + 1 < self.dimension and self.mineGrid[i + 1][j - 1].mine:
                        mines += 1
                    if i - 1 >= 0 and self.mineGrid[i - 1][j].mine:
                        mines += 1
                    if j + 1 < self.dimension and self.mineGrid[i][j + 1].mine:
                        mines += 1
                    if i - 1 >= 0 and j + 1 < self.dimension and self.mineGrid[i - 1][j + 1].mine:
                        mines += 1
                    if i + 1 < self.dimension and self.mineGrid[i + 1][j].mine:
                        mines += 1
                    if i + 1 < self.dimension and j + 1 < self.dimension and self.mineGrid[i + 1][j + 1].mine:
                        mines += 1

                    self.mineGrid[i][j].surroundingMines = mines


if __name__ == '__main__':
    grid = MineGrid(10, .05)
    print('Testing ... ')
