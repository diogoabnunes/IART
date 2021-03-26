"""
Path finding algorithms and precomputation of the blueprint
"""
from math import sqrt
import time
import blueprint
import heapq

def distance(pointA, pointB):
    return sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)

def aStar(startCoord, endCoord, blueprint):
    """ Calculates the shortest paths between 2 points.
        Params: startCoord - tuple
            endCoord - tuple
            blueprint - class Blueprint
    """
    
    if (not blueprint.validPosition(startCoord)) or (not blueprint.validPosition(endCoord)): return None
    print(blueprint.gridVisited)
    heap = [(distance(startCoord, endCoord), startCoord)]
    heapq.heapify(heap)   
    resultPath, pathDist = [], 0
    while heap:
        currentDist, currentPos = heapq.heappop(heap)
        if blueprint.atVisitedGrid(currentPos) == None: raise RuntimeError("Not expected position!")
        if blueprint.atVisitedGrid(currentPos): continue
        blueprint.visit(currentPos)
        if currentDist == 0:
            resultPath.append(currentPos)
            return resultPath, pathDist
        
        pathDist += 1
        resultPath.append(currentPos)
        
        neighbours = blueprint.getNeighbours(currentPos)
        for n in neighbours:
            heapq.heappush(heap, (distance(n, endCoord), n))
            
    return None



if __name__ == "__main__":
    startTime = time.time()
    blueprint = blueprint.Blueprint("../inputs/example.in")
    blueprint.print()
    
    print(aStar((3, 3), (4, 3), blueprint))
    endTime = time.time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.clearVisited()
