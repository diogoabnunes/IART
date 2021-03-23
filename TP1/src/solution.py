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
import blueprint

if __name__ == "__main__":
    startTime = time.time()
    blueprint = blueprint.Blueprint("../inputs/example.in")
    blueprint.print()
    print(blueprint.getNeighbours((2,2)))
    endTime = time.time()
    print(f"Time: {endTime - startTime} seconds")