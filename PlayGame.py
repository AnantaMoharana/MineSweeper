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
    coveredSet = []
    dimension = Game.dimension

    for i in range(0, dimension):
        for j in range(0, dimension):
            coveredSet.append((i, j))

    while coveredSet:


        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)


       # Check for easy ones not currently part of the clue.

        for x1 in range(0, dimension):
            for y1 in range(0, dimension):
                rev_safe = get_revealed_safe_neighbors(x1, y1, Agent)
                hiddenCords = []
                hidden = get_hidden_square(x1, y1, Agent, hiddenCords)
                neighbors = count_surrounding_spaces(x1, y1, Agent)
                mines = get_surrounding_mines(x1, y1, Agent)
                clue = Agent.board[x1][y1]
                if clue - mines == hidden:  # All hidden are mines
                    markMines(Agent, hiddenCords, coveredSet, [])
                elif neighbors - clue - rev_safe == hidden:  # All hidden are safe
                    for coord in hiddenCords:
                        flip(Game, Agent, coord[0], coord[1], coveredSet)








def Improved_Agent_GamePlay(Game, Agent):
    dimension = Game.dimension

    # Create a set of all the covered spaces
    coveredSet = []
    for i in range(0, dimension):
        for j in range(0, dimension):
            coveredSet.append((i, j))

    base = [] #  elements in form of ([Neighbors], Clue) where Neighbor = (x, y) and Clue = int


    # Pull off a random element to get started
    while coveredSet:

        # 1. Random Selection

        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)

        # Safe square, so = 0. Just remove
        if Agent.board[i][j] >= 0:
            for element in base:
                if (i, j) in element[0]:
                    element[0].remove((i, j))
        elif Agent.board[i][j] == -1:
            for element in base:
                if (i, j) in element[0]:
                    element[0].remove((i, j))
                    element[1] = element[1] - 1




        # Get hidden coordinates
        getHidden = []
        get_hidden_square(i,j, Agent, getHidden)

        # Get mines and clue
        getMines = get_surrounding_mines(i, j, Agent)
        getClue = Agent.board[i][j]

        # Add to knowledge base, hidden neighbors = clue - mines
        base.append((getHidden, getClue - getMines))
        # TODO: TAKE INTERSECTION HERE, AND SEE WHAT WE CAN DEDUCE


        # 2 . Basic Agent (Add to Knowledge Base)

        for x1 in range(0, dimension):
            for y1 in range(0, dimension):
                rev_safe = get_revealed_safe_neighbors(x1, y1, Agent)
                hiddenCords = []
                hidden = get_hidden_square(x1, y1, Agent, hiddenCords)
                neighbors = count_surrounding_spaces(x1, y1, Agent)
                mines = get_surrounding_mines(x1, y1, Agent)
                clue = Agent.board[x1][y1]

                if clue - mines == hidden:  # All hidden are mines
                    markMines(Agent, hiddenCords, coveredSet, [])

                    # Update knowledge base to reflect mines we know as 1 and remove
                    for coordinates in hiddenCords:
                        for element in base:
                            if (coordinates[0], coordinates[1]) in element[0]:
                                element[0].remove((x, y))
                                element[1] = element[1] - 1

                elif neighbors - clue - rev_safe == hidden:  # All hidden are safe
                    for coordinates in hiddenCords:

                        for element in base:
                            if (coordinates[0], coordinates[1]) in element[0]:
                                element[0].remove((x, y))

                        flip(Game, Agent, coordinates[0], coordinates[1], coveredSet)

                        # Get hidden coordinates
                        getHidden = []
                        get_hidden_square(coordinates[0], coordinates[1], Agent, getHidden)

                        # Get mines and clue
                        getMines = get_surrounding_mines(coordinates[0], coordinates[1], Agent)
                        getClue = Agent.board[coordinates[0]][coordinates[1]]

                        # Add to knowledge base, hidden neighbors = clue - mines
                        base.append((getHidden, getClue-getMines))
                        # TODO: TAKE INTERSECTION HERE, AND SEE WHAT WE CAN DEDUCE




        # 3. Advanced Agent (Add to Knowledge Base)

        for element in base:
            if element[1] == 0: # All are safe
                for pair in element[0]:
                    flip(Game, Agent, pair[0], pair[1], coveredSet)
                base.remove(element)
            elif len(element[0]) == element[1]: # All are mines
                markMines(Agent, element[0], coveredSet, visited=[])
                base.remove(element)

            # TODO: COMPARE INTERSECTION HERE, AND SEE WHAT WE CAN DEDUCE








