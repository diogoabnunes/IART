from math import *
import functools


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


def routersPlaced(solution) -> int:
    counter = 0
    for router in solution:
        if router != [-1, -1]:
            counter += 1
    return counter


def compareLists(l1, l2):
    if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, l1, l2), True):
        return True
    else:
        return False


def value(blueprint, solution):  # also checks if solution is valid
    t = len(blueprint.getSolutionCoveredCells(solution))
    N = len(blueprint.getSolutionBackboneCells(solution))
    M = routersPlaced(solution)
    remainingBudget = blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)
    if remainingBudget < 0:
        return None

    # print(solution)
    # print('\tt :', t)
    # print('\tN :', N)
    # print('\tM :', M)
    # print('\tremainingBudget :', remainingBudget)
    # print('\ttotal :', 1000 * t + remainingBudget)

    return 1000 * t + remainingBudget


def printGrid(grid):
    rowsInStr = []
    for row in grid:
        rowsInStr.append(''.join(row))
    gridStr = '\n'.join(rowsInStr)
    print(f"Blueprint:\n{gridStr}")