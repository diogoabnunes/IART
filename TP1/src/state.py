import random
import time
import blueprint as bp


def checkSolutionDuplicates(solution):
    aux = []
    for i in solution:
        aux.append(tuple(i))
    return len(aux) != len(set(aux))


def generateSolution(blueprint):
    solution = []
    auxList = [0] * blueprint.getMaxRouters()
    for i in auxList:
        x = random.randint(0, blueprint.size[0] - 1)
        y = random.randint(0, blueprint.size[1] - 1)
        if not blueprint.validPosition(x, y):
            auxList.append(i)
            continue
        solution.append([x, y])
    return solution


def routersPlaced(solution) -> int:
    counter = 0
    for router in solution:
        if router != [-1, -1]:
            counter += 1
    return counter


def value(blueprint, solution):  # also checks if solution is valid
    t = len(blueprint.getSolutionCoveredCells(solution))
    N = len(blueprint.getSolutionBackboneCells(solution))
    M = routersPlaced(solution)
    remainingBudget = blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)
    if (remainingBudget < 0): return None

    return 1000 * t + remainingBudget


def randomNeighbour(blueprint, solution: list):  # can return an infeasable solution
    routersNum = routersPlaced(solution)

    routerChange = random.randint(0, routersNum - 1)
    coordChange = random.randint(0, 1)
    upOrDown = random.randint(0, 1)

    neighbour = solution.copy()

    if upOrDown == 1 and neighbour[routerChange][coordChange] != blueprint.size[coordChange] - 1:
        neighbour[routerChange][coordChange] += 1
    elif upOrDown == 0 and neighbour[routerChange][coordChange] != 0:
        neighbour[routerChange][coordChange] -= 1
    print("s")
    print(neighbour[routerChange])
    print(blueprint.atGrid(neighbour[routerChange]))
    print("e")
    if blueprint.atGrid(neighbour[routerChange]) == "#":
        return None, None
    if checkSolutionDuplicates(solution):
        return None, None
    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None:
        return None, None
    return neighbour, neighbourValue


def hillClimbing(blueprint, solution):
    iteration = 0
    solutionValue = value(blueprint, solution)

    validSolution = True

    while True:
        neighbour, neighbourValue = randomNeighbour(blueprint, solution)
        if neighbour is None and neighbourValue is None:
            continue
        break

    while routersPlaced(neighbour) > blueprint.getMaxRouters() / 10:
        while iteration < 100:
            if neighbourValue > solutionValue:
                solutionValue = neighbourValue
                solution = neighbour
                iteration = 0

            neighbourCandidate, neighbourCandidateValue = randomNeighbour(blueprint, solution)
            iteration += 1
            if neighbourCandidate is None and neighbourCandidateValue is None:
                continue
            neighbour, neighbourValue = neighbourCandidate, neighbourCandidateValue

        neighbour[-blueprint.getMaxRouters() + routersPlaced(neighbour) - 1] = [-1, -1]

    return solution


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")

    startTime = time.process_time()
    # blueprint.getCellCoverage((2,15))

    solution = generateSolution(blueprint)
    print("Before Hill Climbing:", solution, ":", value(blueprint, solution))
    solution = hillClimbing(blueprint, solution)
    print("After Hill Climbing:", solution, ":", value(blueprint, solution))

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()
