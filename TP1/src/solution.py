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
import paths

if __name__ == "__main__":
    startTime = time.time()
    blueprint = blueprint.Blueprint("../inputs/example.in")
    blueprint.print()
    
    print(paths.aStar((2,2), (9,2), blueprint))
    endTime = time.time()
    print(f"Time: {endTime - startTime} seconds")