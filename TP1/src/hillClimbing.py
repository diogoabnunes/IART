import random
import time
import blueprint as bp
from utils import *
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


def validSolution(blueprint, solution):  # doesn't check budget
    if checkSolutionDuplicates(solution): return False
    for router in solution:
        if not blueprint.validPosition(router): return False
    return True


def generateMaxRoutersSolution(blueprint):
    solution = []
    auxList = [0] * blueprint.getMaxRouters()
    for i in auxList:
        x = random.randint(0, blueprint.size[1] - 1)
        y = random.randint(0, blueprint.size[0] - 1)
        if not blueprint.validPosition(x, y):
            auxList.append(i)
            continue
        solution.append((x, y))
    return solution

def getIndiceOfLastNonEmptyRouter(solution) -> int:
    for i in range(0, len(solution)):
        if solution[-(i + 1)] != [-1, -1]:
            return len(solution) - i - 1





def randomNeighbour(blueprint, solution: list):  # can return an infeasable solution
    routersNum = routersPlaced(solution)

    routerChange = random.randint(0, routersNum - 1)
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
    """

    :param blueprint:
    :param solution: inital solution
    :param routerToChange: index, between 0 and number of router in the solution
    :param coordToChange: 0 or 1, 0 changes x, 1 changes y
    :param upOrDown: 1 increments, 0 decrements, -1 makes the router at routerToChange [-1,
    :param numRouters: if it's lower than the number of routers in the solution, removes the worst router
    :return:
    """

    neighbour = copySolution(solution)

    if numRouters - 1 < routerToChange:
        raise RuntimeError("numRouters < routerToChange")

    if upOrDown == 1 and neighbour[routerToChange][coordToChange] != blueprint.size[coordToChange] - 1:
        neighbour[routerToChange][coordToChange] += 1
    elif upOrDown == 0 and neighbour[routerToChange][coordToChange] != 0:
        neighbour[routerToChange][coordToChange] -= 1
    elif upOrDown == -1:
        indexToChange = getIndiceOfLastNonEmptyRouter(neighbour)
        neighbour[routerToChange] = neighbour[indexToChange]
        neighbour[indexToChange] = [-1, -1]

    if not validSolution(blueprint, neighbour): return None, None

    routersToRemove = routersPlaced(solution) - numRouters
    if routersToRemove < 0:
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
        if upgrade:
            upgrade = False
            break

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
    blueprint = bp.Blueprint("../inputs/example.in")

    startTime = time.process_time()

    while True:
        solution = generateMaxRoutersSolution(blueprint)
        if not validSolution(blueprint, solution):
            continue
        if value(blueprint, solution) is None:
            continue
        break
    # v1 = value(blueprint, solution)
    # v2 = value(blueprint, solution)
    # print(v1)
    # print(v2)

    print("Before Hill Climbing:", solution, ":", value(blueprint, solution))
    s2 = hillClimbing(blueprint, solution)
    print("After Hill Climbing:", s2, ":", value(blueprint, s2))

    s3 = hillClimbingSteepestAscend(blueprint, solution)
    print("After Hill Climbing:", s3, ":", value(blueprint, s3))

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()
