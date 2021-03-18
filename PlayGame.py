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

    visited = []
    zero=[]
    mine_sets=[]
    sets_list=[]

    # Pull off a random element to get started
    while coveredSet:
        #Agent.display()
        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)
        neighbor_list=[]
        if Agent.board[i][j]==0:
            zero.append((i,j))
            nonzero=[]
            reveal_safe_zeros(Agent,Game,zero,coveredSet,nonzero)
            Agent.display()
            tracker=[]
            while nonzero:
                #answerSheet.display()
                neighbor_list.clear()
                spot=nonzero.pop(0)
                get_revealed_safe_non_zero_neighbors(spot[0],spot[1],Agent,neighbor_list)
                #get neighboring revealed spots
                set_items=[]
                get_hidden_neighboring_spots(spot[0],spot[1],set_items,Agent)
                mine_sets.append([Agent.board[spot[0]][spot[1]],set_items,spot])
                tracker.append([spot[0],spot[1]])
                sets_list.append(set_items)

                for item in neighbor_list:
                    set_items=[]
                    get_hidden_neighboring_spots(item[1][0],item[1][1],set_items,Agent)
                    sets_list.append(set_items)
                    if item[1] not in tracker:
                        mine_sets.append([item[0],set_items,item[1]])
                        tracker.append(item[1])

                if len(sets_list)>2: #2
                    intersection(sets_list)
                    sets_list=sets_list.pop()
                    for i in range (len(sets_list)):
                        copy=(sets_list[i][0],sets_list[i][1])
                        if copy not in coveredSet:
                            copy=[sets_list[i][0],sets_list[i][1]]
                            sets_list.remove(copy)
                else:
                    nonzero.append(spot)
                if len(sets_list)>0:
                    if len(sets_list)==2:
                        intersection(sets_list)
                        sets_list=sets_list.pop()
                        nonzero.remove(spot)
                    print(sets_list)
                    markMines(Agent,sets_list, coveredSet,visited)
                for item in sets_list:
                    for info in mine_sets:
                        if item in info[1]:
                            info[1].remove(item)
                            info[0]=info[0]-1

                for item in mine_sets:
                    if item[0]==0:
                        #hiddenCords=[]
                        if (item[2][0], item[2][1]) in coveredSet:
                            coveredSet.remove((item[2][0], item[2][1]))
                        if (item[2][0], item[2][1]) in nonzero:
                            nonzero.remove((item[2][0], item[2][1]))
                        #hidden = get_hidden_square(item[2][0], item[2][1], Agent, hiddenCords)
                        for coord in item[1]:
                            flip(Game, Agent, coord[0], coord[1])
                            if (coord[0], coord[1]) in coveredSet:
                                coveredSet.remove((coord[0], coord[1]))
                            if (coord[0], coord[1]) in nonzero:
                                nonzero.remove((coord[0], coord[1]))
                        mine_sets.remove(item)

                

                

                for item in sets_list:
                    neighboring_spots=[]
                    get_revealed_safe_non_zero_neighbors(item[0],item[1],Agent, neighboring_spots)

                    for spot in neighboring_spots:
                        value=spot[0]
                        x=spot[1][0]
                        y=spot[1][1]
                        if value-1==0:
                            if (x,y) in coveredSet:
                                coveredSet.remove((x,y))
                            if (x,y) in nonzero:
                                nonzero.remove((x,y))
                            covered=[]
                            get_hidden_neighboring_spots(x,y,covered,Agent)
                            revealed(Game,Agent,covered,coveredSet)

                           # for spot in covered:
                           #     spots_neighbors=[]
                           #     get_hidden_neighboring_spots(spot[0],spots[1],spots_neighbors)
                           #     for element in spots_neighbors:
                           #         if element in neighbor_list:
                           #             spots_neighbors.remove(element)
                           # for spot in spots_neighbors:
                           #     set_items2=[]
                           #     get_hidden_neighboring_spots(item[1][0],item[1][1],set_items2,Agent)
                           #     sets_list2.append(set_items)  
#
                            #set_items= 
                Agent.display()





               
                    

        else:
            neighbor_list.clear()
            get_revealed_safe_non_zero_neighbors(i,j,Agent,neighbor_list)
            #get neighboring revealed spots
            set_items=[]
            get_hidden_neighboring_spots(i,j,set_items,Agent)
            mine_sets.append([Agent.board[i][j],set_items,[i,j]])
            sets_list.append(set_items)

            for item in neighbor_list:
                set_items=[]
                get_hidden_neighboring_spots(item[1][0],item[1][1],set_items,Agent)
                sets_list.append(set_items)
                mine_sets.append([item[0],set_items,item[1]])

            if len(sets_list)>2:
                intersection(sets_list)
                sets_list=sets_list.pop()
                for i in range (len(sets_list)):
                    copy=(sets_list[i][0],sets_list[i][1])
                    if copy not in coveredSet:
                        copy=[sets_list[i][0],sets_list[i][1]]
                        sets_list.remove(copy)
            else:
                nonzero.append(spot)
            if len(sets_list)>0:
                if len(sets_list)==2:
                    intersection(sets_list)
                    sets_list=sets_list.pop()
                    nonzero.remove(spot)
                print(sets_list)
                markMines(Agent,sets_list, coveredSet,visited)
            for item in sets_list:
                for info in mine_sets:
                    if item in info[1]:
                        info[1].remove(item)
                        info[0]=info[0]-1

            for item in mine_sets:
                if item[0]==0:
                    hiddenCords=[]
                    if (item[2][0], item[2][1]) in coveredSet:
                        coveredSet.remove((item[2][0], item[2][1]))
                    if (item[2][0], item[2][1]) in nonzero:
                        nonzero.remove((item[2][0], item[2][1]))
                    hidden = get_hidden_square(item[2][0], item[2][1], Agent, hiddenCords)
                    for coord in hiddenCords:
                        flip(Game, Agent, coord[0], coord[1])


