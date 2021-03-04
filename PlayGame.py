import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from main import Agent_Board
from main import Cell
from main import MineGrid



def Basic_Agent_GamePlay(Game, Agent):

    num=Game.numberOfMines
    visitedCells=[]
    bombCells=[]
    revealed_mines=0
    while(num != 0):
        i=random.randint(0,Game.dimension-1)
        j=random.randint(0,Game.dimension-1)
        if Agent.board[i][j]!=-2: #if we have already revealed the spot we continue
            continue
        else:
            Agent.board[i][j]=Game.mineGrid[i][j]

            if Game.mineGrid[i][j]==-1:
                Agent.board[i][j]=-1
                num=num-1
                bombCells.append([i,j])
                revealed_mines=revealed_mines+1
                continue
            else:
                #number of safe spaces
                num_of_safe_square=count_surrounding_spaces(i,j,Agent)-Agent.board[i][j] #change to number of surrounding square
                #number of mines surrounding the cell
                num_of_surrounding_mines=Game.mineGrid[i][j]
                #hidden neighbors
                hiddenCoordinates=[]
                hidden=get_hidden_square(i,j,Agent,hiddenCoordinates)

                safe_revealed_neighbors=get_revealed_safe_neighbors(i,j,Agent)

                if Game.numberOfMines-revealed_mines==hidden:
                    #every neighbor is a mine
                    for coordinate in hiddenCoordinates:
                        x=coordinate[0]
                        y=coordinate[1]
                        Agent.board[x][y]=-1
                        num=num-1
                        visitedCells.append([x,y])
                    
                if num_of_safe_square-safe_revealed_neighbors==hidden:
                    #mark every neighbor as safe.
                    for coordinate in hiddenCoordinates:
                        x=coordinate[0]
                        y=coordinate[1]
                        Agent.board[x][y]=Game.mineGrid[x][y]
                        visitedCells.append([x,y])


def get_revealed_safe_neighbors(i,j,Agent):
    safely_revealed=0
    if i - 1 >= 0:
        if Agent.board[i - 1][j]!=-2 and Agent.board[i - 1][j]!=-1:
            safely_revealed = safely_revealed + 1
    if j - 1 >= 0:
        if Agent.board[i][j - 1]!=-2 and Agent.board[i][j-1]!=-1:
            safely_revealed =safely_revealed + 1
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j]!=-2 and Agent.board[i + 1][j]!=-1:
            safely_revealed = safely_revealed + 1
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1]!=-2 and Agent.board[i][j + 1]!=-1:
            safely_revealed = safely_revealed + 1
    if i-1>=0 and j-1>=0:
        if Agent.board[i-1][j-1]!=-2 and Agent.board[i-1][j-1]!=-1 :
            safely_revealed=safely_revealed+1
    if i-1>=0 and j+1<=Agent.dimension-1:
        if Agent.board[i-1][j+1]!=-2 and Agent.board[i-1][j+1]!=-1 :
            safely_revealed=safely_revealed+1                 
    if i+1<=Agent.dimension-1 and j+1<=Agent.dimension-1:
        if Agent.board[i+1][j+1]!=-2 and Agent.board[i+1][j+1]!=-1 :
            safely_revealed=safely_revealed
    if i+1<=Agent.dimension-1 and j-1>=0:
        if Agent.board[i+1][j-1]!=-2 and Agent.board[i+1][j-1]!=-1 :
            safely_revealed=safely_revealed+1   
    return safely_revealed  

def count_surrounding_spaces(i,j,Agent):
    neighbors=0
    if i - 1 >= 0:
        neighbors=neighbors+1
    if j - 1 >= 0:
        neighbors=neighbors+1
    if i + 1 < Agent.dimension:
        neighbors=neighbors+1
    if j + 1 < Agent.dimension:
        neighbors=neighbors+1
    if i-1>=0 and j-1>=0:
        neighbors=neighbors+1
    if i-1>=0 and j+1<=Agent.dimension-1:
        neighbors=neighbors+1
    if i+1<=Agent.dimension-1 and j+1<=Agent.dimension-1:
        neighbors=neighbors+1
    if i+1<=Agent.dimension-1 and j-1>=0:
        neighbors=neighbors+1
    return neighbors




def get_hidden_square(i,j,Agent,hiddenCoordinates):
    hidden=0
    if i - 1 >= 0:
        if Agent.board[i - 1][j]==-2:
            hidden = hidden + 1
            hiddenCoordinates.append([i-1,j])
    if j - 1 >= 0:
        if Agent.board[i][j - 1]==-2:
            hidden = hidden + 1
            hiddenCoordinates.append([i,j-1])
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j]==-2:
            hidden = hidden + 1
            hiddenCoordinates.append([i+1,j])
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1]==-2:
            hidden = hidden + 1
            hiddenCoordinates.append([i,j+1])
    if i-1>=0 and j-1>=0:
        if Agent.board[i-1][j-1]==-2:
            hidden=hidden+1
            hiddenCoordinates.append([i-1,j-1])
    if i-1>=0 and j+1<=Agent.dimension-1:
        if Agent.board[i-1][j+1]==-2:
            hidden=hidden+1   
            hiddenCoordinates.append([i-1,j+1])                 
    if i+1<=Agent.dimension-1 and j+1<=Agent.dimension-1:
        if Agent.board[i+1][j+1]==-2:
            hidden=hidden+1
            hiddenCoordinates.append([i+1,j+1])
    if i+1<=Agent.dimension-1 and j-1>=0:
        if Agent.board[i+1][j-1]==-2:
            hidden=hidden+1
            hiddenCoordinates.append([i+1,j-1])     
    return hidden   

















if __name__ == '__main__':


    Game=MineGrid(10,3)
    Agent=Agent_Board(10)
    Basic_Agent_GamePlay(Game,Agent)

    