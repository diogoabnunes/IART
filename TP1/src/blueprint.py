"""
Blueprint class
"""
from math import sqrt
import time
import heapq

class Blueprint:
    def __init__(self, filename):
        with open(filename) as file:
            file = file.read().split("\n") # Separated in lines
            
            [H, W, R] = [int(x) for x in file[0].split()]
            [Pb, Pr, B] = [int(x) for x in file[1].split()]
            [br, bc] = [int(x) for x in file[2].split()]
            
            self.size = (W, H)
            self.routerRadius = R
            self.backboneCost = Pb
            self.routerCost = Pr
            self.budget = B
            self.backbonePosition = (bc, br)
            self.paths = {}

            grid = []
            gridVisited = []
            for i in range(H):
                row = []
                rowVisited = []
                for j in range(W):
                    row.append(file[i+3][j])
                    rowVisited.append(False)
                grid.append(row)
                gridVisited.append(rowVisited)
            self.grid = grid
            self.gridVisited = gridVisited
    
    def printGrid(self):   
        rowsInStr = []
        for row in self.grid:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        print(f"Blueprint:\n{gridStr}")

    def print(self):
        print(f"Rows: {self.size[1]} - Columns: {self.size[0]}")
        print(f"Router Radius: {self.routerRadius}")
        print(f"Backbone Cost: {self.backboneCost} - Router Cost: {self.routerCost} - Budget: {self.budget}")
        print(f"Backbone coord: {self.backbonePosition}")
        self.printGrid()
    
    def getNeighbours(self, coord):
        """ Returned neighbours do not include walls """
        neighbours = [(-1,-1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        
        if coord[0] == 0:
            neighbours.remove((-1,-1))
            neighbours.remove((-1,0))
            neighbours.remove((-1,1))

        if coord[1] == 0:
            try:
                neighbours.remove((-1,-1))
            except: 
                pass

            neighbours.remove((0,-1))
            neighbours.remove((1,-1))

        if coord[0] == self.size[0] - 1:
            try:
                neighbours.remove((1, -1))
            except:
                pass
            neighbours.remove((1, 0))
            neighbours.remove((1, 1))

        if coord[1] == self.size[1] - 1:
            try: 
                neighbours.remove((-1, 1))
            except:
                pass
            neighbours.remove((0, 1))
            try:
                neighbours.remove((1, 1))
            except:
                pass

        result = []
        for n in neighbours:
            position = (coord[0] + n[0], coord[1] + n[1])
            if self.grid[position[1]][position[0]] != "#":
                try:
                    result.append(position)
                except:
                    pass
        
        return result
    
    def atGrid(self, x, y = None):
        """
        Returns the content of a position of the grid.
        Accepts one parameter only when it's a tuple
        """
        try:
            if type(x) == tuple:
                return self.grid[x[1]][x[0]]
            return self.grid[y][x]
        except IndexError:
            return False
        
    def atVisitedGrid(self, x, y = None):
        """
        Return true if the cell has been visited, false otherwise. If there is an error returns None.
        Accepts one parameter only when it's a tuple
        """
        try:
            if type(x) == tuple:
                return self.gridVisited[x[1]][x[0]]
            return self.gridVisited[y][x]
        except IndexError:
            return None
    
    def validPosition(self, x, y = None):
        """
        Checks if a position is valid and doesn't have a wall.
        """
        atGrid = self.atGrid(x, y)
        if (atGrid == False): 
            return False
        return atGrid != '#'
    
    def visit(self, x, y = None):
        """
        Mark a cell as visited
        """
        try:
            if type(x) == tuple:
                self.gridVisited[x[1]][x[0]] = True
                return
            self.gridVisited[y][x] = True
            return
        except IndexError:
            return None
        
    def clearVisited(self):
        """
        Resets visited cells
        """
        gridVisited = []
        for i in range(self.size[1]):
            rowVisited = []
            for j in range(self.size[0]):
                rowVisited.append(False)
            gridVisited.append(rowVisited)
        self.gridVisited = gridVisited
    
    def reset(self):
        self.clearVisited()
        self.paths = {}

    def printPath(self, returnFromAStar):
        path, dist = returnFromAStar
        print("Distance: " + str(dist))
        
        gridToPrint = self.grid.copy()
        for coord in path:
            setGridContent(gridToPrint, "\033[37;42m" + self.atGrid(coord) + "\033[m", coord)
            
        rowsInStr = []
        for row in gridToPrint:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        print(gridStr)

    def score(self):
        N = self.getNumCables()
        M = self.getNumRouters()
        t = self.targetCellsCovered()
        return 1000 * t + (self.B - (N * self.Pb + M * self.Pr))

    def checkBudget(self):
        N = self.getNumCables()
        M = self.getNumRouters()
        return N * self.Pb + M * self.Pr <= self.B

    def aStar(self, startCoord, endCoord):
        """ Calculates the shortest paths between 2 points.
            Params: startCoord - tuple
                endCoord - tuple
                blueprint - class Blueprint
        """
        
        if (not self.validPosition(startCoord)) or (not self.validPosition(endCoord)): return None

        heap = [(distance(startCoord, endCoord), startCoord)]
        heapq.heapify(heap)   
        resultPath, pathDist = [], 0
        while heap:
            currentDist, currentPos = heapq.heappop(heap)
            if self.atVisitedGrid(currentPos) == None: raise RuntimeError("Not expected position!")
            if self.atVisitedGrid(currentPos): continue

            self.visit(currentPos)
            if currentDist == 0:
                resultPath.append(currentPos)
                return resultPath, pathDist
            
            pathDist += 1
            resultPath.append(currentPos)
            
            neighbours = self.getNeighbours(currentPos)
            for n in neighbours:
                heapq.heappush(heap, (distance(n, endCoord), n))
                
        return None

    def calculateAllPaths(self, endCoord):
        self.paths = {}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if not self.validPosition(i, j): continue
                self.paths[(i, j)] = self.aStar((i,j), endCoord)

# Blueprint end

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


if __name__ == "__main__":
    startTime = time.process_time()
    blueprint = Blueprint("./inputs/example.in")
    blueprint.clearVisited()
    
    # blueprint.printPath(blueprint.aStar((3, 2), (17, 2)))
    blueprint.calculateAllPaths((1, 1))
    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()