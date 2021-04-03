import time
import blueprint as bp
from utils import *

def hillClimbing(blueprint, solution):
    solutionValue = value(blueprint, solution)

    iteration = 0
    upgrade = False
    while iteration <= 1:
        for numRouters in range(blueprint.getMaxRouters(), -1, -1):
            for i in range(numRouters):
                for j in range(0, 2):
                    for k in range(0, 2):
                        neighbourSolution, neighbourValue = neighbour(blueprint, solution, i, j, k, numRouters)
                        if neighbourSolution is None and neighbourValue is None:
                            continue
                        if compareLists(solution, neighbourSolution):
                            continue

                        if neighbourValue > solutionValue:
                            solutionValue = neighbourValue
                            solution = neighbourSolution.copy()
                            iteration = 0
                            upgrade = True
                            break
                    if upgrade:
                        break
                if upgrade:
                    break
            if upgrade:
                break
        iteration += 1

    return solution

def hillClimbingSteepestAscend(blueprint, solution):
    solutionValue = value(blueprint, solution)

    upgrade = True
    steepest = (solution, solutionValue)

    while upgrade:
        upgrade = False
        for numRouters in range(blueprint.getMaxRouters(), -1, -1):
            for i in range(numRouters):
                for j in range(0, 2):
                    for k in range(0, 2):
                        neighbourSolution, neighbourValue = neighbour(blueprint, solution, i, j, k, numRouters)
                        if neighbourSolution is None and neighbourValue is None:
                            continue
                        if compareLists(solution, neighbourSolution):
                            continue

                        if neighbourValue > steepest[1]:
                            steepest = (neighbourSolution, neighbourValue)
                            upgrade = True
        solution, solutionValue = steepest


    return solution

if __name__ == "__main__":
    seed = random.randrange(999999999)
    rng = random.Random(seed)
    print("Seed was:", seed)
    random.seed(seed)
    # random.seed(72710764)
    blueprint = bp.Blueprint("../inputs/example.in")


    while True:
        solution = generateMaxRoutersSolution(blueprint)
        if not validSolution(blueprint, solution):
            continue
        if value(blueprint, solution) is None:
            continue
        break

    print("Before Hill Climbing:", solution, ":", value(blueprint, solution))
    regularStartTime = time.process_time()
    s2 = hillClimbing(blueprint, solution)
    regularEndTime = time.process_time()
    print("After Regular Hill Climbing:", s2, ":", value(blueprint, s2))
    blueprint.plotSolution(s2)
    blueprint.printSolutionPaths(s2)
    blueprint.printSolutionCoverage(s2)
    print(f"Time: {regularEndTime - regularStartTime} seconds\n")

    steepestStartTime = time.process_time()
    s3 = hillClimbingSteepestAscend(blueprint, solution)
    steepestEndTime = time.process_time()
    print("After Steepest Hill Climbing:", s3, ":", value(blueprint, s3))
    print(f"Time: {steepestEndTime - steepestStartTime} seconds")
    blueprint.reset()
