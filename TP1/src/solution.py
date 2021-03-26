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

def simulatedAnnealing():
    print("Algorithm: Simulated Annealing (not implemented yet)\n")

def hillClimbing():
    print("Algorithm: Hill Climbing (not implemented yet)\n")

def geneticAlgorithm():
    print("Algorithm: Genetic Algorithm (not implemented yet)\n")
    
def tabuSearch():
    print("Algorithm: Tabu Search (not implemented yet)\n")

def menu():
    print("IART - Router Placement\n")
    
    while True:
        print("File input")
        print("[1] example.in")
        print("[2] charleston_road.in")
        print("[3] rue_de_londres.in")
        print("[4] opera.in")
        print("[5] lets_go_higher.in")
        print("[0] Quit")
        file = input("File input: ")
        
        if file == str(1): file = "../inputs/example.in"
        elif file == str(2): file = "../inputs/charleston_road.in"
        elif file == str(3): file = "../inputs/rue_de_londres.in"
        elif file == str(4): file = "../inputs/rue_de_londres.in"
        elif file == str(5): file = "../inputs/lets_go_higher.in"
        elif file == str(0): break;
        else:
            print("File not found\n")
            continue;
        print("File input: " + file + "\n")
        
        print("Choose algorithm to run")
        print("[1] Simulated Annealing")
        print("[2] Hill Climbing")
        print("[3] Genetic Algorithm")
        print("[4] Tabu Search")
        print("[0] Quit")
        val = input("Option: ")
        
        startTime = time.time()
        
        if val == str(1):
            simulatedAnnealing()
            bp = blueprint.Blueprint(file)
            bp.print()
            print(paths.aStar((2,2), (9,2), bp))
        elif val == str(2): hillClimbing()
        elif val == str(3): geneticAlgorithm()
        elif val == str(4): tabuSearch()
        elif val == str(0): break
        else:
            print("Algorithm not found\n")
            continue
        
        endTime = time.time()
        print(f"Time: {endTime - startTime} seconds\n\n")

if __name__ == "__main__":
    menu()