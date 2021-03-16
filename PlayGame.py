import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings
from main import AgentBoard
from main import MineGrid

warnings.simplefilter(action='ignore', category=FutureWarning)

# GAME BOARD: -1 = MINE, 0-9 = CLUE
# AGENT BOARD: -3 = FLAGGED MINE, -2 = COVERED, -1 = BLOWN UP MINE, 0-9 = CLUE


def Basic_Agent_GamePlay(Game, Agent):
    print("Running Basic")
    coveredSet=[]
    dimension=Game.dimension

    for i in range(0,dimension):
        for j in range(0,dimension):
            coveredSet.append((i,j))

    visited=[]

    while coveredSet:
        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)
        visited.append([i,j])

        for cord in visited:
            x=cord[0]
            y=cord[1]
            rev_safe = get_revealed_safe_neighbors(x, y, Agent)
            hiddenCords = []
            hidden = get_hidden_square(x, y, Agent, hiddenCords)
            neighbors = count_surrounding_spaces(x, y, Agent)
            mines = get_surrounding_mines(x, y, Agent)
            clue = Agent.board[x][y]
            if clue - mines == hidden:  # All hidden are mines
                markMines(Agent, hiddenCords, coveredSet,visited)
            elif neighbors-clue-rev_safe == hidden:  # All hidden are safe
                for coord in hiddenCords:
                    flip(Game, Agent, coord[0], coord[1])








        

def Improved_Agent_GamePlay(Game, Agent):
    print("Running Improved")
    dimension = Game.dimension

    # Create a set of all the covered spaces
    coveredSet = []
    for i in range(0, dimension):
        for j in range(0, dimension):
            coveredSet.append((i, j))

    safe = []
    visited = []

    minesFlagged = 0
    zero=[]

    # Pull off a random element to get started
    while coveredSet:
        #i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)
        i,j=1,1


        if Agent.board[i][j]==0:
            zero.append((i,j))
            reveal_safe_zeros(Agent,Game,zero,coveredSet)
        else:
            neighbor_list=[]
            get_neighboring_spots(i,j,neighbor_list,Agent)
            set_spots=[]
            get_revealed_safe_neighbors(i,j,Agent,set_spots)
            mine_sets=[]
            sets_list=[]
            for item in set_spots:
                set_items=[]
                get_neighboring_spots(item[1][0],item[1][1],set_items,Agent)
                sets_list.append(set_items)
                mine_sets.append([item[0],set_items])
            

            if len(sets_list)>1:
                intersection(sets_list)
                sets_list=sets_list.pop()
                for i in range (len(sets_list)):
                    copy=(sets_list[i][0],sets_list[i][1])
                    if copy not in coveredSet:
                        sets_list.remove(copy)
                if len(sets_list)>0:
                    
                    print(sets_list)
                    markMines(Agent, sets_list, coveredSet,visited)
            for item in sets_list:
                for info in mine_sets:
                    if item in info[1]:
                        info[1].remove(item)
                        info[0]=info[0]-1

            for item in mine_sets:
                if item[0]==0:
                    revealed(Game,Agent,item[1],coveredSet)

            break




                
            
            





        
        





'''         #i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet) commented out for the sake of the demonstration
        # print(Agent.board[i][j])
        i,j=1,1
        coveredSet.remove((2,2))
        #get the neighbors of the spot
        neighbor_list=[]
        get_neighboring_spots(i,j,neighbor_list,Agent)
        #create a sub environment 3for tongihts example it will be a 3x3 matrix
        #
        #
        #
        #
        #
        #Get revealed neighbors
        set_spots=[]
        get_revealed_safe_neighbors(i,j,Agent,set_spots)
        print('Progress')
        mine_sets=[]
        for item in set_spots:
            set_items=[]
            get_neighboring_spots(item[1][0],item[1][1],set_items,Agent)
            mine_sets.append((item[0],set_items))
        # we now have obtained our sets

        while mine_sets and len(mine_sets)>1:
            set1=mine_sets[len(mine_sets)-1]
            mine_sets.remove(set1)
            set2=mine_sets[len(mine_sets)-1]

            suround1=set1[0]
            suround2=set2[0]
            set1=set1[1]
            set2=set2[1]
            intersect=intersection(set1,set2)
            for xy in intersect:
                Agent.board[xy[0]][xy[1]]=-3
                set1.remove(xy)
                set2.remove(xy)
                suround1=suround1-1
                suround2=suround2-1
            if suround1==len(set1):
                #markMines(Agent,set1)
                #do some updating
                while set1:
                    xy=set1[len(set1)-1]
                    Agent.board[xy[0]][xy[1]]=-3
                    set1.remove(xy)
                    suround1=suround1-1

            if suround2==len(set2):
                while set1:
                    xy=set1[len(set1)-1]
                    Agent.board[xy[0]][xy[1]]=-3
                    set2.remove(xy)
                    suround1=suround1-1
                print("progress")
                #also do some updating
            if suround2==0 and suround1==0:
                for xy in set1:
                    Agent.board[xy[0]][xy[1]]=Game.mineGrid[xy[0]][xy[1]]
                for xy in set2:
                    Agent.board[xy[0]][xy[1]]=Game.mineGrid[xy[0]][xy[1]]
                 '''
            
