import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings
from main import AgentBoard
from main import MineGrid


warnings.simplefilter(action='ignore', category=FutureWarning)


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


def Improved_Agent_GamePlay(Game, Agent):
    dimension = Game.dimension

    # Create a set of all the covered spaces
    coveredSet = []
    for i in range(0, dimension):
        for j in range(0, dimension):
            coveredSet.append((i, j))

    safe = []
    visited = []

    minesFlagged = 0

    # Pull off a random element to get started
    for _ in range(2):
        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)
        print(Agent.board[i][j])
        Agent, Game, safe, visited = checkZeros(Agent, Game, dimension, i, j, safe, visited)







    #if Agent.board[i][j] == 0:
      #  safe.append((i, j))
      #  clearZeros(Agent, Game, dimension, i, j, safe, visited)
  # else: # flip more
    # i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)

        #if Agent.board[i][j] == 0:
    #i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)
    #Agent, Game, safe, visited = checkZeros(Agent, Game, dimension, i, j, safe, visited)
        # Check Knowledge base

        # Flip again





    Agent.display()




    # Do a quick search to check for easily identified mines and safe spaces
    # NOTE, THIS WILL ONLY EXECUTE WHEN THE FIRST VALUE RANDOMLY SELECTED IS A ZERO !!
    # MAY NEED TO RUN SEVERAL TIMES TO SEE
    for _ in range(4):
        for x in range(0, dimension):
            for y in range(0, dimension):

                safe = get_revealed_safe_neighbors(x, y, Agent)
                hiddenCords = []
                hidden = get_hidden_square(x, y, Agent, hiddenCords)
                neighbors = count_surrounding_spaces(x, y, Agent)
                mines = get_surrounding_mines(x, y, Agent)
                if Agent.board[x][y] > 0:

                    clue = Agent.board[x][y]
                    print(clue, hidden)
                    if hidden+mines == clue: # All hidden are mines
                        minesFlagged = markMines(minesFlagged, Agent, hiddenCords)
                    elif mines == clue: # All hidden are safe
                        for coord in hiddenCords:
                            flip(Game, Agent, coord[0], coord[1])

    print(100 * (minesFlagged / Game.numberOfMines), "% of Mines found safely")
    Agent.display()





def checkZeros(Agent, Game, dimension, i, j, safe, visited):
    if Agent.board[i][j] == 0:
        safe.append((i, j))
        return clearZeros(Agent, Game, dimension, i, j, safe, visited)
    return Agent, Game, safe, visited


def clearZeros(Agent, Game, dimension, i, j, safe, visited):
    while len(safe) > 0:
        ans = safe.pop(0)
        i = ans[0]
        j = ans[1]
        visited.append((i, j))

        # flip 8 surrounding squares, which must be safe
        if i - 1 >= 0 and (i - 1, j) not in visited:
            flip(Game, Agent, i - 1, j)
            if Agent.board[i - 1][j] == 0:
                safe.append((i - 1, j))
        if j - 1 >= 0 and (i, j - 1) not in visited:
            flip(Game, Agent, i, j - 1)
            if Agent.board[i][j - 1] == 0:
                safe.append((i, j - 1))
        if i + 1 < dimension and (i + 1, j) not in visited:
            flip(Game, Agent, i + 1, j)
            if Agent.board[i + 1][j] == 0:
                safe.append((i + 1, j))
        if j + 1 < Agent.dimension and (i, j + 1) not in visited:
            flip(Game, Agent, i, j + 1)
            if Agent.board[i][j + 1] == 0:
                safe.append((i, j + 1))
        if i - 1 >= 0 and j - 1 >= 0 and (i - 1, j - 1) not in visited:
            flip(Game, Agent, i - 1, j - 1)
            if Agent.board[i - 1][j - 1] == 0:
                safe.append((i - 1, j - 1))
        if i - 1 >= 0 and j + 1 <= Agent.dimension - 1 and (i - 1, j + 1) not in visited:
            flip(Game, Agent, i - 1, j + 1)
            if Agent.board[i - 1][j + 1] == 0:
                safe.append((i - 1, j + 1))
        if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1 and (i + 1, j + 1) not in visited:
            flip(Game, Agent, i + 1, j + 1)
            if Agent.board[i + 1][j + 1] == 0:
                safe.append((i + 1, j + 1))
        if i + 1 <= Agent.dimension - 1 and j - 1 >= 0 and (i + 1, j - 1) not in visited:
            flip(Game, Agent, i + 1, j - 1)
            if Agent.board[i + 1][j - 1] == 0:
                safe.append((i + 1, j - 1))
    return Agent, Game, safe, visited




def flip(Game, Agent, x, y):
    Agent.board[x][y] = Game.mineGrid[x][y]


def markMines(flaggedMines, Agent, hidden):
    for x in hidden:
        Agent.board[x[0]][x[1]] = -1
        flaggedMines = flaggedMines + 1
    return flaggedMines


def pickRandomSquare(Game, Agent, coveredSet):
    xfirst = random.choices(coveredSet)
    xfirst = xfirst[0]
    coveredSet.remove(xfirst)

    #print(xfirst)

    x = xfirst[0]
    y = xfirst[1]

    flip(Game, Agent, x, y)

    return x, y, coveredSet



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


def get_surrounding_mines(i,j,Agent):
    hidden=0
    if i - 1 >= 0:
        if Agent.board[i - 1][j]==-1:
            hidden = hidden + 1
    if j - 1 >= 0:
        if Agent.board[i][j - 1]==-1:
            hidden = hidden + 1
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j]==-1:
            hidden = hidden + 1
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1]==-1:
            hidden = hidden + 1
    if i-1>=0 and j-1>=0:
        if Agent.board[i-1][j-1]==-1:
            hidden=hidden+1
    if i-1>=0 and j+1<=Agent.dimension-1:
        if Agent.board[i-1][j+1]==-1:
            hidden=hidden+1
    if i+1<=Agent.dimension-1 and j+1<=Agent.dimension-1:
        if Agent.board[i+1][j+1]==-1:
            hidden=hidden+1
    if i+1<=Agent.dimension-1 and j-1>=0:
        if Agent.board[i+1][j-1]==-1:
            hidden=hidden+1
    return hidden



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


    answerSheet = MineGrid(16, 40)
    agent = AgentBoard(16)
    #Basic_Agent_GamePlay(answerSheet,agent)

    Improved_Agent_GamePlay(answerSheet, agent)

    answerSheet.display()
    #agent.display()
