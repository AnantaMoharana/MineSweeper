import random
import matplotlib.pyplot as plt
import warnings
from main import AgentBoard
from main import MineGrid
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)


# GAME BOARD: -1 = MINE, 0-9 = CLUE
# AGENT BOARD: -3 = FLAGGED MINE, -2 = COVERED, -1 = BLOWN UP MINE, 0-9 = CLUE



def Basic_Agent_GamePlay(Game, Agent):
   # Just follow the basic algorithmic implementation

    coveredSet=[]
    dimension=Game.dimension

    # Make a list of all 'covered' (unvisited) squares

    for i in range(0,dimension):
        for j in range(0,dimension):
            coveredSet.append((i,j))

    visited=[]

    # While we still have squares to visit
    while coveredSet:
        # Flip a random square to start us off
        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)

        visited.append([i,j])

        # Loop over every one we have seen thus far to see if we can find something
        for cord in visited:
            x=cord[0]
            y=cord[1]

            # Use the helper functions to find relevant clues and information

            rev_safe = get_revealed_safe_neighbors(x, y, Agent)

            hiddenCords = []
            hidden = get_hidden_square(x, y, Agent, hiddenCords)

            neighbors = count_surrounding_spaces(x, y, Agent)

            mines = get_surrounding_mines(x, y, Agent)
            clue = Agent.board[x][y]

            if clue - mines == hidden:  # All hidden are mines, mark them on the Agent board as such
                markMines(Agent, hiddenCords, coveredSet,visited)

            elif neighbors-clue-rev_safe == hidden:  # All hidden are safe, mark them on Agent board as such
                for coord in hiddenCords:
                    flip(Game, Agent, coord[0], coord[1], coveredSet)


def Improved_Agent_GamePlay(Game, Agent):
    dimension = Game.dimension

    # Create a set of all the covered spaces
    coveredSet = []
    for i in range(0, dimension):
        for j in range(0, dimension):
            coveredSet.append((i, j))

    #  elements in knowledge base are in form of ([Neighbors], Clue) where neighbor = (pos x, pos y) and Clue = int
    base = []

    # Pull off a random element to get started
    while coveredSet or not done(Agent):

        # 1. Random Selection
        i, j, coveredSet = pickRandomSquare(Game, Agent, coveredSet)
         
        if i == j == 0 and not coveredSet:
            return

        # Safe square, so variable must be = 0. Just remove var from equations, no need to subtract
        if Agent.board[i][j] >= 0:
            for element in base:
                if (i, j) in element[0]:
                    element[0].remove((i, j))

        # Mine square, so variable must be = 1. Remove var from all equations and subtract 1 from their clue
        elif Agent.board[i][j] == -1 or Agent.board[i][j] == -3:
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

        # Knowledge Base work
        for item in base:
            isSubset, newList, newClue = difference(item, (getHidden, getClue - getMines))

            if isSubset:

                if newClue == 0:  # All safe, add to base and flip
                    for y in newList:
                        flip(Game, Agent, y[0], y[1], coveredSet)
                        for element in base:
                            if (y[0], y[1]) in element[0]:
                                element[0].remove((y[0], y[1]))

                elif len(newList) == newClue:  # All mines, add to base and mark
                    markMines(Agent, newList, coveredSet, visited=[])
                    for y in newList:
                        for element in base:
                            if (y[0], y[1]) in element[0]:
                                element[0].remove((y[0], y[1]))
                                element[1] = element[1] - 1


        # 2 . Basic Agent as a base for the algorithm. (Add to Knowledge Base)
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
                                element[0].remove((x1, y1))
                                element[1] = element[1] - 1

                elif neighbors - clue - rev_safe == hidden:  # All hidden are safe
                    for coordinates in hiddenCords:

                        for element in base:
                            if (coordinates[0], coordinates[1]) in element[0]:
                                element[0].remove((x1, y1))

                        flip(Game, Agent, coordinates[0], coordinates[1], coveredSet)

                        # Get hidden coordinates
                        getHidden = []
                        get_hidden_square(coordinates[0], coordinates[1], Agent, getHidden)

                        # Get mines and clue
                        getMines = get_surrounding_mines(coordinates[0], coordinates[1], Agent)
                        getClue = Agent.board[coordinates[0]][coordinates[1]]

                        # Add to knowledge base, hidden neighbors = clue - mines
                        base.append((getHidden, getClue-getMines))

                        # Knowledge Base work
                        for k in base:
                            isSubset, newList, newClue = difference(k, (getHidden, getClue-getMines))

                            if isSubset:

                                if newClue == 0: # All safe
                                    for y in newList:
                                        flip(Game, Agent, y[0], y[1], coveredSet)
                                        for element in base:
                                            if (y[0], y[1]) in element[0]:
                                                element[0].remove((y[0], y[1]))
                                elif len(newList) == newClue: # All mines
                                    markMines(Agent, newList, coveredSet, visited=[])
                                    for y in newList:
                                        for element in base:
                                            if (y[0], y[1]) in element[0]:
                                                element[0].remove((y[0], y[1]))
                                                element[1] = element[1] - 1

        # 3. Advanced Agent (Add to Knowledge Base)

        for element in base:
            if element[1] == 0: # All are safe
                for pair in element[0]:
                    flip(Game, Agent, pair[0], pair[1], coveredSet)
                base.remove(element)
            elif len(element[0]) == element[1]: # All are mines
                markMines(Agent, element[0], coveredSet, visited=[])
                base.remove(element)

            # Knowledge Base work
            for k in base:
                isSubset, newList, newClue = difference(k, (getHidden, getClue - getMines))
                if isSubset:

                    if newClue == 0:  # All safe, mark as such
                        for y in newList:
                            flip(Game, Agent, y[0], y[1], coveredSet)
                            for elements in base:
                                if (y[0], y[1]) in elements[0]:
                                    elements[0].remove((y[0], y[1]))

                    elif len(newList) == newClue:  # All mines, mark as such
                        markMines(Agent, newList, coveredSet, visited=[])
                        for y in newList:
                            for elements in base:
                                if (y[0], y[1]) in elements[0]:
                                    elements[0].remove((y[0], y[1]))
                                    elements[1] = elements[1] - 1


