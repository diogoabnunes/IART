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
from utils import *
import kruskal
import matplotlib
import matplotlib.pyplot as plt

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
            self.backbonePosition = (br, bc)
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
    
    def notVoid(self, x, y=None):
        """
        Checks if a position is valid and isn't a void.
        """
        atGrid = self.atGrid(x, y)
        if not atGrid:
            return False
        return atGrid != '-'

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

    def printSolutionPaths(self, solution, filename = None):
        path = self.accessMstPathsDict(solution)
        print("Distance: " + str(len(path)))

        gridToPrint = []
        for row in self.grid:
            gridToPrint.append(row.copy())

        for coord in path:
            setGridContent(gridToPrint, "\033[37;43m" + self.atGrid(coord) + "\033[m", coord)

        for router in solution:
            setGridContent(gridToPrint, "\033[37;43mr\033[m", router)
        setGridContent(gridToPrint, "\033[37;43mb\033[m", self.backbonePosition)


        rowsInStr = []
        for row in gridToPrint:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        if filename is None:
            print(gridStr)
        else:
            with open(filename, "w") as file:
                file.write(gridStr)

    def printSolutionCoverage(self, solution, filename = None):
        cellsCovered = self.getSolutionCoveredCells(solution)
        print("Cells covered: " + str(len(cellsCovered)))

        gridToPrint = []
        for row in self.grid:
            gridToPrint.append(row.copy())

        for coord in cellsCovered:
            setGridContent(gridToPrint, "\033[37;42m" + self.atGrid(coord) + "\033[m", coord)

        for router in solution:
            setGridContent(gridToPrint, "r", router)

        rowsInStr = []
        for row in gridToPrint:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        if filename is None:
            print(gridStr)
        else:
            with open(filename, "w") as file:
                file.write(gridStr)

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

    def printGrid(self):
        rowsInStr = []
        for row in self.grid:
            rowsInStr.append(''.join(row))
        gridStr = '\n'.join(rowsInStr)
        print(gridStr)

    def plotSolution(self, solution, fpath=None):      # https://github.com/sbrodehl/HashCode/blob/master/Final%20Round/Utilities.py#L90
        # plot graph with coverage
        fig = plt.figure()

        ax = plt.Axes(fig, (0, 0, 1, 1))
        ax.set_axis_off()
        fig.add_axes(ax)

        gridAux = []
        for row in self.grid:
            rowAux = []
            for element in row:
                if element == '-':
                    rowAux.append((54, 0, 67))
                if element == '.':
                    rowAux.append((100, 139, 139))
                if element == '#':
                    rowAux.append((51, 53, 108))
            gridAux.append(rowAux)

        for router in solution:
            coveredCells = self.accessCoverageDict(router)
            for cell in coveredCells:
                setGridContent(gridAux, (13, 152, 186), cell)

        paths = self.accessMstPathsDict(solution)
        for cell in paths:
            if gridAux[cell[0]][cell[1]] == (51, 53, 108):
                setGridContent(gridAux, (202, 184, 28), cell)
            else:
                setGridContent(gridAux, (253,235,79), cell)

        for router in solution:
            setGridContent(gridAux, (147, 218, 115), router)

        setGridContent(gridAux, (0, 230, 0), self.backbonePosition)

        ax.imshow(gridAux)

        plt.savefig(fpath)

        plt.show()


# Blueprint end

if __name__ == "__main__":
    blueprint = Blueprint("../inputs/lets_go_higher.in")
    blueprint.printGrid()



