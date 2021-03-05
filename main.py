import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# Cell used to in conjunction with Agent's Board
class Cell:
    def __init__(self, isMine, surroundingMines):
        self.isMine = isMine
        self.surroundingMines = surroundingMines


# Computer's copy of the board, where the mines are actually located
class MineGrid:

    def __init__(self, d, n):
        self.dimension = d
        self.numberOfMines = n
        mineGrid = [[0]*self.dimension]*self.dimension

        # Instantiate our minesweeper grid with 0's

        self.mineGrid = np.array(mineGrid)

        # Fill our grid with mines, represented as -1
        x=self.numberOfMines
        while x>0:
            i=random.randint(0,self.dimension-1)
            j=random.randint(0,self.dimension-1)
            if self.mineGrid[i][j]==-1:
                continue
            else:
                self.mineGrid[i][j] = -1
                x=x-1

        # Add surrounding mine numbers to board
        self.putNumbersOnBoard()


    def putNumbersOnBoard(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.mineGrid[i][j]!=-1:
                    mines = 0
                    if i - 1 >= 0 and j - 1 >= 0 and self.mineGrid[i - 1][j - 1]==-1:
                        mines += 1
                    if j - 1 >= 0 and self.mineGrid[i][j - 1]==-1:
                        mines += 1
                    if j - 1 >= 0 and i + 1 < self.dimension and self.mineGrid[i + 1][j - 1]==-1:
                        mines += 1
                    if i - 1 >= 0 and self.mineGrid[i - 1][j]==-1:
                        mines += 1
                    if j + 1 < self.dimension and self.mineGrid[i][j + 1]==-1:
                        mines += 1
                    if i - 1 >= 0 and j + 1 < self.dimension and self.mineGrid[i - 1][j + 1]==-1:
                        mines += 1
                    if i + 1 < self.dimension and self.mineGrid[i + 1][j]==-1:
                        mines += 1
                    if i + 1 < self.dimension and j + 1 < self.dimension and self.mineGrid[i + 1][j + 1]==-1:
                        mines += 1

                    self.mineGrid[i][j]=mines

    def display(self):
        # Create a temp grid of just numbers (so we can show colors too)

        # Add colors to grid
        _, ax = plt.subplots()
        ax.imshow(self.mineGrid, cmap=cm.get_cmap('Reds', 10))

        # Add numbers to grid
        for i in range(self.dimension):
            for j in range(self.dimension):
                ax.text(j, i, self.mineGrid[i][j], ha="center", va="center", color="black")

        plt.axis('off')
        plt.title('Environment')
        plt.show()


# Agent's copy of the the board
class AgentBoard:
    def __init__(self, dimension):
        # Agent is not allowed to peek into the grid
        Agent_Environment=[[-2]*dimension]*dimension
        self.dimension=dimension
        self.minesSafelyFound=0
        self.board=np.array(Agent_Environment)


    def display(self):
        # Create a temp grid of just numbers (so we can show colors too)


        # Add colors to grid
        _, ax = plt.subplots()
        ax.imshow(self.board, cmap=cm.get_cmap('Reds', 10))

        # Add numbers to grid
        for i in range(self.dimension):
            for j in range(self.dimension):
                ax.text(j, i, self.board[i][j], ha="center", va="center", color="black")

        plt.axis('off')
        plt.title('Agent')
        plt.show()

