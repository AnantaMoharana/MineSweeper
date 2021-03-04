import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
"""
class Cell:
    def __init__(self,isMine,SurroundingMines,hasBeenRevealed):
        self.isMine=False
        self.SurroundingMines=0
        self.surroundingSafeSquares=0
        self.hasBeenRevealed=False
        self.isSafe=True
        self.surroundingHidden=0
        self.identified_Surrounding_Mines=0
        self.visited=False

class Environment:
    def __init__(self,d,p):
        self.dimension=d
        self.probability=p
        self.mineCount=0
        self.mineGrid=[]
        self.revealedMines=0
        for i in range(self.dimension):
            col = []
            for j in range(self.dimension):
                col.append(Cell(False, 0,False))
            self.mineGrid.append(col)

        self.mineGrid = np.array(self.mineGrid)

        for i in range(self.dimension):
            for j in range(self.dimension):
                self.mineGrid[i][j].isMine=random.choices([False, True], [1 - self.probability, self.probability])[0]
                if self.mineGrid[i][j].isMine==True:
                    self.mineCount=self.mineCount+1
                    self.mineGrid[i][j].isSafe=False

       

        for i in range(self.dimension):
            for j in range(self.dimension):
                neighbors=0
                if i - 1 >= 0:
                    if self.mineGrid[i - 1][j].isMine == True:
                        neighbors = neighbors + 1
                if j - 1 >= 0:
                    if self.mineGrid[i][j - 1].isMine == True:
                        neighbors = neighbors + 1
                if i + 1 < self.dimension:
                    if self.mineGrid[i + 1][j].isMine == True:
                        neighbors = neighbors + 1
                if j + 1 < self.dimension:
                    if self.mineGrid[i][j + 1].isMine == True:
                        neighbors = neighbors + 1

                if i-1>=0 and j-1>=0:
                    if self.mineGrid[i-1][j-1].isMine==True:
                        neighbors=neighbors+1
                if i-1>=0 and j+1<=self.dimension-1:
                    if self.mineGrid[i-1][j+1].isMine==True:
                        neighbors=neighbors+1                    
                if i+1<=self.dimension-1 and j+1<=self.dimension-1:
                    if self.mineGrid[i+1][j+1].isMine==True:
                        neighbors=neighbors+1
                if i+1<=self.dimension-1 and j-1>=0:
                    if self.mineGrid[i+1][j-1].isMine==True:
                        neighbors=neighbors+1  
                self.mineGrid[i][j].SurroundingMines=neighbors
                self.mineGrid[i][j].surroundingSafeSquares=self.mineCount-neighbors

        
        

    



"""
class Cell:
    def __init__(self, isMine, surroundingMines):
        self.isMine = isMine
        self.surroundingMines = surroundingMines


    def setSurroundingMines(self, m):
        self.surroundingMines =  m



# mineGrid is a 2D matrix of Cells, where we can also store future information

class MineGrid:

    def __init__(self, d, n):
        self.dimension = d
        self.numberOfMines = n
        mineGrid=[[0]*self.dimension]*self.dimension

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

        # Show us the board
        #self.display()


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

 #       tmp = []

 #       for i in range(self.dimension):
  #          col = []
  #          for j in range(self.dimension):
  #             col.append(self.mineGrid[i][j].surroundingMines)
  #          tmp.append(col)

        # Add colors to grid
        _, ax = plt.subplots()
        ax.imshow(self.mineGrid, cmap=cm.get_cmap('Reds', 10))

        # Add numbers to grid
        for i in range(self.dimension):
            for j in range(self.dimension):
                ax.text(j, i, self.mineGrid[i][j], ha="center", va="center", color="black")  # ,  bbox=dict(facecolor='blue'))

        plt.axis('off')
        plt.title('Environment')
        plt.show()


class Agent_Board:
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
                ax.text(j, i, self.board[i][j], ha="center", va="center", color="black")  # ,  bbox=dict(facecolor='blue'))

        plt.axis('off')
        plt.title('Agent')
        plt.show()








if __name__ == '__main__':
    d = 10
    p = 2
    Grid=MineGrid(d,p)

    print('Testing ... ')
    Grid.display()

    Agent=Agent_Board(Grid.dimension)
    Agent.display()

