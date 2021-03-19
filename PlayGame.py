import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings
from main import AgentBoard
from main import MineGrid
from operator import itemgetter as i

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

    #visited = []
    zero=[]
    #mine_sets=[]
    #sets_list=[]
    nonzero={}
    # Pull off a random element to get started
    while coveredSet:
        #Agent.display()
        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)
        #i,j=4,8
        #Agent.board[i][j]=Game.mineGrid[i][j]
        #coveredSet.remove((i,j))

        neighbor_list=[]
        if Agent.board[i][j]==0:
            zero.append((i,j))

            reveal_safe_zeros(Agent,Game,zero,coveredSet,nonzero)
            Agent.display()
            for key in nonzero:
                mine=nonzero[key]
                safe_non_zero_neihgbors=get_revealed_safe_non_zero_neighbors(key[0],key[1],Agent)
                nonzero[key]=[mine,safe_non_zero_neihgbors]
            #nonzero={k: v for k, v in sorted(nonzero.items(), key=lambda item: item[1][0])}
            #nonzero={k: v for k, v in sorted(nonzero.items(), key=lambda item: item[1][1])}
            nonzero={k: v for k, v in sorted(nonzero.items(), key=lambda item: (item[1][0],-item[1][1]))}
            spots_to_visit=list(nonzero)
            while nonzero:
                if len(spots_to_visit)<=0:
                    #nonzero.clear()
                    break

                spot=spots_to_visit.pop(0)
                if spot not in nonzero:
                    continue
                print(spot)
                #spot=(4,7)
                if spot in coveredSet:
                    coveredSet.remove(spot)
                

                neighbor_list=[]
                get_revealed_safe_non_zero_neighbors(spot[0],spot[1],Agent,neighbor_list)

                for item in neighbor_list:
                    if (item[1][0],item[1][1]) not in list(nonzero):
                        neighbor_list.remove(item)




                sets=[]
                spots_set=[]
                get_hidden_neighboring_spots(spot[0],spot[1],spots_set,Agent)
                sets.append(spots_set)
                for item in neighbor_list:
                    set_items=[]
                    get_hidden_neighboring_spots(item[1][0],item[1][1],set_items,Agent)
                    sets.append(set_items)


                if len(sets)>2: #2 # recheck this shit
                    intersection(sets)
                    sets=sets.pop()
                    for i in range (len(sets)):
                        copy=(sets[i][0],sets[i][1])
                        if copy not in coveredSet:
                            copy=[sets[i][0],sets[i][1]]
                            sets.remove(copy)
                else:
                    continue

                for spot2 in sets:
                    Agent.board[spot2[0]][spot2[1]]=-3
                    if (spot2[0], spot2[1]) in coveredSet:
                        coveredSet.remove((spot2[0], spot2[1]))
                    neighbors=[]
                    get_revealed_safe_non_zero_neighbors(spot2[0],spot2[1],Agent,neighbors)

                    for neighbor in neighbors:
                        if (neighbor[1][0],neighbor[1][1])  in list(nonzero):
                            nonzero[(neighbor[1][0],neighbor[1][1])][0]=nonzero[(neighbor[1][0],neighbor[1][1])][0]-1
                            #updating

                #if there are no bombs surrounding the spot reveal all of its hidden spots 
                key_to_remove=[]
                for key in nonzero.keys():
                    if nonzero[key][0]==0:
                        key_to_remove.append(key)
                

                while key_to_remove:

                    remove=key_to_remove.pop()
                    if remove in spots_to_visit:
                        spots_to_visit.remove(remove)
                    safe=[]
                    get_hidden_neighboring_spots(remove[0],remove[1],safe,Agent)

                    for spot in safe:
                        Agent.board[spot[0]][spot[1]]=Game.mineGrid[spot[0]][spot[1]]
                        #add the new spot to the list
