from math import *
import functools
import random
import heapq

#######################################################################################################################
######################################## GERENAL USE UTILITIES ########################################################
#######################################################################################################################

def distance(pointA, pointB):
    return sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)

def setGridContent(grid, content, x, y=None):
    try:
        if type(x) == tuple:
            grid[x[0]][x[1]] = content
            return
        grid[x][y] = content
        return
    except IndexError:
        return None

def compareLists(l1, l2):
    if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, l1, l2), True):
        return True
    else:
        return False

def printGrid(grid):
    rowsInStr = []
    for row in grid:
        rowsInStr.append(''.join(row))
    gridStr = '\n'.join(rowsInStr)
    print(f"Blueprint:\n{gridStr}")

#######################################################################################################################
########################################### SOLUTION UTILITIES ########################################################
#######################################################################################################################

def value(blueprint, solution):  # also checks if solution is valid
    t = len(blueprint.getSolutionCoveredCells(solution))
    N = len(blueprint.accessMstPathsDict(solution))
    M = routersPlaced(solution)
    remainingBudget = blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)
    if remainingBudget < 0:
        return None
    return 1000 * t + remainingBudget

def routersPlaced(solution) -> int:
    counter = 0
    for router in solution:
        if router != (-1, -1):
            counter += 1
    return counter

def checkSolutionDuplicates(solution):
    aux = []
    for i in solution:
        aux.append(tuple(i))
    return len(aux) != len(set(aux))


def validSolution(blueprint, solution):  # doesn't check budget
    if checkSolutionDuplicates(solution): return False
    for router in solution:
        if not blueprint.validPosition(router): return False
    return True


def generateMaxRoutersSolution(blueprint):
    solution = []
    auxList = [0] * blueprint.getMaxRouters()
    for i in auxList:
        x = random.randint(0, blueprint.height - 1)
        y = random.randint(0, blueprint.width - 1)
        if not blueprint.validPosition(x, y) or not blueprint.notVoid(x,y):
            auxList.append(i)
            continue
        solution.append((x, y))
    return solution

def getIndiceOfLastNonEmptyRouter(solution) -> int:
    for i in range(0, len(solution)):
        if solution[-(i + 1)] != (-1, -1):
            return len(solution) - i - 1


def randomNeighbour(blueprint, solution: list):  # can return an infeasable solution
    routersNum = routersPlaced(solution)

    routerChange = random.randint(0, routersNum - 1)
    coordChange = random.randint(0, 1)
    upOrDown = random.randint(0, 1)

    neighbour = solution.copy()

    add = 0
    if upOrDown == 1:
        add = 1
    elif upOrDown == 0:
        add = -1

    if upOrDown == -1:
        neighbour[routerChange] = (-1, -1)
    else:
        if coordChange == 0:
            neighbour[routerChange] = (neighbour[routerChange][0] + add, neighbour[routerChange][1])
        elif coordChange == 1:
            neighbour[routerChange] = (neighbour[routerChange][0], neighbour[routerChange][1] + add)


    if not validSolution(blueprint, neighbour): return None, None
    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None: return None, None
    return neighbour, neighbourValue


def neighbour(blueprint, solution, routerToChange, coordToChange, upOrDown, numRouters):
    """
    :param blueprint:
    :param solution: inital solution
    :param routerToChange: index, between 0 and number of router in the solution
    :param coordToChange: 0 or 1, 0 changes x, 1 changes y
    :param upOrDown: 1 increments, 0 decrements, -1 makes the router at routerToChange [-1,
    :param numRouters: if it's lower than the number of routers in the solution, removes the worst router
    :return:
    """

    neighbour = solution.copy()

    if numRouters - 1 < routerToChange:
        raise RuntimeError("numRouters < routerToChange")

    add = 0
    if upOrDown == 1:
        add = 1
    elif upOrDown == 0:
        add = -1

    if upOrDown == -1:
        neighbour[routerToChange] = (-1, -1)
    else:
        if coordToChange == 0:
            neighbour[routerToChange] = (neighbour[routerToChange][0] + add, neighbour[routerToChange][1])
        elif coordToChange == 1:
            neighbour[routerToChange] = (neighbour[routerToChange][0], neighbour[routerToChange][1] + add)


    if not validSolution(blueprint, neighbour): return None, None

    routersToRemove = routersPlaced(solution) - numRouters
    if routersToRemove < 0:
        auxSol = neighbour.copy()
        for i in range(len(auxSol)):
            auxSol[i] = (len(blueprint.accessCoverageDict(auxSol[i])), tuple(auxSol[i]), i)

        heapq.heapify(auxSol)
        for i in range(routersToRemove):
            removedRouter = heapq.heappop(auxSol)
            indexToChange = getIndiceOfLastNonEmptyRouter(neighbour)
            neighbour[removedRouter[2]] = neighbour[indexToChange]
            neighbour[indexToChange] = (-1, -1)

    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None: return None, None

    return neighbour, neighbourValue


