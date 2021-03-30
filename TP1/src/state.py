import random
import time
import blueprint as bp
import utils
import heapq
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
        if not utils.compareLists(router, [-1,-1]):
            counter += 1
    return counter

def getIndiceOfLastNonEmptyRouter(solution) -> int:
    for i in range(0, len(solution)):
        if solution[-(i + 1)] != [-1, -1]:
            return len(solution) - i - 1

def value(blueprint, solution):  #also checks if solution is valid
    t = len(blueprint.getSolutionCoveredCells(solution))
    N = len(blueprint.getSolutionBackboneCells(solution))
    M = routersPlaced(solution)
    remainingBudget = blueprint.budget - (N * blueprint.backboneCost + M * blueprint.routerCost)
    if (remainingBudget < 0): return None

    # print(solution)
    # print('\t', t)
    # print('\t', N)
    # print('\t', M)
    # print('\t', remainingBudget)
    # print('\t', 1000 * t + remainingBudget)

    return 1000 * t + remainingBudget

def randomNeighbour(blueprint, solution: list):          # can return an infeasable solution
    routersNum = routersPlaced(solution)

    routerChange = random.randint(0, routersNum-1)
    coordChange = random.randint(0, 1)
    upOrDown = random.randint(0, 1)

    neighbour = copySolution(solution)

    if upOrDown == 1 and neighbour[routerChange][coordChange] != blueprint.size[coordChange] - 1:
        neighbour[routerChange][coordChange] += 1
    elif upOrDown == 0 and neighbour[routerChange][coordChange] != 0:
        neighbour[routerChange][coordChange] -= 1

    if not validSolution(blueprint, neighbour): return None, None
    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None: return None, None
    return neighbour, neighbourValue

def copySolution(solution):
    copy = []
    for router in solution:
        copy.append(router.copy())
    return copy

def neighbour(blueprint, solution, routerToChange, coordToChange, upOrDown, numRouters):

    neighbour = copySolution(solution)

    if numRouters - 1 < routerToChange:
        raise RuntimeError("numRouters < routerToChange")

    if upOrDown == 1 and neighbour[routerToChange][coordToChange] != blueprint.size[coordToChange] - 1:
        neighbour[routerToChange][coordToChange] += 1
    elif upOrDown == 0 and neighbour[routerToChange][coordToChange] != 0:
        neighbour[routerToChange][coordToChange] -= 1

    if not validSolution(blueprint, neighbour): return None, None

    routersToRemove = routersPlaced(solution) - numRouters
    auxSol = neighbour.copy()
    for i in range(len(auxSol)):
        auxSol[i] = (len(blueprint.accessCoverageDict(auxSol[i])), tuple(auxSol[i]), i)

    heapq.heapify(auxSol)
    for i in range(routersToRemove):
        removedRouter = heapq.heappop(auxSol)
        indexToChange = getIndiceOfLastNonEmptyRouter(neighbour)
        neighbour[removedRouter[2]] = neighbour[indexToChange]
        neighbour[indexToChange] = [-1, -1]


    neighbourValue = value(blueprint, neighbour)
    if neighbourValue is None: return None, None

    return neighbour, neighbourValue

def hillClimbing(blueprint, solution):
    solutionValue = value(blueprint, solution)
    neighbourSolution = [[1,1]] * blueprint.getMaxRouters()

    for numRouters in range(blueprint.getMaxRouters(), -1, -1):
        print("solution with", numRouters, "routers")
        for i in range(numRouters):
            print("i:", i, "/", numRouters)
            for j in range(0,2):
                for k in range(0,2):
                    neighbourSolution, neighbourValue = neighbour(blueprint, solution, i, j, k, numRouters)
                    if neighbourSolution is None and neighbourValue is None:
                        continue
                    if utils.compareLists(solution, neighbourSolution):
                        continue

                    if neighbourValue > solutionValue:
                        solutionValue = neighbourValue
                        solution = neighbourSolution.copy()


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



