"""
Blueprint class
"""
import time
import random
from aStar import *

from utils import *

class Blueprint:
    def __init__(self, filename):
        with open(filename) as file:
            file = file.read().split("\n")  # Separated in lines

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
            self.cellsCoverage = {}
            self.grid = []
            self.gridVisited = []

            for i in range(H):
                row = []
                for j in range(W):
                    row.append(file[i + 3][j])
                self.grid.append(row)

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
        neighbours = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        if coord[0] == 0:
            neighbours.remove((-1, -1))
            neighbours.remove((-1, 0))
            neighbours.remove((-1, 1))

        if coord[1] == 0:
            try:
                neighbours.remove((-1, -1))
            except:
                pass

            neighbours.remove((0, -1))
            neighbours.remove((1, -1))

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
            result.append(position)
        return result

    def atGrid(self, x, y=None):
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

    def atVisitedGrid(self, x, y=None):
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

    def validPosition(self, x, y=None):
        """
        Checks if a position is valid and doesn't have a wall.
        """
        atGrid = self.atGrid(x, y)
        if not atGrid:
            return False
        return atGrid != '#'

    def visit(self, x, y=None):
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
        path = returnFromAStar
        print("Distance: " + str(len(path)))

        gridToPrint = self.grid.copy()
        for coord in path:
            setGridContent(gridToPrint, "\033[37;42m" + self.atGrid(coord) + "\033[m", coord)

        setGridContent(gridToPrint, "S", path[0])
        setGridContent(gridToPrint, "E", path[-1])

        rowsInStr = []
        for row in gridToPrint:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        print(gridStr)

    def score(self):
        N = self.getNumCables()
        M = self.getNumRouters()
        t = self.targetCellsCovered()
        return 1000 * t + (self.budget - (N * self.backboneCost + M * self.routerCost))

    def checkBudget(self):
        N = self.getNumCables()
        M = self.getNumRouters()
        return N * self.backboneCost + M * self.routerCost <= self.budget


    def calculateAllPaths(self, endCoord):
        self.paths = {}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if not self.validPosition(i, j): continue
                self.paths[(i, j)] = aStar(self, (i, j), endCoord)

    def getMaxRouters(self) -> int:
        return int(self.budget / self.routerCost)

    def generateSolution(self):
        solution = []
        auxList = [0] * self.getMaxRouters()
        for i in auxList:
            x = random.randint(0, self.size[1])
            y = random.randint(0, self.size[0])
            if self.validPosition(x, y):
                auxList.append(i)
                continue
            solution.append((x, y))
        return solution

    def getCellCoverage(self, coords):
        if not self.validPosition(coords):
            return None
        ret = []

        upperCoverage = max(0, coords[1] - self.routerRadius)
        leftCoverage = max(0, coords[0] - self.routerRadius)
        rightCoverage = min(self.size[0], coords[0] + self.routerRadius)
        bottomCoverage = min(self.size[1], coords[1] + self.routerRadius)

        # getWalls
        walls = []
        for i in range(leftCoverage, rightCoverage + 1):
            for j in range(upperCoverage, bottomCoverage + 1):
                if self.atGrid((i, j)) == "#":
                    walls.append((i, j))

        # min e max [w, v]
        for x in range(leftCoverage, rightCoverage + 1):
            for y in range(upperCoverage, bottomCoverage + 1):
                if self.atGrid((x, y)) == ".":
                    (a, b) = (coords[0], coords[1])

                    minX = min(a, x)
                    maxX = max(a, x)
                    minY = min(b, y)
                    maxY = max(b, y)

                    append = True
                    for (wallX, wallY) in walls:
                        if (maxX >= wallX >= minX) and (maxY >= wallY >= minY):
                            append = False

                    if append:
                        ret.append((x, y))
        return ret

    def printRouterCoverage(self, cellCoverage, routerCoord):
        print("Cell coverage size: " + str(len(cellCoverage)))
        gridToPrint = self.grid.copy()

        for coord in cellCoverage:
            setGridContent(gridToPrint, "\033[30;44m" + self.atGrid(coord) + "\033[m", coord)

        setGridContent(gridToPrint, 'R', routerCoord)

        rowsInStr = []
        for row in gridToPrint:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        print(gridStr)

    def getAllCellsCoverage(self):
        for x in range(blueprint.size[1]):
            for y in range(blueprint.size[0]):
                cellsCovered = blueprint.getCellCoverage((x, y))
                self.cellsCoverage[(x, y)] = cellsCovered

# a testar qual o melhor
    def getSolutionBackboneCells1(self, solution):
        cells = []
        for router in solution:
            routerCells = self.paths[router]
            cells.extend(routerCells)
        cells = list(dict.fromkeys(cells))
        return cells

    def getSolutionBackboneCells2(self, solution):
        cells = []
        for router in solution:
            cells = list(set(cells) | set(self.paths[router]))
        return cells



# Blueprint end


if __name__ == "__main__":
    blueprint = Blueprint("../inputs/charleston_road.in")

    startTime = time.process_time()
    # aStar(blueprint, (1, 2), (5, 2))
    blueprint.printPath(aStar(blueprint, (0,0), (90, 120)))
    # blueprint.calculateAllPaths((1, 1))
    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()

    # blueprint = Blueprint("../inputs/labirinto.in")
    #
    # startTime = time.process_time()
    # # aStar(blueprint, (1, 2), (5, 2))
    # blueprint.printPath(aStar(blueprint, (1, 2), (5,2)))
    # #    blueprint.calculateAllPaths((1, 1))
    # endTime = time.process_time()
    # print(f"Time: {endTime - startTime} seconds")
    # blueprint.reset()

    # blueprint = Blueprint("../inputs/better_example.in")
    #
    # startTime = time.process_time()
    # # aStar(blueprint, (1, 2), (5, 2))
    # blueprint.printPath(aStar(blueprint, (0,0), (21, 7)))
    # #    blueprint.calculateAllPaths((1, 1))
    # endTime = time.process_time()
    # print(f"Time: {endTime - startTime} seconds")
    # blueprint.reset()
