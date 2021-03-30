import random
import time
import blueprint as bp
import utils
"""
[coord, ...]
coord = [x, y]
[router, router, [-1,-1], [-1,-1]]

solucao valida:
- nao ha duplicados  (validSolution)
- todas os router estap em posicoes validas (validSolution)
- budget nao e excedido (value)
"""
def checkSolutionDuplicates(solution):
    aux = []
    for i in solution:
        aux.append(tuple(i))
    return len(aux) != len(set(aux))

def validSolution(blueprint, solution):   # doesn't check budget
    if checkSolutionDuplicates(solution): return False
    for router in solution:
        if not blueprint.validPosition(router): return False
    return True


def generateMaxRoutersSolution(blueprint):
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
        if router != [-1,-1]:
            counter += 1
    return counter


def value(blueprint, solution):  #also checks if solution doesn't exceed budget
    try:
        cellsCovered = len(blueprint.getSolutionCoveredCells(solution))
        backboneCells = len(blueprint.getSolutionBackboneCells(solution))
    except TypeError:
        return None
    numRouters = routersPlaced(solution)
    remainingBudget = backboneCells * blueprint.backboneCost + numRouters * blueprint.routerCost
    if (remainingBudget < 0): return None

    return 1000 * cellsCovered + remainingBudget

def randomNeighbour(blueprint, solution: list):          # can return an infeasable solution
    routersNum = routersPlaced(solution)

    routerChange = random.randint(0, routersNum-1)
    coordChange = random.randint(0, 1)
    upOrDown = random.randint(0, 1)

    neighbour = solution.copy()

    if upOrDown == 1 and neighbour[routerChange][coordChange] != blueprint.size[coordChange] - 1:
        neighbour[routerChange][coordChange] += 1
    elif upOrDown == 0 and neighbour[routerChange][coordChange] != 0:
        neighbour[routerChange][coordChange] -= 1

    if not validSolution(blueprint, neighbour): return None, None
    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None: return None, None
    return neighbour, neighbourValue

def neighbour(blueprint, solution, routerToChange, coordToChange, upOrDown):
    neighbour = solution.copy()

    if upOrDown == 1 and neighbour[routerToChange][coordToChange] != blueprint.size[coordToChange] - 1:
        neighbour[routerToChange][coordToChange] += 1
    elif upOrDown == 0 and neighbour[routerToChange][coordToChange] != 0:
        neighbour[routerToChange][coordToChange] -= 1

    if not validSolution(blueprint, neighbour): return None, None
    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None: return None, None
    return neighbour, neighbourValue

def hillClimbing(blueprint, solution):
    iteration = 0
    solutionValue = value(blueprint, solution)
    neighbour = [[1,1]] * blueprint.getMaxRouters()
    neighbourValue = -1

    while routersPlaced(neighbour) > blueprint.getMaxRouters()/10:
        for i in range(blueprint.size[0]):
            for j in range(blueprint.size[1]):
                if neighbourValue > solutionValue:
                    solutionValue = neighbourValue
                    solution = neighbour.copy()
                    iteration = 0

                neighbourCandidate, neighbourCandidateValue = randomNeighbour(blueprint, solution)
                iteration += 1
                if neighbourCandidate is None and neighbourCandidateValue is None:
                    continue
                if utils.compareLists(solution, neighbourCandidate):
                    continue
                neighbour, neighbourValue = neighbourCandidate.copy(), neighbourCandidateValue

        neighbour[-blueprint.getMaxRouters() + routersPlaced(neighbour) - 1] = [-1, -1]

    return solution


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")

    startTime = time.process_time()
    # blueprint.getCellCoverage((2,15))

    solution = generateMaxRoutersSolution(blueprint)
    # v1 = value(blueprint, solution)
    # v2 = value(blueprint, solution)
    # print(v1)
    # print(v2)

    print("Before Hill Climbing:", solution, ":", value(blueprint, solution))
    s2 = hillClimbing(blueprint, solution)
    print("After Hill Climbing:", s2, ":", value(blueprint, s2))

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()


