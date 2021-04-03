import geneticAlgorithm
import hillClimbing
import tabuSearch
import utils
import blueprint as bp
import time


def simulatedAnnealing():
    print("Algorithm: Simulated Annealing (not implemented yet)\n")


def menu():
    print("IART - Router Placement")

    while True:
        print("\nFile input")
        print("[1] example.in")
        print("[2] charleston_road.in")
        print("[3] rue_de_londres.in")
        print("[4] opera.in")
        print("[5] lets_go_higher.in")
        print("[0] Quit")
        file = input("File input: ")

        if file == str(1):
            file = "../inputs/example.in"
        elif file == str(2):
            file = "../inputs/charleston_road.in"
        elif file == str(3):
            file = "../inputs/rue_de_londres.in"
        elif file == str(4):
            file = "../inputs/opera.in"
        elif file == str(5):
            file = "../inputs/lets_go_higher.in"
        elif file == str(0):
            break
        else:
            print("File not found\n")
            continue
        print("File input: " + file + "\n")
        
        blueprint = bp.Blueprint(file)
        
        print("\nChoose algorithm to run")
        print("[1] Simulated Annealing")
        print("[2] Hill Climbing")
        print("[3] Genetic Algorithm")
        print("[4] Tabu Search")
        print("[0] Quit")
        val = input("Option: ")
    


        while True:
            solution = utils.generateMaxRoutersSolution(blueprint)
            if not utils.validSolution(blueprint, solution):
                continue
            if utils.value(blueprint, solution) is None:
                continue
            break


        startTime = time.time()
        if val == str(1):
            simulatedAnnealing()
        elif val == str(2):
            solution = hillClimbing.hillClimbing(blueprint, solution)
        elif val == str(3):
            solution = geneticAlgorithm.geneticAlgorithm(blueprint)
        elif val == str(4):
            solution = tabuSearch.tabuSearch(blueprint, solution)
        elif val == str(0): 
            break
        else:
            print("Algorithm not found\n")
            continue
        endTime = time.time()
        print(f"\nTime: {endTime - startTime} seconds\n\n")

        outFileNames = file.split("/")
        outFileNames = outFileNames[-1]


        blueprint.printSolutionCoverage(solution,)
        blueprint.printSolutionPaths(solution,)
        blueprint.plotSolution(solution, )

        print("\nWhat do you wish to do?")
        print("[1] Start Over")
        print("[2] Quit")
        option = input("Option: ")
        
        if option == str(1):
            continue
        elif option == str(2):
            print("\nAre you sure you want to leave?")
            print("[1] No, I am staying!")
            print("[2] Yes...")
            option1 = input("Option: ")
            
            if option1 == str(1):
                continue
            elif option1 == str(2):
                break
                


if __name__ == "__main__":
    menu()
