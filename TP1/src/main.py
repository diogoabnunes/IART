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
        print("[1] example.in (8x22)")
        print("[2] labirinto.in (3x7)")
        print("[3] enunciado.in (7x16)")
        print("[4] better_example.in (8x22)")
        print("[5] charleston_road.in (240x180)")
        print("[6] rue_de_londres.in (559x404)")
        print("[7] opera.in (667x540)")
        print("[8] lets_go_higher.in (872x975)")
        print("[0] Quit")
        file = input("File input: ")

        if file == str(1):
            file = "../inputs/example.in"
        elif file == str(2):
            file = "../inputs/labirinto.in"
        elif file == str(3):
            file = "../inputs/enunciado.in"
        elif file == str(4):
            file = "../inputs/better_example.in"
        elif file == str(5):
            file = "../inputs/charleston_road.in"
        elif file == str(6):
            file = "../inputs/rue_de_londres.in"
        elif file == str(7):
            file = "../inputs/opera.in"
        elif file == str(8):
            file = "../inputs/lets_go_higher.in"
        elif file == str(0):
            break
        else:
            print("File not found\n")
            continue
        print("File input: " + file + "\n")

        blueprint = bp.Blueprint(file)

        print("Choose algorithm to run")
        print("[1] Simulated Annealing")
        print("[2] Hill Climbing: Normal")
        print("[3] Hill Climbing: Steepest Ascend")
        print("[4] Genetic Algorithm")
        print("[5] Tabu Search")
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
            solution = hillClimbing.hillClimbingSteepestAscend(blueprint, solution)
        elif val == str(4):
            solution = geneticAlgorithm.geneticAlgorithm(blueprint)
        elif val == str(5):
            solution = tabuSearch.tabuSearch(blueprint, solution)
        elif val == str(0):
            break
        else:
            print("Algorithm not found\n")
            continue
        endTime = time.time()
        print(f"\nTime: {endTime - startTime} seconds\n\n")

        blueprint.printSolutionCoverage(solution)
        blueprint.printSolutionPaths(solution)

        # print("\nContinue?")
        # print("[1] Yes")
        # print("[0] No (Quit)")
        # option = input("Option: ")
        #
        # if option == str(1):
        #     continue
        # elif option == str(0):
        #     print("\nAre you sure you want to leave?")
        #     print("[1] No, I am staying!")
        #     print("[2] Yes...")
        #     option1 = input("Option: ")
        #
        #     if option1 == str(1):
        #         continue
        #     elif option1 == str(2):
        #         break
        # else:
        #     break


if __name__ == "__main__":
    menu()