#
                            #fill this out and then go to bed


                        if (spot[0],spot[1]) in coveredSet:
                            coveredSet.remove((spot[0],spot[1]))

                        mines=get_surrounding_mines(spot[0],spot[1],Agent)
                        safe_neighbors=get_revealed_safe_non_zero_neighbors(spot[0],spot[1],Agent)
                        nonzero[(spot[0],spot[1])]=[Agent.board[spot[0]][spot[1]]-mines,safe_neighbors]

                        if nonzero[(spot[0],spot[1])][0]==0:
                            key_to_remove.append((spot[0],spot[1]))
                        nonzero={k: v for k, v in sorted(nonzero.items(), key=lambda item: item[1])}
                        spots_to_visit=list(nonzero)
                        

                    #spots_to_visit.remove(remove)
                    nonzero.pop(remove)

                        

                Agent.display()
        else: # if the spot we reveal is not zero
            if Agent.board[i][j]==-1:
                print("Ouch")
                #break
                #coveredSet.remove((i,j))
            nonzero[(i,j)]=Agent.board[i][j]
            print("non-zero")
            print((i,j))

            Agent.display()




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
            set_spots.append([Agent.board[i-1][j],[i-1,j]])
    if j - 1 >= 0:
        if Agent.board[i][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i][j-1],[i,j-1]])
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i+1][j],[i+1,j]])
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i][j+1],[i,j+1]])
    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i-1][j-1],[i-1,j-1]])
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i-1][j+1],[i-1,j+1]])
    if i+1<=Agent.dimension-1 and j+1<=Agent.dimension-1:
        if Agent.board[i + 1][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i+1][j+1],[i+1,j+1]])
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i+1][j-1],[i+1,j-1]])
    return safely_revealed  



def revealed(Game,Agent, spots, coveredSet):
    for item in spots:
        x=item[0]
        y=item[1]
        Agent.board[x][y]=Game.mineGrid[x][y]

        if(x,y) in coveredSet:
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
                safety=[]
                safe_non_zero_neihgbors=get_revealed_safe_non_zero_neighbors(i-1,j,Agent,safety)
                print(safe_non_zero_neihgbors)
                nonzero[(i-1,j)]=Agent.board[i-1][j]
                coveredSet.remove((i-1,j))

   
        if j - 1 >= 0 and Agent.board[i][j-1]==-2:
            Agent.board[i][j-1]=Game.mineGrid[i][j-1]
            if Agent.board[i][j-1]==0:
                zero.append([i,j-1])
                coveredSet.remove((i,j-1))
            else:
                nonzero[(i,j-1)]=Agent.board[i][j-1]
                coveredSet.remove((i,j-1))
    
        if i + 1 < Agent.dimension and Agent.board[i+1][j]==-2:
            Agent.board[i+1][j]=Game.mineGrid[i+1][j]
            if Agent.board[i+1][j]==0:
                zero.append([i+1,j])
                coveredSet.remove((i+1,j))
            else:
                nonzero[(i+1,j)]=Agent.board[i+1][j]
                coveredSet.remove((i+1,j))
    
        if j + 1 < Agent.dimension and Agent.board[i][j+1]==-2:
            Agent.board[i][j+1]=Game.mineGrid[i][j+1]
            if Agent.board[i][j+1]==0:
                zero.append([i,j+1])
                coveredSet.remove((i,j+1))
            else:
                nonzero[(i,j+1)]=Agent.board[i][j+1]
                coveredSet.remove((i,j+1))
   
        if i - 1 >= 0 and j - 1 >= 0 and Agent.board[i-1][j-1]==-2:
            Agent.board[i-1][j-1]=Game.mineGrid[i-1][j-1]
            if Agent.board[i-1][j-1]==0:
                zero.append([i-1,j-1])
                coveredSet.remove((i-1,j-1))
            else:
                nonzero[(i-1,j-1)]=Agent.board[i-1][j-1]
                coveredSet.remove((i-1,j-1))
    
        if i - 1 >= 0 and j + 1 <= Agent.dimension - 1 and Agent.board[i-1][j+1]==-2:
            Agent.board[i-1][j+1]=Game.mineGrid[i-1][j+1]
            if Agent.board[i-1][j+1]==0:
                zero.append([i-1,j+1])
                coveredSet.remove((i-1,j+1))
            else:
                nonzero[(i-1,j+1)]=Agent.board[i-1][j+1]
                coveredSet.remove((i-1,j+1))
    
        if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1 and Agent.board[i+1][j+1]==-2:
            Agent.board[i+1][j+1]=Game.mineGrid[i+1][j+1]
            if Agent.board[i+1][j+1]==0:
                zero.append([i+1,j+1])
                coveredSet.remove((i+1,j+1))
            else:
                nonzero[(i+1,j+1)]=Agent.board[i+1][j+1]
                coveredSet.remove((i+1,j+1))
    
        if i + 1 <= Agent.dimension - 1 and j - 1 >= 0 and Agent.board[i+1][j-1]==-2:
            Agent.board[i+1][j-1]=Game.mineGrid[i+1][j-1]
            if Agent.board[i+1][j-1]==0:
                zero.append([i+1,j-1])
                coveredSet.remove((i+1,j-1))
            else:
                nonzero[(i+1,j-1)]=Agent.board[i+1][j-1]
                coveredSet.remove((i+1,j-1))




        
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
    #answerSheet.mineGrid[0][2]=1
    #answerSheet.mineGrid[0][3]= -1   
    #answerSheet.mineGrid[0][4]=-1
    #answerSheet.mineGrid[0][5]=1