def get_hidden_neighboring_spots(i, j, neighbor_list, Agent):
    if i - 1 >= 0:
        if Agent.board[i - 1][j] == -2:
            neighbor_list.append([i - 1, j])

    if j - 1 >= 0:
        if Agent.board[i][j - 1] == -2:
            neighbor_list.append([i, j - 1])

    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] == -2:
            neighbor_list.append([i + 1, j])

    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] == -2:
            neighbor_list.append([i, j + 1])

    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] == -2:
            neighbor_list.append([i - 1, j - 1])

    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] == -2:
            neighbor_list.append([i - 1, j + 1])

    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i + 1][j + 1] == -2:
            neighbor_list.append([i + 1, j + 1])

    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] == -2:
            neighbor_list.append([i + 1, j - 1])


def get_revealed_safe_non_zero_neighbors(i, j, Agent, set_spots=[]):
    safely_revealed = 0
    if i - 1 >= 0:
        if Agent.board[i - 1][j] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i - 1][j], [i - 1, j]])
    if j - 1 >= 0:
        if Agent.board[i][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i][j - 1], [i, j - 1]])
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i + 1][j], [i + 1, j]])
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i][j + 1], [i, j + 1]])
    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i - 1][j - 1], [i - 1, j - 1]])
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i - 1][j + 1], [i - 1, j + 1]])
    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i + 1][j + 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i + 1][j + 1], [i + 1, j + 1]])
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] > 0:
            safely_revealed = safely_revealed + 1
            set_spots.append([Agent.board[i + 1][j - 1], [i + 1, j - 1]])
    return safely_revealed


def revealed(Game, Agent, spots, coveredSet):
    for item in spots:
        x = item[0]
        y = item[1]
        Agent.board[x][y] = Game.mineGrid[x][y]

        if (x, y) in coveredSet:
            coveredSet.remove((x, y))


# intersection method from geeks for geeks
def intersection(sets):
    while len(sets) > 1:
        lst1 = sets.pop()
        lst2 = sets.pop()
        lst3 = [value for value in lst1 if value in lst2]
        sets.append(lst3)


# Helper methods
def get_neighboring_spots(i, j, neighbor_list, Agent):
    if i - 1 >= 0:
        neighbor_list.append([i - 1, j])

    if j - 1 >= 0:
        neighbor_list.append([i, j - 1])

    if i + 1 < Agent.dimension:
        neighbor_list.append([i + 1, j])

    if j + 1 < Agent.dimension:
        neighbor_list.append([i, j + 1])

    if i - 1 >= 0 and j - 1 >= 0:
        neighbor_list.append([i - 1, j - 1])

    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        neighbor_list.append([i - 1, j + 1])

    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        neighbor_list.append([i + 1, j + 1])

    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        neighbor_list.append([i + 1, j - 1])


