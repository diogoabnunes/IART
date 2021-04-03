from math import *
import functools
import random
import heapq


#######################################################################################################################
######################################## GERENAL USE UTILITIES ########################################################
#######################################################################################################################


def distance(pointA, pointB):
    """
    Calculates the distance between 2 points.
    """
    return sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)


def setGridContent(grid, content, x, y=None):
    """
   Changes the content of a grid position.
   """
    try:
        if type(x) == tuple:
            grid[x[0]][x[1]] = content
            return
        grid[x][y] = content
        return
    except IndexError:
        return None


def compareLists(l1, l2):
    """
    Compares the content of 2 lists.
    """
    if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, l1, l2), True):
        return True
    else:
        return False


def printGrid(grid):
    """
    Prints the actual grid with the actual content.
    """
    rowsInStr = []
    for row in grid:
        rowsInStr.append(''.join(row))
    gridStr = '\n'.join(rowsInStr)
    print(f"Blueprint:\n{gridStr}")


#######################################################################################################################
########################################### SOLUTION UTILITIES ########################################################
#######################################################################################################################


def value(blueprint, solution):  # also checks if solution is valid
    """
    Calculates and returns the value of a solution.
    """
    t = len(blueprint.getSolutionCoveredCells(solution))  # t = number of cells covered by wireless connection
    N = len(blueprint.accessMstPathsDict(solution))  # N = Number of cells connected to the backbone
    M = routersPlaced(solution)  # M = Number of routers
    remainingBudget = blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)
    if remainingBudget < 0:
        return None
    return 1000 * t + remainingBudget


def remainingBudget(blueprint, solution):  # also checks if solution is valid
    """
   Calculates and returns the value of a solution.
   """
    t = len(blueprint.getSolutionCoveredCells(solution))  # t = Number of cells covered by wireless connection
    N = len(blueprint.accessMstPathsDict(solution))  # N = Number of cells connected to the backbone
    M = routersPlaced(solution)  # M = Number of routers
    return blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)


def routersPlaced(solution) -> int:
    """
   Calculates the number of routers placed in a solution ((-1, -1) could be in a solution,
   symbolizing that the budget could have more routers, but these solution uses less routers).
   """
    counter = 0
    for router in solution:
        if router != (-1, -1):  # if the router is used
            counter += 1
    return counter


def checkSolutionDuplicates(solution):
    """
   Checks if a solution has 2 or more routers in a solution (duplicates).
   """
    aux = []
    for router in solution:
        if router != (-1, -1): # if the router is used
            aux.append(router)
    return len(aux) != len(set(aux))


def validSolution(blueprint, solution):  # doesn't check budget
    """
    Checks if a solution doesn't have duplicates and every router is in a valid position (not in a wall position).
    """
    if checkSolutionDuplicates(solution):
        return False
    for router in solution:
        if not blueprint.validPosition(router):
            return False
    return True


def generateMaxRoutersSolution(blueprint):
    """
    Generates a solution using the maximum number of routers.
    """
    solution = []
    auxList = [0] * blueprint.getMaxRouters()  # Creation of an auxiliary list with the size being the max number of available routers
    for i in auxList:
        x = random.randint(0, blueprint.height - 1)
        y = random.randint(0, blueprint.width - 1)  # Generate a random router
        if not blueprint.validPosition(x, y) or not blueprint.notVoid(x, y):  # Check if the created router is in a valid position and in a void cell
            auxList.append(i)
            continue
        solution.append((x, y))  # Add the created router to the solution
    return solution


def generateSolution(blueprint):
    """
    Generates a solution using the maximum number of routers,
    given the path to all routers and the budget available
    :param blueprint:
    :return: Returns the created solution
    """

    individualSol = []
    positionsAdded = {}
    while True:
        for j in range(blueprint.getMaxRouters()):
            rand = random.randint(0, len(blueprint.validPositions) - 1)

            while True:
                try:
                    positionsAdded[rand]
                except KeyError:
                    break
                rand = random.randint(0, len(blueprint.validPositions) - 1)
                continue

            individualSol.append(blueprint.validPositions[rand])
            positionsAdded[rand] = True

            if blueprint.targetCoveredCells == len(blueprint.getSolutionCoveredCells(individualSol)):
                while len(individualSol) < blueprint.getMaxRouters():
                    individualSol.append((-1, -1))
                break

            if value(blueprint, individualSol) is None:
                individualSol.pop()
                while len(individualSol) < blueprint.getMaxRouters():
                    individualSol.append((-1, -1))
                break

        return individualSol


