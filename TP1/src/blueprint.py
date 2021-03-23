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
    