#
    #answerSheet.mineGrid[1][1]=1
    #answerSheet.mineGrid[1][2]=3
    #answerSheet.mineGrid[1][3]=4
    #answerSheet.mineGrid[1][4]=3
    #answerSheet.mineGrid[1][5]=1
    #answerSheet.mineGrid[1][7]=1
    #answerSheet.mineGrid[1][8]=1
    #answerSheet.mineGrid[1][9]=1
#
    #answerSheet.mineGrid[2][1]=1
    #answerSheet.mineGrid[2][2]=-1
    #answerSheet.mineGrid[2][3]=-1
    #answerSheet.mineGrid[2][4]=2
    #answerSheet.mineGrid[2][5]=1
    #answerSheet.mineGrid[2][7]=1
    #answerSheet.mineGrid[2][8]=-1
    #answerSheet.mineGrid[2][9]=1
#
    #answerSheet.mineGrid[3][1]=1
    #answerSheet.mineGrid[3][2]=2
    #answerSheet.mineGrid[3][3]=3
    #answerSheet.mineGrid[3][4]=-1
    #answerSheet.mineGrid[3][5]=1
    #answerSheet.mineGrid[3][7]=1
    #answerSheet.mineGrid[3][8]=1
    #answerSheet.mineGrid[3][9]=1
#
    #answerSheet.mineGrid[4][3]=2
    #answerSheet.mineGrid[4][4]=2
    #answerSheet.mineGrid[4][5]=2
    #answerSheet.mineGrid[4][7]=1
    #answerSheet.mineGrid[4][8]=1
    #answerSheet.mineGrid[4][9]=1
#
    #answerSheet.mineGrid[5][3]=1
    #answerSheet.mineGrid[5][4]=-1
    #answerSheet.mineGrid[5][5]=1
    #answerSheet.mineGrid[5][7]=1
    #answerSheet.mineGrid[5][8]=-1
    #answerSheet.mineGrid[5][9]=1
#
    #answerSheet.mineGrid[6][3]=1
    #answerSheet.mineGrid[6][4]=1
    #answerSheet.mineGrid[6][5]=2
    #answerSheet.mineGrid[6][6]=1
    #answerSheet.mineGrid[6][7]=2
    #answerSheet.mineGrid[6][8]=1
    #answerSheet.mineGrid[6][9]=1
#
    #answerSheet.mineGrid[7][5]=2
    #answerSheet.mineGrid[7][6]=-1
    #answerSheet.mineGrid[7][7]=2
#
    #answerSheet.mineGrid[8][0]=1
    #answerSheet.mineGrid[8][1]=1
    #answerSheet.mineGrid[8][5]=2
    #answerSheet.mineGrid[8][6]=-1
    #answerSheet.mineGrid[8][7]=2
#
    #answerSheet.mineGrid[9][0]=-1
    #answerSheet.mineGrid[9][1]=1
    #answerSheet.mineGrid[9][5]=1
    #answerSheet.mineGrid[9][6]=1
    #answerSheet.mineGrid[9][7]=1
#
    answerSheet.display()
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