def revealed(Game,Agent, spots, coveredSet):
    for item in spots:
        x=item[0]
        y=item[1]
        Agent.board[x][y]=Game.mineGrid[x][y]
        coveredSet.remove((x,y))
#intersection method from geeks for geeks
def intersection(sets): 
    while len(sets)>1:
        lst1=sets.pop()
        lst2=sets.pop()
        lst3 = [value for value in lst1 if value in lst2]
        sets.append(lst3)






#Helper methods
def get_neighboring_spots(i,j, neighbor_list,Agent):        
    if i - 1 >= 0:
        neighbor_list.append([i-1,j])

    if j - 1 >= 0:
        neighbor_list.append([i,j-1])

    if i + 1 < Agent.dimension:
        neighbor_list.append([i+1,j])

    if j + 1 < Agent.dimension:
        neighbor_list.append([i,j+1])

    if i - 1 >= 0 and j - 1 >= 0:
        neighbor_list.append([i-1,j-1])

    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        neighbor_list.append([i-1,j+1])

    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        neighbor_list.append([i+1,j+1])

    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        neighbor_list.append([i+1,j-1])


def reveal_safe_zeros(Agent, Game, zero,coveredSet):
    while zero:
        xfirst = random.choices(zero)
        xfirst = xfirst[0]
        zero.remove(xfirst)

        # print(xfirst)

        i = xfirst[0]
        j = xfirst[1]
        
        if i - 1 >= 0 and Agent.board[i-1][j]==-2:
            Agent.board[i-1][j]=Game.mineGrid[i-1][j]
            if Agent.board[i-1][j]==0:
                zero.append([i-1,j])
                coveredSet.remove((i-1,j))

   
        if j - 1 >= 0 and Agent.board[i][j-1]==-2:
            Agent.board[i][j-1]=Game.mineGrid[i][j-1]
            if Agent.board[i][j-1]==0:
                zero.append([i,j-1])
                coveredSet.remove((i,j-1))
    
        if i + 1 < Agent.dimension and Agent.board[i+1][j]==-2:
            Agent.board[i+1][j]=Game.mineGrid[i+1][j]
            if Agent.board[i+1][j]==0:
                zero.append([i+1,j])
                coveredSet.remove((i+1,j))
    
        if j + 1 < Agent.dimension and Agent.board[i][j+1]==-2:
            Agent.board[i][j+1]=Game.mineGrid[i][j+1]
            if Agent.board[i][j+1]==0:
                zero.append([i,j+1])
                coveredSet.remove((i,j+1))
    
        if i - 1 >= 0 and j - 1 >= 0 and Agent.board[i-1][j-1]==-2:
            Agent.board[i-1][j-1]=Game.mineGrid[i-1][j-1]
            if Agent.board[i-1][j-1]==0:
                zero.append([i-1,j-1])
                coveredSet.remove((i-1,j-1))
    
        if i - 1 >= 0 and j + 1 <= Agent.dimension - 1 and Agent.board[i-1][j+1]==-2:
            Agent.board[i-1][j+1]=Game.mineGrid[i-1][j+1]
            if Agent.board[i-1][j+1]==0:
                zero.append([i-1,j+1])
                coveredSet.remove((i-1,j+1))
    
        if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1 and Agent.board[i+1][j+1]==-2:
            Agent.board[i+1][j+1]=Game.mineGrid[i+1][j+1]
            if Agent.board[i+1][j+1]==0:
                zero.append([i+1,j+1])
                coveredSet.remove((i+1,j+1))
    
        if i + 1 <= Agent.dimension - 1 and j - 1 >= 0 and Agent.board[i+1][j-1]==-2:
            Agent.board[i+1][j-1]=Game.mineGrid[i+1][j-1]
            if Agent.board[i+1][j-1]==0:
                zero.append([i+1,j-1])
                coveredSet.remove((i+1,j-1))




        



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


def markMines(Agent, hidden, coveredSet=[],visited=[]):
    for xy in hidden:
        Agent.board[xy[0]][xy[1]] = -3
        coveredSet.remove((xy[0], xy[1]))
        visited.append([xy[0],xy[1]])