def get_hidden_neighboring_spots(i,j, neighbor_list,Agent):        
    if i - 1 >= 0:
        if Agent.board[i-1][j]==-2:
            neighbor_list.append([i-1,j])

    if j - 1 >= 0:
        if Agent.board[i][j-1]==-2:
            neighbor_list.append([i,j-1])

    if i + 1 < Agent.dimension:
        if Agent.board[i+1][j]==-2:
            neighbor_list.append([i+1,j])

    if j + 1 < Agent.dimension:
        if Agent.board[i][j+1]==-2:
            neighbor_list.append([i,j+1])

    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i-1][j-1]==-2:
            neighbor_list.append([i-1,j-1])

    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i-1][j+1]==-2:
            neighbor_list.append([i-1,j+1])

    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i+1][j+1]==-2:
            neighbor_list.append([i+1,j+1])

    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i+1][j-1]==-2:
            neighbor_list.append([i+1,j-1])

def get_revealed_safe_non_zero_neighbors(i, j, Agent, set_spots=[]):
    safely_revealed = 0
    if i - 1 >= 0:
        if Agent.board[i - 1][j] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i-1][j],[i-1,j]))
    if j - 1 >= 0:
        if Agent.board[i][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i][j-1],[i,j-1]))
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i+1][j],[i+1,j]))
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i][j+1],[i,j+1]))
    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i-1][j-1],[i-1,j-1]))
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i-1][j+1],[i-1,j+1]))
    if i+1<=Agent.dimension-1 and j+1<=Agent.dimension-1:
        if Agent.board[i + 1][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i+1][j+1],[i+1,j+1]))
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i+1][j-1],[i+1,j-1]))
    return safely_revealed  



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


def reveal_safe_zeros(Agent, Game, zero,coveredSet,nonzero):
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
            else:
                nonzero.append((i-1,j))

   
        if j - 1 >= 0 and Agent.board[i][j-1]==-2:
            Agent.board[i][j-1]=Game.mineGrid[i][j-1]
            if Agent.board[i][j-1]==0:
                zero.append([i,j-1])
                coveredSet.remove((i,j-1))
            else:
                nonzero.append((i,j-1))
    
        if i + 1 < Agent.dimension and Agent.board[i+1][j]==-2:
            Agent.board[i+1][j]=Game.mineGrid[i+1][j]
            if Agent.board[i+1][j]==0:
                zero.append([i+1,j])
                coveredSet.remove((i+1,j))
            else:
                nonzero.append((i+1,j))
    
        if j + 1 < Agent.dimension and Agent.board[i][j+1]==-2:
            Agent.board[i][j+1]=Game.mineGrid[i][j+1]
            if Agent.board[i][j+1]==0:
                zero.append([i,j+1])
                coveredSet.remove((i,j+1))
            else:
                nonzero.append((i,j+1))
    
        if i - 1 >= 0 and j - 1 >= 0 and Agent.board[i-1][j-1]==-2:
            Agent.board[i-1][j-1]=Game.mineGrid[i-1][j-1]
            if Agent.board[i-1][j-1]==0:
                zero.append([i-1,j-1])
                coveredSet.remove((i-1,j-1))
            else:
                nonzero.append((i-1,j-1))
    
        if i - 1 >= 0 and j + 1 <= Agent.dimension - 1 and Agent.board[i-1][j+1]==-2:
            Agent.board[i-1][j+1]=Game.mineGrid[i-1][j+1]
            if Agent.board[i-1][j+1]==0:
                zero.append([i-1,j+1])
                coveredSet.remove((i-1,j+1))
            else:
                nonzero.append((i-1,j+1))
    
        if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1 and Agent.board[i+1][j+1]==-2:
            Agent.board[i+1][j+1]=Game.mineGrid[i+1][j+1]
            if Agent.board[i+1][j+1]==0:
                zero.append([i+1,j+1])
                coveredSet.remove((i+1,j+1))
            else:
                nonzero.append((i+1,j+1))
    
        if i + 1 <= Agent.dimension - 1 and j - 1 >= 0 and Agent.board[i+1][j-1]==-2:
            Agent.board[i+1][j-1]=Game.mineGrid[i+1][j-1]
            if Agent.board[i+1][j-1]==0:
                zero.append([i+1,j-1])
                coveredSet.remove((i+1,j-1))
            else:
                nonzero.append((i+1,j-1))




        



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


def get_hidden_square(i, j, Agent, hiddenCoordinates=[]):
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


    answerSheet = MineGrid(10, 4)


    agent = AgentBoard(answerSheet.dimension)
    
    #agent.board[0][0]=1
    #agent.board[2][2]=3
    Improved_Agent_GamePlay(answerSheet, agent)


    answerSheet.display()
    agent.display()
    print("Done\n")
    answer = 0
    found = 0
    for x in range(agent.dimension):
        for y in range(agent.dimension):
            if agent.board[x][y] == -3 and answerSheet.mineGrid[x][y] == -1:
                found = found + 1
            if answerSheet.mineGrid[x][y] == -1:
                answer = answer + 1
                
    print(found)
    print(answer)
    print((found / answer))
