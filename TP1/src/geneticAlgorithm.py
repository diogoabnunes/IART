import random
import time
import blueprint as bp
from utils import *


def crossover(sol1, sol2):
    solution1, solution2 = [], []

    routers1, routers2 = routersPlaced(sol1), routersPlaced(sol2)
    minSize = min(routers1, routers2)
    rand = random.randint(1, minSize)

    for i in range(len(sol1)):  # or len(sol2), supposed to be the same
        if i < rand:
            solution1.append(sol1[i])
            solution2.append(sol2[i])
        else:
            solution1.append(sol2[i])
            solution2.append(sol1[i])

    return solution1, solution2


def mutation(sol1, sol2):
    solution1, solution2 = [], []

    routers1, routers2 = routersPlaced(sol1), routersPlaced(sol2)
    minSize = min(routers1, routers2)
    rand = random.randint(1, minSize)

    print(f"Rand: {rand}")

    for i in range(len(sol1)):  # or len(sol2), supposed to be the same
        if i != rand:
            solution1.append(sol1[i])
            solution2.append(sol2[i])
        else:
            solution1.append(sol2[i])
            solution2.append(sol1[i])

    return solution1, solution2


# def reproduce(x, y) -> list:
#     N = len(x)
#     n = routersPlaced(x)
#     c = random.randint(1, n-1)
#
#     return x[0:c+1] + y[c+1:N]

def generateInitialPopulation(blueprint):
    population = []

    validPopulationPositions = blueprint.validPositions
    validPopulationPositions.append([-1, -1])

    maxSizeSolution = blueprint.getMaxRouters()

    for ind in range(30):
        individual = []
        for j in range(maxSizeSolution):
            rand = random.randint(0, len(validPopulationPositions) - 1)
            individual.append(validPopulationPositions[rand])
        population.append(individual)

    return population


def geneticAlgorithm(blueprint):
    population = generateInitialPopulation(blueprint)

    print(population)

    startAlgorithm = time.process_time()
    # while time.process_time() - startAlgorithm > 10: # 10 seconds processing
    for index in range(10):
        rand1, rand2 = random.randint(0, len(population) - 1), random.randint(0, len(population) - 1)
        co1, co2 = crossover(population[rand1], population[rand2])

        mutate = random.randint(0, 100)
        if mutate <= 50:  # to change
            co1, co2 = mutation(co1, co2)
            print("Mutation!")

        r1, r2 = blueprint.getSolutionCoveredCells(co1), blueprint.getSolutionBackboneCells(co2)

        print(r1)
        print(r2)

        if len(r1) > len(r2):
            population.append(r1)
        elif len(r1) < len(r2):
            population.append(r2)
        else:
            population.append(r1)
            population.append(r2)

    """
    1. randomize 2 parents
    2. crossover between them
    3. if mutation, go for it
    4. #1: add best child to population (crossover): realistic?
       #2: add both childs to population (crossover): viable? Could not converge to a better solution
       #3: add child to population (reproduce): viable? Could not converge to a better solution
    5. when time elapsed:
    6. search the best individual in population and return
    """

    return population  # to change


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")

    startTime = time.process_time()

    solution = geneticAlgorithm(blueprint)
    print("Solution: ")
    for sol in solution:
        print(sol)

    endTime = time.process_time()
    print(f"Time: {endTime - startTime} seconds")
    blueprint.reset()
