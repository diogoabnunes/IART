from math import *

def distance(pointA, pointB):
    return sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)

def setGridContent(grid, content, x, y = None):
    try:
        if type(x) == tuple:
            grid[x[1]][x[0]] = content
            return
        grid[y][x] = content
        return
    except IndexError:
        return None