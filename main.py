import random
import numpy as np


class MineGrid:

    def __init__(self, d, n):
        self.dimension = d
        self.probability = n
        self.mineGrid = []

        # Instantiate our minesweeper grid
        for i in range(self.dimension):
            col = []
            for j in range(self.dimension):
                col.append(0)
            self.mineGrid.append(col)

        # Fill our grid with mines, represented as -1
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.mineGrid[i][j] = random.choices([0, -1], [1 - self.probability, self.probability])
        self.mineGrid = np.array(self.mineGrid)

        # How will we graphically represent our grid?

if __name__ == '__main__':
    grid = MineGrid(10, .05)
    print('Testing ... ')