def done(Agent):
    for x in range(0, Agent.dimension):
        for y in range(0, Agent.dimension):
            if Agent.board[x][y] == -2:
                return False
    return True


def difference(element1, element2):
    clue1 = element1[1]
    clue2 = element2[1]
    difference = []

    for item in element2[0]:
        if item not in element1[0]:
            difference.append(item)



    # Check if element1 is a subset of element2
    isSubset = True
    for item in element1[0]:
        try:
            element2[0].index(item)
        except ValueError:
            isSubset = False
            break

    return isSubset, difference, (clue2 - clue1)


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


def getNumHidden(Agent):
    count = 0
    for x in range(0, Agent.dimension):
        for y in range(0, Agent.dimension):
            if Agent.board[x][y] == -2:
                count = count + 1
    return count



def pickRandomBONUS(Game, Agent, coveredSet):

    # Get random probability that ANY hidden box is a mine
    if getNumHidden(Agent) == 0:
        return 0, 0, []

    prob = Game.numberOfMines / getNumHidden(Agent)


    bonus = [[prob] * Agent.dimension for _ in range(Agent.dimension)]

    for i in range(0, Agent.dimension):
        for j in range(0, Agent.dimension):
            if Agent.board[i][j] == -3 or Agent.board[i][j] == -1:
                bonus[i][j] = 1.02
            elif Agent.board[i][j] >= 0:
                bonus[i][j] = 1.01

                neighborList = []
                get_neighboring_spots(i, j, neighborList, Agent)
                num_neighbors = len(neighborList)


                num_mines = get_surrounding_mines(i, j, Agent)

                neighborList = []
                get_hidden_neighboring_spots(i, j, neighborList, Agent)

                clue = Agent.board[i][j]

                for item in neighborList:
                    if Agent.board[item[0]][item[1]] == -2:
                        prev = bonus[item[0]][item[1]]

                        curr = (clue - num_mines) / num_neighbors

                        if prev > curr:
                            bonus[item[0]][item[1]] = curr

    getMin = np.array(bonus)
    minElement = getMin.min()

    indexes = []


    if minElement > 1.00:
        return 0, 0, []

    for i in range(0, Agent.dimension):
        for j in range(0, Agent.dimension):
            if bonus[i][j] == minElement:
                indexes.append((i, j))


    xfirst = random.choices(indexes)
    xfirst = xfirst[0]

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
    density = [.1, .2, .3, .4, .5]
    runsPerD = 10
    dim = 10
    successRateBasic = [0] * len(density)
    successRateAdvanced = [0] * len(density)
    for i in range(len(density)):
        for j in range(runsPerD):
            print("density ", density[i], " run # ", j)
            answerSheet = MineGrid(dim, int(dim*dim*density[i]))
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