def getIndexOfLastNonEmptyRouter(solution) -> int:
    """
    Returns the index of the first router position "null" (when we don't need all possible routers to 1 solution.
    """
    for i in range(0, len(solution)):
        if solution[-(i + 1)] != (-1, -1):
            return len(solution) - i - 1


def randomNeighbour(blueprint, solution: list, remove=False):  # can return an infeasible solution
    """
    Given a solution, returns a random neighbour and the respective value.
    """

    routerChange = random.randint(0, getIndexOfLastNonEmptyRouter(solution))

    while True:
        upOrDownX = random.randint(-1, 1)
        upOrDownY = random.randint(-1, 1)
        if upOrDownX == 0 and upOrDownY == 0:
            continue
        break

    neighbour = solution.copy()

    if remove:
        lastIx = getIndexOfLastNonEmptyRouter(neighbour)
        neighbour[routerChange] = neighbour[lastIx]
        neighbour[lastIx] = (-1, -1)
    else:
        neighbour[routerChange] = (neighbour[routerChange][0] + upOrDownX, neighbour[routerChange][1] + upOrDownY)

    if not validSolution(blueprint, neighbour):
        return None, None
    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None:
        return None, None
    return neighbour, neighbourValue


def neighbour(blueprint, solution, routerToChange, coordToChange, upOrDown, numRouters, calcValue = True):
    """
    :param blueprint: Problem blueprint.
    :param solution: Initial solution.
    :param routerToChange: index, between 0 and number of router in the solution
    :param coordToChange: 0 or 1, 0 changes x, 1 changes y
    :param upOrDown: 1 increments, 0 decrements, -1 makes the router at routerToChange (-1, -1)
    :param numRouters: if it's lower than the number of routers in the solution, removes the worst router
    :return: The pretended neighbour and his value.
    """
    
    if solution is None:
        return None, None
    
    neighbour = solution.copy()

    if numRouters - 1 < routerToChange:
        raise RuntimeError("numRouters < routerToChange")

    add = 0
    if upOrDown == 1:
        add = 1
    elif upOrDown == 0:
        add = -1

    if upOrDown == -1:
        lastIx = getIndexOfLastNonEmptyRouter(neighbour)
        neighbour[routerToChange] = neighbour[lastIx]
        neighbour[lastIx] = (-1, -1)
    else:
        if coordToChange == 0:
            neighbour[routerToChange] = (neighbour[routerToChange][0] + add, neighbour[routerToChange][1])
        elif coordToChange == 1:
            neighbour[routerToChange] = (neighbour[routerToChange][0], neighbour[routerToChange][1] + add)

    if not validSolution(blueprint, neighbour):
        return None, None

    routersToRemove = routersPlaced(solution) - numRouters
    if routersToRemove >= 0:
        lastIx = getIndexOfLastNonEmptyRouter(neighbour)
        for i in range(routersToRemove):
            toRemove = random.randint(0, lastIx - 1)
            neighbour[toRemove] = neighbour[lastIx]
            neighbour[lastIx] = (-1, -1)
            lastIx -= 1
            if lastIx == -1:
                break
    if calcValue:
        neighbourValue = value(blueprint, neighbour)
        if neighbourValue is None:
            return None, None
        return neighbour, neighbourValue
    else:
        return neighbour

def orderRouters(solution):
    """
    Given a solution, puts all the (-1, -1) routers in the end of the list (not needed all the routers).
    """
    toLast, newSol = [], []

    for router in solution:
        if router != (-1, -1):
            newSol.append(router)
        else:
            toLast.append(router)

    for router in toLast:
        newSol.append(router)

    return newSol


def printSolToFile(solution, time, blueprint, filename):
    """
    Prints a solution information to a file.
    """
    with open(filename, "w") as file:
        file.write("Solution value: " + str(value(blueprint, solution)) + "\n")
        file.write("Remaining budget: " + str(remainingBudget(blueprint, solution)) + "\n")
        file.write("Execution time: " + str(time) + "s\n")
        file.write("\n")
        for router in solution:
            file.write(str(router) + "\n")
