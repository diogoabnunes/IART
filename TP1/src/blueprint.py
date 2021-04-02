"""
Blueprint class
H: Rows
W: Columns
R: Radius
Pb: Backbone Cost ("Price Backbone")
Pr: Router Cost ("Price Router")
B: Budget
br: Row of initial cell that is already connected to the backbone
bc: Column of initial cell that is already connected to the backbone
"""
import time
from utils import *
import kruskal

class Blueprint:
    def __init__(self, filename):
        with open(filename) as file:
            file = file.read().split("\n")  # Separated in lines

            [H, W, R] = [int(x) for x in file[0].split()]
            [Pb, Pr, B] = [int(x) for x in file[1].split()]
            [br, bc] = [int(x) for x in file[2].split()]

            self.width = W
            self.height = H
            self.routerRadius = R
            self.backboneCost = Pb
            self.routerCost = Pr
            self.budget = B
            self.backbonePosition = (bc, br)
            self.msts = {}
            self.mstPaths = {}
            self.cellsCoverage = {}
            self.grid = []
            self.gridVisited = []
            self.validPositions = []

            for i in range(H):
                row = []
                for j in range(W):
                    row.append(file[i + 3][j])
                self.grid.append(row)

            for i in range(self.height):
                for j in range(self.width):
                    if self.atGrid((i, j)) != "#":
                        self.validPositions.append((i, j))

    def printGrid(self):
        rowsInStr = []
        for row in self.grid:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        print(f"Blueprint:\n{gridStr}")

    def print(self):
        print(f"Rows: {self.height} - Columns: {self.width}")
        print(f"Router Radius: {self.routerRadius}")
        print(f"Backbone Cost: {self.backboneCost} - Router Cost: {self.routerCost} - Budget: {self.budget}")
        print(f"Backbone coord: {self.backbonePosition}")
        self.printGrid()

    def getCellNeighbours(self, coord):
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

        if coord[0] == self.height - 1:
            try:
                neighbours.remove((1, -1))
            except:
                pass
            neighbours.remove((1, 0))
            neighbours.remove((1, 1))

        if coord[1] == self.width - 1:
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
            if type(x) == tuple or type(x) == list:
                if 0 <= x[0] <= self.height and 0 <= x[1] <= self.width:
                    return self.grid[x[0]][x[1]]
                else:
                    raise IndexError()
            if 0 <= x <= self.height and 0 <= x <= self.width:
                return self.grid[x][y]
            else:
                raise IndexError()
        except IndexError:
            return False

    def validPosition(self, x, y=None):
        """
        Checks if a position is valid and doesn't have a wall.
        """
        atGrid = self.atGrid(x, y)
        if not atGrid:
            return False
        return atGrid != '#'

    def validPositionGenetic(self, x, y=None):
        """
        Checks if a position is valid and doesn't have a wall.
        """
        atGrid = self.atGrid(x, y)
        if not atGrid:
            return False
        return atGrid != '#'

    def reset(self):
        self.msts = {}
        self.cellsCoverage = {}

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

    def getMaxRouters(self) -> int:
        return int(self.budget / self.routerCost)

    def getCellCoverage(self, coords):
        """
        Returns a list of the cell coord that would be covered by the router's
        network if the router was to be put in a certain cell with &coords
        """
        if not self.validPosition(coords):
            return None
        ret = []

        upperCoverage = max(0, coords[0] - self.routerRadius)
        leftCoverage = max(0, coords[1] - self.routerRadius)
        rightCoverage = min(self.width, coords[1] + self.routerRadius)
        bottomCoverage = min(self.height, coords[0] + self.routerRadius)

        # getWalls
        walls = []
        for i in range(upperCoverage, bottomCoverage + 1):
            for j in range(leftCoverage, rightCoverage + 1):
                if self.atGrid((i, j)) == "#":
                    walls.append((i, j))

        # min e max [w, v]
        for x in range(upperCoverage, bottomCoverage + 1):
            for y in range(leftCoverage, rightCoverage + 1):
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
        """
        Gets the router's network coverage for all cells
        """
        for x in range(blueprint.width):
            for y in range(blueprint.height):
                cellsCovered = blueprint.getCellCoverage((x, y))
                self.cellsCoverage[(x, y)] = cellsCovered

    # def getSolutionPathsDistPrediction(self, solution):
    #     """
    #     :param solution: Solution needs to be valid!!!
    #     :return: list of backbone cells
    #     """
    #     mst = self.accessPathsDict(solution)
    #     return mst.calcCostPrediction()

    def getSolutionCoveredCells(self, solution):
        """
        :param solution: Solution needs to be valid!!!
        :return: list of covered cells
        """
        cells = []
        for router in solution:
            if router != (-1, -1):
                coveredCells = self.accessCoverageDict(router)
                cells.extend(coveredCells)
        cells = list(dict.fromkeys(cells))
        return cells

    def accessCoverageDict(self, router):
        try:
            coverage = self.cellsCoverage[router]
            return coverage
        except KeyError:
            coverage = self.getCellCoverage(router)
            self.cellsCoverage[router] = coverage
            return coverage

    def accessMstDict(self, solution):
        try:
            mst = self.msts[tuple(solution)]
            return mst
        except KeyError:
            graph = kruskal.buildGraphWithSolution(solution, self.backbonePosition)
            mst = graph.kruskal()
            self.msts[tuple(solution)] = mst
            return mst

    def accessMstPathsDict(self, solution):
        try:
            paths = self.mstPaths[tuple(solution)]
            return paths
        except KeyError:
            mst = self.accessMstDict(solution)
            paths = mst.getPaths(self)
            self.mstPaths[tuple(solution)] = paths
            return paths

# Blueprint end


if __name__ == "__main__":
    blueprint = Blueprint("../inputs/example.in")
    startTime = time.process_time()

    blueprint.printGrid()
    print(blueprint.validPositions)

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()

