import time
import blueprint as bp
from utils import *


def hillClimbing(blueprint, solution):
    maxRouters = getIndiceOfLastNonEmptyRouter(solution) + 1
    solutionValue = value(blueprint, solution)
    print("\nStarting solution value:", solutionValue)
    iteration = 0
    upgrade = False
    while iteration <= 1:
        for numRouters in range(maxRouters, -1, -1):
            for i in range(numRouters):
                for j in range(0, 2):
                    for k in range(0, 2):
                        for l in range(1, max(3, blueprint.routerRadius // 2)):
                            neighbourSolution, neighbourValue = neighbour(blueprint, solution, i, j, k, numRouters, l)
                            if neighbourSolution is None and neighbourValue is None:
                                continue
                            if compareLists(solution, neighbourSolution):
                                continue

                            if neighbourValue >= solutionValue:
                                solutionValue = neighbourValue
                                solution = neighbourSolution.copy()
                                iteration = 0
                                upgrade = True
                                print("Upgrade:", solutionValue)
                                break
                        if upgrade:
                            break
                    if upgrade:
                        break
                if upgrade:
                    break
            if upgrade:
                upgrade = False
                break
        iteration += 1
    print("Final solution value:", solutionValue)
    return solution


def hillClimbingSteepestAscend(blueprint, solution):
    solutionValue = value(blueprint, solution)
    print("\nStarting solution value:", solutionValue)

    upgrade = True
    steepest = (solution, solutionValue)

    while upgrade:
        upgrade = False
        for numRouters in range(blueprint.getMaxRouters(), -1, -1):
            for i in range(numRouters):
                for j in range(0, 2):
                    for k in range(0, 2):
                        for l in range(1, max(1, blueprint.routerRadius // 2)):
                            neighbourSolution, neighbourValue = neighbour(blueprint, solution, i, j, k, numRouters, l)
                            if neighbourSolution is None and neighbourValue is None:
                                continue
                            if compareLists(solution, neighbourSolution):
                                continue

                            if neighbourValue >= steepest[1]:
                                steepest = (neighbourSolution, neighbourValue)
                                upgrade = True
        if solutionValue < steepest[1]:
            print("Upgrade:", steepest[1])
        solution, solutionValue = steepest

    print("Final solution value:", solutionValue)
    return solution


# TO CLEAN THIS
if __name__ == "__main__":
    seed = random.randrange(999999999)
    rng = random.Random(seed)
    print("Seed is:", seed)
    random.seed(seed)
    # random.seed(72710764)
    blueprint = bp.Blueprint("../inputs/charleston_road.in")
    print("Generating initial solution...")
    startTime = time.process_time()
    solution = generateSolution(blueprint)
    regularStartTime = time.process_time()
    print("Generated initial solution.")
    print(f"Time: {regularStartTime - startTime} seconds\n")

    s2 = hillClimbing(blueprint, solution)
    regularEndTime = time.process_time()
    blueprint.plotSolution(s2)
    blueprint.printSolutionPaths(s2)
    blueprint.printSolutionCoverage(s2)
    # print(f"Time: {regularEndTime - regularStartTime} seconds\n")

    steepestStartTime = time.process_time()
    s3 = hillClimbingSteepestAscend(blueprint, solution)
    steepestEndTime = time.process_time()

    blueprint.plotSolution(s3)
    blueprint.printSolutionPaths(s3)
    blueprint.printSolutionCoverage(s3)
    print(f"Time: {steepestEndTime - steepestStartTime} seconds")
    blueprint.reset()
