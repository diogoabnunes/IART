import random
import time
import blueprint as bp
from utils import *


def crossover(sol1, sol2):
    return 0


def mutation(sol1, sol2):
    return 0


def generateInitialPopulation(blueprint):
    """
    1. Generate initial population: 30 (of solutions: lists of routers)
    2. Order population by value of each solution
    """
    population = []

    maxLength = blueprint.getMaxRouters()
    validPositions = blueprint.validPositions
    validPositions.append([-1, -1])

    for i in range(30):
        individualSol = []
        for j in range(maxLength):
            rand = random.randint(0, len(validPositions) - 1)
            while validPositions[rand] in individualSol:
                rand = random.randint(0, len(validPositions) - 1)
            individualSol.append(validPositions[rand])
        individualSol.sort(reverse=True, key=lambda elem: value(blueprint, elem))
        population.append(individualSol)

    for i in population:
        print(i)

    return population


def geneticAlgorithm(blueprint):
    population = generateInitialPopulation(blueprint)  # 1
    """
    1. Generate initial population: 30 (of solutions: lists of routers)
    2. Order population by value of each solution
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

    geneticAlgorithm(blueprint)

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()