def reveal_safe_zeros(Agent, Game, zero, coveredSet, nonzero):
    while zero:
        xfirst = random.choices(zero)
        xfirst = xfirst[0]
        zero.remove(xfirst)

        # print(xfirst)

        i = xfirst[0]
        j = xfirst[1]

        if i - 1 >= 0 and Agent.board[i - 1][j] == -2:
            Agent.board[i - 1][j] = Game.mineGrid[i - 1][j]
            if Agent.board[i - 1][j] == 0:
                zero.append([i - 1, j])
                coveredSet.remove((i - 1, j))
            else:
                safety = []
                safe_non_zero_neihgbors = get_revealed_safe_non_zero_neighbors(i - 1, j, Agent, safety)
                #print(safe_non_zero_neihgbors)
                nonzero[(i - 1, j)] = Agent.board[i - 1][j]
                coveredSet.remove((i - 1, j))

        if j - 1 >= 0 and Agent.board[i][j - 1] == -2:
            Agent.board[i][j - 1] = Game.mineGrid[i][j - 1]
            if Agent.board[i][j - 1] == 0:
                zero.append([i, j - 1])
                coveredSet.remove((i, j - 1))
            else:
                nonzero[(i, j - 1)] = Agent.board[i][j - 1]
                coveredSet.remove((i, j - 1))

        if i + 1 < Agent.dimension and Agent.board[i + 1][j] == -2:
            Agent.board[i + 1][j] = Game.mineGrid[i + 1][j]
            if Agent.board[i + 1][j] == 0:
                zero.append([i + 1, j])
                coveredSet.remove((i + 1, j))
            else:
                nonzero[(i + 1, j)] = Agent.board[i + 1][j]
                coveredSet.remove((i + 1, j))

        if j + 1 < Agent.dimension and Agent.board[i][j + 1] == -2:
            Agent.board[i][j + 1] = Game.mineGrid[i][j + 1]
            if Agent.board[i][j + 1] == 0:
                zero.append([i, j + 1])
                coveredSet.remove((i, j + 1))
            else:
                nonzero[(i, j + 1)] = Agent.board[i][j + 1]
                coveredSet.remove((i, j + 1))

        if i - 1 >= 0 and j - 1 >= 0 and Agent.board[i - 1][j - 1] == -2:
            Agent.board[i - 1][j - 1] = Game.mineGrid[i - 1][j - 1]
            if Agent.board[i - 1][j - 1] == 0:
                zero.append([i - 1, j - 1])
                coveredSet.remove((i - 1, j - 1))
            else:
                nonzero[(i - 1, j - 1)] = Agent.board[i - 1][j - 1]
                coveredSet.remove((i - 1, j - 1))

        if i - 1 >= 0 and j + 1 <= Agent.dimension - 1 and Agent.board[i - 1][j + 1] == -2:
            Agent.board[i - 1][j + 1] = Game.mineGrid[i - 1][j + 1]
            if Agent.board[i - 1][j + 1] == 0:
                zero.append([i - 1, j + 1])
                coveredSet.remove((i - 1, j + 1))
            else:
                nonzero[(i - 1, j + 1)] = Agent.board[i - 1][j + 1]
                coveredSet.remove((i - 1, j + 1))

        if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1 and Agent.board[i + 1][j + 1] == -2:
            Agent.board[i + 1][j + 1] = Game.mineGrid[i + 1][j + 1]
            if Agent.board[i + 1][j + 1] == 0:
                zero.append([i + 1, j + 1])
                coveredSet.remove((i + 1, j + 1))
            else:
                nonzero[(i + 1, j + 1)] = Agent.board[i + 1][j + 1]
                coveredSet.remove((i + 1, j + 1))

        if i + 1 <= Agent.dimension - 1 and j - 1 >= 0 and Agent.board[i + 1][j - 1] == -2:
            Agent.board[i + 1][j - 1] = Game.mineGrid[i + 1][j - 1]
            if Agent.board[i + 1][j - 1] == 0:
                zero.append([i + 1, j - 1])
                coveredSet.remove((i + 1, j - 1))
            else:
                nonzero[(i + 1, j - 1)] = Agent.board[i + 1][j - 1]
                coveredSet.remove((i + 1, j - 1))


def flip(Game, Agent, x, y, coveredSet):

    Agent.board[x][y] = Game.mineGrid[x][y]

    if Agent.board[x][y] == 0:
        hidden = []
        get_hidden_neighboring_spots(x, y, hidden, Agent)

        for cords in hidden:
            flip(Game, Agent, cords[0], cords[1], coveredSet)