def pickRandomSquare(Game, Agent, coveredSet):
    xfirst = random.choices(coveredSet)
    xfirst = xfirst[0]
    coveredSet.remove(xfirst)

    # print(xfirst)

    x = xfirst[0]
    y = xfirst[1]

    flip(Game, Agent, x, y)

    return x, y, coveredSet


def get_revealed_safe_neighbors(i, j, Agent, set_spots=[]):
    safely_revealed = 0
    if i - 1 >= 0:
        if Agent.board[i - 1][j] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i-1][j],[i-1,j]))
    if j - 1 >= 0:
        if Agent.board[i][j - 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i][j-1],[i,j-1]))
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i+1][j],[i+1,j]))
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i][j+1],[i,j+1]))
    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i-1][j-1],[i-1,j-1]))
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i-1][j+1],[i-1,j+1]))
    if i+1<=Agent.dimension-1 and j+1<=Agent.dimension-1:
        if Agent.board[i + 1][j + 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i+1][j+1],[i+1,j+1]))
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i+1][j-1],[i+1,j-1]))
    return safely_revealed


def count_surrounding_spaces(i, j, Agent):
    neighbors = 0
    if i - 1 >= 0:
        neighbors = neighbors + 1
    if j - 1 >= 0:
        neighbors = neighbors + 1
    if i + 1 < Agent.dimension:
        neighbors = neighbors + 1
    if j + 1 < Agent.dimension:
        neighbors = neighbors + 1
    if i - 1 >= 0 and j - 1 >= 0:
        neighbors = neighbors + 1
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        neighbors = neighbors + 1
    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        neighbors = neighbors + 1
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        neighbors = neighbors + 1
    return neighbors


def get_surrounding_mines(i, j, Agent):
    hidden = 0
    if i - 1 >= 0:
        if Agent.board[i - 1][j] == -1 or Agent.board[i - 1][j] == -3:
            hidden = hidden + 1
    if j - 1 >= 0:
        if Agent.board[i][j - 1] == -1 or Agent.board[i][j - 1] == -3:
            hidden = hidden + 1
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] == -1 or Agent.board[i + 1][j] == -3:
            hidden = hidden + 1
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] == -1 or Agent.board[i][j + 1] == -3:
            hidden = hidden + 1
    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] == -1 or Agent.board[i - 1][j - 1] == -3:
            hidden = hidden + 1
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] == -1 or Agent.board[i - 1][j + 1] == -3:
            hidden = hidden + 1
    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i + 1][j + 1] == -1 or Agent.board[i + 1][j + 1] == -3:
            hidden = hidden + 1
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] == -1 or Agent.board[i + 1][j - 1] == -3:
            hidden = hidden + 1
    return hidden


def get_hidden_square(i, j, Agent, hiddenCoordinates):
    hidden = 0
    if i - 1 >= 0:
        if Agent.board[i - 1][j] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i - 1, j])
    if j - 1 >= 0:
        if Agent.board[i][j - 1] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i, j - 1])
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i + 1, j])
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i, j + 1])
    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i - 1, j - 1])
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i - 1, j + 1])
    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i + 1][j + 1] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i + 1, j + 1])
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] == -2:
            hidden = hidden + 1
            hiddenCoordinates.append([i + 1, j - 1])
    return hidden



if __name__ == '__main__':

    sum = 0
    s1=[[1,0],[1,2],[4,3]]
    s2=[[1,0],[1,3,],[4,4]]
    s3=[[1,0],[1,4],[4,5]]
    setlist = [s1,s2,s3]
    intersection(setlist)
    u=setlist.pop()
    print(u)

    answerSheet = MineGrid(3, 0)
    answerSheet.mineGrid[0][0]=1
    answerSheet.mineGrid[0][1]=2
    answerSheet.mineGrid[0][2]=2
    answerSheet.mineGrid[1][0]=2
    answerSheet.mineGrid[1][1]= -1   
    answerSheet.mineGrid[1][2]=-1
    answerSheet.mineGrid[2][0]=2
    answerSheet.mineGrid[2][1]=-1
    answerSheet.mineGrid[2][2]=3

    agent = AgentBoard(answerSheet.dimension)
    agent.board[0][0]=1
    agent.board[2][2]=3
    Improved_Agent_GamePlay(answerSheet, agent)

    #answer = 0
    #found = 0
    #for x in range(agent.dimension):
    #    for y in range(agent.dimension):
    #        if agent.board[x][y] == -3:
    #            found = found + 1
    #        if answerSheet.mineGrid[x][y] == -1:
    #            answer = answer + 1
    #            
    #print((found / answer))
    answerSheet.display()
    agent.display()
