from math import *
import functools


def distance(pointA, pointB):
    return sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)


def setGridContent(grid, content, x, y=None):
    try:
        if type(x) == tuple:
            grid[x[1]][x[0]] = content
            return
        grid[y][x] = content
        return
    except IndexError:
        return None


def compareLists(l1, l2):
    if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, l1, l2), True):
        return True
    else:
        return False
