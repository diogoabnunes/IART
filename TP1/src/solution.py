'''
H: Rows
W: Columns
R: Radius
Pb: Backbone Cost ("Price Backbone")
Pr: Router Cost ("Price Router")
B: Budget
br: Row of initial cell that is already connected to the backbone
bc: Column of initial cell that is already connected to the backbone
'''

import time

def processInput(filename):
    with open(filename) as file:
        file = file.read().split("\n") # Separated in lines
        
        [H, W, R] = [int(x) for x in file[0].split()]
        [Pb, Pr, B] = [int(x) for x in file[1].split()]
        [br, bc] = [int(x) for x in file[2].split()]
        
        grid = []
        for i in range(H):
            row = []
            for j in range(W):
                row.append(file[i+3][j])
            grid.append(row)
        
    printInput(H, W, R, Pb, Pr, B, br, bc, grid)
        
    return {
        "height": H,
        "width": W,
        "radius": R,
        "backboneCost": Pb,
        "routerCost": Pr,
        "budget": B,
        "backbone": [br, bc],
        "grid": grid
    }

def printInput(H, W, R, Pb, Pr, B, br, bc, grid):
    print(f"Rows: {H}")
    print(f"Columns: {W}")
    print(f"Radius: {R}")
    print(f"Backbone Cost: {Pb}")
    print(f"Router Cost: {Pr}")
    print(f"Budget: {B}")
    print(f"Initial cell connected to the backbone: ({br}, {bc})")

if __name__ == "__main__":
    startTime = time.time()
    processInput("../inputs/lets_go_higher.in")
    endTime = time.time()
    print(f"Time: {endTime - startTime} seconds")