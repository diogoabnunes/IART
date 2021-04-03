import random
import time
import blueprint as bp
from utils import *


def crossover(sol1, sol2):
    """
    Makes a Single-Point Crossover with 2 possible solutions to routers positions.
    :return: A child of the 2 solutions given (using crossover).
    """
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


def mutation(blueprint, sol):
    """
    Makes a Mutation in a solution of routers positions.
    :return: Solution with a mutation.
    """
    r = routersPlaced(sol)
    rand = random.randint(0, r - 1)

    routerToMutate = list(sol[rand])
    # to do

    return sol


def generateInitialPopulation(blueprint):
    """
    Generates the first generation of solutions randomly.
    :return: list with population of first generation.
    """
    population = []

    maxLength = blueprint.getMaxRouters()
    validPositions = blueprint.validPositions
    # validPositions.append((-1, -1))

    iteration = 0
    lastIteration = 8
    solLength = 0


    while iteration < lastIteration:
        print("Generating initial population: " + str(iteration) + "/" + str(lastIteration))
        individualSol = []
        while solLength < maxLength:
            rand = random.randint(0, len(validPositions) - 1)
            while validPositions[rand] in individualSol:
                rand = random.randint(0, len(validPositions) - 1)

            individualSol.append(validPositions[rand])

            if len(blueprint.accessCoverageDict(individualSol[-1])) == 0:
                individualSol.pop()
                continue

            if value(blueprint, individualSol) is None:
                individualSol.pop()
                while len(individualSol) < maxLength:
                    individualSol.append((-1, -1))
                break

            if blueprint.targetCoveredCells == len(blueprint.getSolutionCoveredCells(individualSol)):
                while len(individualSol) < maxLength:
                    individualSol.append((-1, -1))
                break

            solLength += 1

        individualSol = orderRouters(individualSol)

        if value(blueprint, individualSol) is not None:
                iteration += 1
                population.append(individualSol)

    population.sort(reverse=True, key=lambda elem: value(blueprint, elem))

    for sol in population:
        print(getIndiceOfLastNonEmptyRouter(sol))

    print("Generating initial population: Done!")
    return population


def geneticAlgorithm(blueprint):
    """
    Genetic Algorithm: For 20 "generations", all population reproduces randomly, between the best half of solutions.
    :return: The best solution of the last generation.
    """
    population = generateInitialPopulation(blueprint)
    iteration = 0
    lastIteration = 20

    while iteration < lastIteration:
        print("Generation... " + str(iteration) + "/" + str(lastIteration))
        for sol in population:
            print(getIndiceOfLastNonEmptyRouter(sol))
        nextGeneration = []

        for i in range(int(len(population))):
            x = population[random.randint(0, int(len(population) / 2))]
            y = population[random.randint(0, int(len(population) / 2))]
            child = crossover(x, y)

            if random.randint(0, 100) < 50:  # to change
                child = mutation(blueprint, child)

            child = orderRouters(child)
            if value(blueprint, child) is not None:
                nextGeneration.append(child)

        population = nextGeneration
        population.sort(reverse=True, key=lambda elem: value(blueprint, elem))
        iteration += 1

    print("Generation... Done!")
    return population[0]


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/charleston_road.in")

    # seed = random.randrange(999999999)
    # rng = random.Random(seed)
    # print("Seed was:", seed)
    random.seed(1)

    startTime = time.process_time()
    solution = geneticAlgorithm(blueprint)
    endTime = time.process_time()

    print("Genetic Algorithm")
    print(str(value(blueprint, solution)) + " points")
    blueprint.printSolutionCoverage(solution)
    blueprint.printSolutionPaths(solution)

    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()