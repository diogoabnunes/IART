import random
import time
import blueprint as bp
from utils import *


def crossover(sol1, sol2):
    r1, r2 = routersPlaced(sol1), routersPlaced(sol2)
    minRouters = min(r1, r2)
    rand = random.randint(1, max(1, minRouters - 1))

    child = []

    for i in range(len(sol1)):
        if i < rand:
            child.append(sol1[i])
        else:
            child.append(sol2[i])

    return child


def mutation(blueprint, sol):  # should be a change in one solution, not a combination of 2
    r = routersPlaced(sol)
    rand = random.randint(0, r - 1)

    routerToMutate = list(sol[rand])
    print("Mutation",routerToMutate)
    # to do

    return sol


def generateInitialPopulation(blueprint):
    """
    1. Generate initial population: 30 (of solutions: lists of routers)
    2. Order population by value of each solution
    """
    population = []

    maxLength = blueprint.getMaxRouters()
    validPositions = blueprint.validPositions
    validPositions.append((-1, -1))

    iteration = 0

    while True:
        print("Generating initial population: " + str(iteration) + "/30")
        individualSol = []
        for j in range(maxLength):
            rand = random.randint(0, len(validPositions) - 1)
            while validPositions[rand] in individualSol:
                rand = random.randint(0, len(validPositions) - 1)
            individualSol.append(validPositions[rand])

            individualSol = orderRouters(individualSol)

        if value(blueprint, individualSol) is not None and validSolution(blueprint, individualSol):
            iteration += 1
            population.append(individualSol)

        if iteration == 30:
            break

    population.sort(reverse=True, key=lambda elem: value(blueprint, elem))

    return population


def geneticAlgorithm(blueprint):
    population = generateInitialPopulation(blueprint)
    iteration = 0
    lastIteration = 20

    while iteration < lastIteration:
        print("Doing... " + str(iteration) + "/" + str(lastIteration))
        nextGeneration = []

        for i in range(int(len(population))):
            x = population[random.randint(0, int(len(population) / 2))]
            y = population[random.randint(0, int(len(population) / 2))]
            child = crossover(x, y)

            if random.randint(0, 100) < 50:  # to change
                child = mutation(blueprint, child)

            child = orderRouters(child)
            if value(blueprint, child) is not None and validSolution(blueprint, child):
                nextGeneration.append(child)

        population = nextGeneration
        population.sort(reverse=True, key=lambda elem: value(blueprint, elem))
        iteration += 1

    return max(population, key=lambda elem: value(blueprint, elem))


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/charleston_road.in")

    seed = random.randrange(999999999)
    rng = random.Random(seed)
    print("Seed was:", seed)
    random.seed(seed)
    # random.seed(576984236)
    # 52005: 5295197
    # 51005: 845043316
    # 53005: 490183077

    startTime = time.process_time()

    blueprint.printGrid()

    solution = geneticAlgorithm(blueprint)
    print("Genetic Algorithm")
    print(str(value(blueprint, solution)) + " points")
    print("Router solution: " + str(solution))

    blueprint.printSolution(solution)

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()