def markMines(Agent, hidden, coveredSet=[], visited=[]):
    for xy in hidden:
        Agent.board[xy[0]][xy[1]] = -3
        if (xy[0], xy[1]) in coveredSet:
            coveredSet.remove((xy[0], xy[1]))
        visited.append([xy[0], xy[1]])


def pickRandomSquare(Game, Agent, coveredSet):
    xfirst = random.choices(coveredSet)
    xfirst = xfirst[0]
    coveredSet.remove(xfirst)

    # print(xfirst)

    x = xfirst[0]
    y = xfirst[1]

    flip(Game, Agent, x, y, coveredSet)

    return x, y, coveredSet


def get_revealed_safe_neighbors(i, j, Agent, set_spots=[]):
    safely_revealed = 0
    if i - 1 >= 0:
        if Agent.board[i - 1][j] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i - 1][j], [i - 1, j]))
    if j - 1 >= 0:
        if Agent.board[i][j - 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i][j - 1], [i, j - 1]))
    if i + 1 < Agent.dimension:
        if Agent.board[i + 1][j] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i + 1][j], [i + 1, j]))
    if j + 1 < Agent.dimension:
        if Agent.board[i][j + 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i][j + 1], [i, j + 1]))
    if i - 1 >= 0 and j - 1 >= 0:
        if Agent.board[i - 1][j - 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i - 1][j - 1], [i - 1, j - 1]))
    if i - 1 >= 0 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i - 1][j + 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i - 1][j + 1], [i - 1, j + 1]))
    if i + 1 <= Agent.dimension - 1 and j + 1 <= Agent.dimension - 1:
        if Agent.board[i + 1][j + 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i + 1][j + 1], [i + 1, j + 1]))
    if i + 1 <= Agent.dimension - 1 and j - 1 >= 0:
        if Agent.board[i + 1][j - 1] >= 0:
            safely_revealed = safely_revealed + 1
            set_spots.append((Agent.board[i + 1][j - 1], [i + 1, j - 1]))
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
    # Graph parameters
    density = [.1, .2, .3, .4, .5, .6, .7, .8]
    runsPerD = 10
    dim = 12
    successRateBasic = [0] * len(density)
    successRateAdvanced = [0] * len(density)
    for i in range(len(density)):
        for j in range(runsPerD):
            print("density ", density[i], " run # ", j)
            answerSheet = MineGrid(dim, int(dim*dim*density[i]))
            #answerSheet.display()
            agent = AgentBoard(dim)
            Basic_Agent_GamePlay(answerSheet, agent)
            answer = 0
            found = 0
            for x in range(agent.dimension):
                for y in range(agent.dimension):
                    if agent.board[x][y] == -3 and answerSheet.mineGrid[x][y] == - 1:
                        found = found + 1
                    if answerSheet.mineGrid[x][y] == -1:
                        answer = answer + 1
            successRateBasic[i] = successRateBasic[i] + (found / answer)


            agent = AgentBoard(dim)
            Improved_Agent_GamePlay(answerSheet, agent)
            answer = 0
            found = 0
            for x in range(agent.dimension):
                for y in range(agent.dimension):
                    if agent.board[x][y] == -3 and answerSheet.mineGrid[x][y] == - 1:
                        found = found + 1
                    if answerSheet.mineGrid[x][y] == -1:
                        answer = answer + 1
            successRateAdvanced[i] = successRateAdvanced[i] + (found / answer)


        successRateBasic[i] = 100 * successRateBasic[i]/runsPerD
        successRateAdvanced[i] = 100 * successRateAdvanced[i] / runsPerD
    plt.plot(density, successRateBasic)
    plt.plot(density, successRateAdvanced)
    plt.legend(['Basic Agent', 'M.I.S.S.L.E'])
    plt.title("Basic vs Advanced Agents")
    plt.ylabel('percentage of mines correctly flagged and defused')
    plt.xlabel('Mine Density')
    plt.show()
