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
    t = len(blueprint.getSolutionCoveredCells(solution))
    N = len(blueprint.accessMstPathsDict(solution))
    M = routersPlaced(solution)
    remainingBudget = blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)
    if remainingBudget < 0:
        return None
    return 1000 * t + remainingBudget

def remainingBudget(blueprint, solution):  # also checks if solution is valid
    """
   Calculates and returns the value of a solution.
   """
    t = len(blueprint.getSolutionCoveredCells(solution))
    N = len(blueprint.accessMstPathsDict(solution))
    M = routersPlaced(solution)
    return blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)


def routersPlaced(solution) -> int:
    """
   Calculates the number of routers placed in a solution ((-1, -1) could be in a solution,
   symbolizing that the budget could have more routers, but these solution uses less routers).
   """
    counter = 0
    for router in solution:
        if router != (-1, -1):
            counter += 1
    return counter


def checkSolutionDuplicates(solution):
    """
   Checks if a solution has 2 or more routers in a solution (duplicates).
   """
    aux = []
    for i in solution:
        aux.append(tuple(i))
    return len(aux) != len(set(aux))


def validSolution(blueprint, solution):  # doesn't check budget
    """
    Checks if a solution doesn't have duplicates and every router is in a valid position (not in a wall position).
    """
    if checkSolutionDuplicates(solution): return False
    for router in solution:
        if not blueprint.validPosition(router): return False
    return True


def generateMaxRoutersSolution(blueprint):
    """
    Generates a solution using the maximum number of routers for the given budget.
    """
    solution = []
    auxList = [0] * blueprint.getMaxRouters()
    for i in auxList:
        x = random.randint(0, blueprint.height - 1)
        y = random.randint(0, blueprint.width - 1)
        if not blueprint.validPosition(x, y) or not blueprint.notVoid(x, y):
            auxList.append(i)
            continue
        solution.append((x, y))
    return solution


def generateSolution(blueprint):
    """
    TODO
    :param blueprint:
    :return:
    """
    individualSol = []
    while True:
        for j in range(blueprint.getMaxRouters()):
            rand = random.randint(0, len(blueprint.validPositions) - 1)
            while blueprint.validPositions[rand] in individualSol:
                rand = random.randint(0, len(blueprint.validPositions) - 1)

            individualSol.append(blueprint.validPositions[rand])

            while len(blueprint.accessCoverageDict(individualSol[-1])) == 0:
                individualSol.pop()
                rand = random.randint(0, len(blueprint.validPositions) - 1)
                while blueprint.validPositions[rand] in individualSol:
                    rand = random.randint(0, len(blueprint.validPositions) - 1)
                individualSol.append(blueprint.validPositions[rand])

            if blueprint.targetCoveredCells == len(blueprint.getSolutionCoveredCells(individualSol)):
                while len(individualSol) < blueprint.getMaxRouters():
                    individualSol.append((-1, -1))
                break

            if value(blueprint, individualSol) is None:
                individualSol.pop()
                while len(individualSol) < blueprint.getMaxRouters():
                    individualSol.append((-1, -1))
                break

        individualSol = orderRouters(individualSol)
        if value(blueprint, individualSol) is None:
            continue
        return individualSol


def getIndiceOfLastNonEmptyRouter(solution) -> int:
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
    routersNum = routersPlaced(solution)

    if remove:
        routerChange = random.randint(0, getIndiceOfLastNonEmptyRouter(solution))
    else:
        routerChange = random.randint(0, routersNum - 1)
    coordChange = random.randint(0, 1)
    upOrDown = random.randint(0, 1)

    neighbour = solution.copy()

    add = 0
    if upOrDown == 1:
        add = 1
    elif upOrDown == 0:
        add = -1

    if remove:
        neighbour[routerChange] = (-1, -1)
    else:
        if coordChange == 0:
            neighbour[routerChange] = (neighbour[routerChange][0] + add, neighbour[routerChange][1])
        elif coordChange == 1:
            neighbour[routerChange] = (neighbour[routerChange][0], neighbour[routerChange][1] + add)

    if not validSolution(blueprint, neighbour):
        return None, None
    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None: return None, None
    return neighbour, neighbourValue


def neighbour(blueprint, solution, routerToChange, coordToChange, upOrDown, numRouters, quantity = 1):
    """
    :param blueprint: Problem blueprint.
    :param solution: Initial solution.
    :param routerToChange: index, between 0 and number of router in the solution
    :param coordToChange: 0 or 1, 0 changes x, 1 changes y
    :param upOrDown: 1 increments, 0 decrements, -1 makes the router at routerToChange [-1,
    :param numRouters: if it's lower than the number of routers in the solution, removes the worst router
    :return: The pretended neighbour and his value.
    """

    neighbour = solution.copy()

    if numRouters - 1 < routerToChange:
        raise RuntimeError("numRouters < routerToChange")

    add = 0
    if upOrDown == 1:
        add = quantity
    elif upOrDown == 0:
        add = -quantity

    if upOrDown == -1:
        lastIx = getIndiceOfLastNonEmptyRouter(neighbour)
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
        # auxSol = neighbour.copy()
        # for i in range(len(auxSol)):
        #     auxSol[i] = (len(blueprint.accessCoverageDict(auxSol[i])), tuple(auxSol[i]), i)
        #
        # heapq.heapify(auxSol)
        # for i in range(routersToRemove):
        #     removedRouter = heapq.heappop(auxSol)
        #     indexToChange = getIndiceOfLastNonEmptyRouter(neighbour)
        #     neighbour[removedRouter[2]] = neighbour[indexToChange]
        #     neighbour[indexToChange] = (-1, -1)
        lastIx = getIndiceOfLastNonEmptyRouter(neighbour)
        for i in range(routersToRemove):
            print("gere")
            toRemove = random.randint(0, lastIx - 1)
            neighbour[toRemove] = neighbour[lastIx]
            neighbour[lastIx] = (-1, -1)
            lastIx -= 1
            if lastIx == -1:
                break

    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None:
        return None, None

    return neighbour, neighbourValue


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
