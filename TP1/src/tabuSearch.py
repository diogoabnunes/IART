import time
import blueprint as bp
import hillClimbing
from utils import *
import utils

def getTabuStructure(blueprint,solution):
    dict = {}
    index = 0
    for i in solution:
        aux1 = (index, 0, 0, len(solution))
        aux2 = (index, 0, 1, len(solution))
        aux3 = (index, 1, 0, len(solution))
        aux4 = (index, 1, 1, len(solution))
        aux5 = (index, 0, -1, len(solution))
        dict[aux1] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux2] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux3] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux4] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux5] = {'tabuTime': 0, 'MoveValue': 0}
        index = index + 1

    return dict

def tabuSearch(blueprint, solution):
    # Parameters
    tabuTenure = 10
    tabuStructure = getTabuStructure(blueprint, solution)
    bestSolution = solution
    bestValue = value(blueprint, bestSolution)
    currentSolution = solution
    currentValue = value(blueprint, currentSolution)

    iter = 1
    terminate = 0
    while terminate < 50:
        print('\n\n### Iteration {} ###  Current Value: {}, Best Value: {}'.format(iter, currentValue, bestValue))

        for i in tabuStructure:
            candidateSolution, candidateValue = utils.neighbour(blueprint, currentSolution, i[0], i[1], i[2], i[3])
            if candidateValue is not None:
                tabuStructure[i]['MoveValue'] = candidateValue

        while True:
            bestMove = max(tabuStructure, key =lambda x: tabuStructure[x]['MoveValue'])
            moveValue = tabuStructure[bestMove]["MoveValue"]
            tabuTime = tabuStructure[bestMove]["tabuTime"]

            if tabuTime < iter:
                currentSolution, currentValue = utils.neighbour(blueprint, currentSolution, bestMove[0], bestMove[1], bestMove[2], bestMove[3])

                if moveValue > bestValue:
                    bestSolution = currentSolution
                    bestValue = currentValue
                    print("   Best Move: {}, Value: {} => Best Improving => Admissible".format(bestMove, currentValue))
                    terminate = 0
                else:
                    print("   ## Termination: {} ## Best Move: {}, Value: {} => Least non-improving => " "Admissible".format(terminate, bestMove, currentValue))
                    terminate += 1

                tabuStructure[bestMove]['tabuTime'] = iter + tabuTenure
                iter += 1
                break

            else:

                if moveValue > bestValue:
                    currentSolution, currentValue = utils.neighbour(blueprint, currentSolution, bestMove[0], bestMove[1], bestMove[2], bestMove[3])
                    bestSolution = currentSolution
                    bestValue = currentValue
                    print("   Best Move: {}, Value: {} => Aspiration => Admissible".format(bestMove, currentValue))
                    terminate = 0
                    iter += 1
                    break
                else:
                    tabuStructure[bestMove]["MoveValue"] = float('-inf')
                    terminate += 1
                    print("   Best Move: {}, Value: {} => Tabu => Inadmissible".format(bestMove, currentValue))
                    break
    print('\n', '#' * 50, "Performed iterations: {}".format(iter), "Best found Solution: {} , Value: {}".format(bestSolution, bestValue), sep="\n")
    return bestSolution

if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")

    while True:
        solution = utils.generateMaxRoutersSolution(blueprint)
        if not utils.validSolution(blueprint, solution):
            continue
        if utils.value(blueprint, solution) is None:
            continue
        break

    startTime = time.process_time()
    solution = tabuSearch(blueprint, solution)
    endTime = time.process_time()

    blueprint.printSolutionCoverage(solution)
    blueprint.printSolutionPaths(solution)
    
    totalTime = endTime - startTime
    print("\nTime: {} seconds".format(totalTime))
    blueprint.reset()
