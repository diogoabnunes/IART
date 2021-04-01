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


def mutation(sol1, sol2):
    r1, r2 = routersPlaced(sol1), routersPlaced(sol2)
    minRouters = min(r1, r2)
    rand = random.randint(1, max(1, minRouters - 1))

    mutated = []

    for i in range(len(sol1)):
        if i != rand:
            mutated.append(sol1[i])
        else:
            mutated.append(sol2[i])

    return sol1


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
        individualSol = []
        for j in range(maxLength):
            rand = random.randint(0, len(validPositions) - 1)
            while validPositions[rand] in individualSol:
                rand = random.randint(0, len(validPositions) - 1)
            individualSol.append(validPositions[rand])
            individualSol.sort(reverse=True, key=lambda x: x)

        if value(blueprint, individualSol) is not None:
            iteration += 1
            population.append(individualSol)

        if iteration == 20:
            break

    population.sort(reverse=True, key=lambda elem: value(blueprint, elem))

    return population


def geneticAlgorithm(blueprint):
    population = generateInitialPopulation(blueprint)  # 1
    iteration = 0

    while True:
        nextGeneration = []

        for i in range(len(population)):
            x = random.randint(0, int(len(population) / 2))
            y = random.randint(0, int(len(population) / 2))
            child = crossover(population[x], population[y])

            if random.randint(0, 100) < 50:  # to change to 10, 5, ... ?
                child = mutation(population[x], population[y])

            child.sort(reverse=True, key=lambda x: x)
            if value(blueprint, child) is not None:
                nextGeneration.append(child)

        nextGeneration.sort(reverse=True, key=lambda elem: value(blueprint, elem))
        population = nextGeneration
        iteration += 1
        if iteration == 20:
            break

    return max(population, key=lambda elem: value(blueprint, elem))

    """
    1. Generate initial population: 30 (of solutions: lists of routers): DONE
    2. Order population by value of each solution: DONE
    3. while iterations < 20:
    4.     for i in range(len(population)):
    5.         Randomize 2 solutions on the first half of solutions (better ones)
    6.         Crossover between them to get a single child
    7.         If mutation, do it
    8.         Append child to newpopulation
    9.     Make population = newpopulation (new generation)
    10.    Order population by value of each solution
    11.END: return the best solution (i think its the first one, right?)
    """


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")

    startTime = time.process_time()

    blueprint.printGrid()

    a = geneticAlgorithm(blueprint)
    print("Genetic Algorithm")
    print(str(value(blueprint, a)) + " points")
    print("Router solution: " + str(a))

    # for sol in a:
    #     setGridContent(blueprint.grid, "r", sol)
    blueprint.printGrid()

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()


