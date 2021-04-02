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


def mutation(blueprint, sol): # should be a change in one solution, not a combination of 2
    r = routersPlaced(sol)
    rand = random.randint(0, r - 1)

    routerToMutate = list(sol[rand])
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


# def geneticAlgorithmBackup(blueprint):
#     """
#         1. Generate initial population: 30 (of solutions: lists of routers): DONE
#         2. Order population by value of each solution: DONE
#         3. while iterations < 20:
#         4.     for i in range(len(population)):
#         5.         Randomize 2 solutions on the first half of solutions (better ones)
#         6.         Crossover between them to get a single child
#         7.         If mutation, do it
#         8.         Append child to newpopulation
#         9.     Make population = newpopulation (new generation)
#         10.    Order population by value of each solution
#         11.END: return the best solution (i think its the first one, right?)
#         """
#
#     population = generateInitialPopulation(blueprint)
#     iteration = 0
#
#     while True:
#         nextGeneration = []
#         i = 0
#
#         while True:
#             x = random.randint(0, int(len(population)) - 1)
#             y = random.randint(0, int(len(population)) - 1)
#             child = crossover(population[x], population[y])
#
#             if random.randint(0, 100) < 50:  # to change to 10, 5, ... ?
#                 child = mutation(population[x], population[y])
#
#             child = orderRouters(child)
#
#             if value(blueprint, child) is not None and validSolution(blueprint, child):
#                 nextGeneration.append(child)
#
#             i += 1
#             if i >= len(population):
#                 break
#
#         nextGeneration.sort(reverse=True, key=lambda elem: value(blueprint, elem))
#         population = nextGeneration
#         iteration += 1
#         if iteration == 100:
#             break
#
#     print("Population:")
#     for sol in population:
#         print(sol, value(blueprint, sol))
#
#     return max(population, key=lambda elem: value(blueprint, elem))

def geneticAlgorithm(blueprint):
    population = generateInitialPopulation(blueprint)
    iteration = 0
    lastIteration = 30

    while iteration < lastIteration:
        nextGeneration = []

        for i in range(int(len(population))):
            x = population[random.randint(0, int(len(population) / 2))]
            y = population[random.randint(0, int(len(population) / 2))]
            child = crossover(x, y)

            # if random.randint(0, 100) < 50:  # to change
            #     child = mutation(blueprint, child)

            child = orderRouters(child)
            if value(blueprint, child) is not None and validSolution(blueprint, child):
                nextGeneration.append(child)

        population = nextGeneration
        population.sort(reverse=True, key=lambda elem: value(blueprint, elem))
        iteration += 1

    return max(population, key=lambda elem: value(blueprint, elem))


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")

    startTime = time.process_time()

    blueprint.printGrid()

    a = geneticAlgorithm(blueprint)
    print("Genetic Algorithm")
    print(str(value(blueprint, a)) + " points")
    print("Router solution: " + str(a))

    for sol in a:
        setGridContent(blueprint.grid, "r", sol)
    blueprint.printGrid()

    print("Best one: " + str(value(blueprint, [(3, 5), (3, 16)])))

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()


