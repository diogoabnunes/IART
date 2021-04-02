from utils import *
import heapq
import math


class Node:
    def __init__(self, pos, parent, h = 0, cost = 0):
        self.position = pos
        self.parent = parent
        self.cost = cost
        self.heurisitic = h

    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
        processedCost = 1
        return (processedCost*self.cost + self.heurisitic) < (processedCost*other.cost + other.heurisitic)

    def __repr__(self):
        return '({0},{1})'.format(self.position, self.cost + self.heurisitic)


def aStar(blueprint, startCoord, endCoord):
    """ Calculates the shortest paths between 2 points.
        Params: startCoord - tuple
            endCoord - tuple
            blueprint - class Blueprint
    """
    startCoord = tuple(startCoord)
    if (not blueprint.atGrid(startCoord)) or (not blueprint.atGrid(endCoord)):
        return None

    startNode = Node(startCoord, None, distance(startCoord, endCoord))
    endNode = Node(endCoord, None, 0)

    open = [startNode]
    heapq.heapify(open)
    closed = []

    while open:
        currentNode = heapq.heappop(open)
        closed.append(currentNode)

        if currentNode == endNode:
            path = []
            while currentNode != startNode:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            path.append(currentNode.position)
            return path[::-1]

        neighbours = blueprint.getCellNeighbours(currentNode.position)
        for n in neighbours:
            if isDiagonal(n, currentNode.position):
                moveCost = math.sqrt(2)
            else:
                moveCost = 1
            neighbourNode = Node(n, currentNode, distance(n, endCoord), currentNode.cost + moveCost)
            if neighbourNode in closed: continue

            addToOpen = True
            for node in open:
                if neighbourNode == node and neighbourNode.cost + neighbourNode.heurisitic >= node.cost + node.heurisitic:
                    addToOpen = False

            if (addToOpen):
                heapq.heappush(open, neighbourNode)
    return None

def isDiagonal(pos1, pos2):
    ydiff = abs(pos1[0] - pos2[0])
    xdiff = abs(pos1[1] - pos2[1])

    return xdiff != 0 and ydiff != 0
