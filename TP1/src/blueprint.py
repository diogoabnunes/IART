"""
Blueprint class
"""

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

                grid = []
                for i in range(H):
                    row = []
                    for j in range(W):
                        row.append(file[i+3][j])
                    grid.append(row)
                self.grid = grid
    
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
            if self.grid[position[0]][position[1]] != "#":
                try:
                    result.append(position)
                except:
                    pass
        
        return result

        
        
                    
            
