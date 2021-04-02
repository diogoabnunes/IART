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

def TabuSearch(blueprint, solution):
    # Parameters
    tabuTenure = 10
    tabuStructure = getTabuStructure(blueprint, solution)
    bestSolution = solution
    bestValue = value(blueprint, bestSolution)
    currentSolution = solution
    currentValue = value(blueprint, currentSolution)

    iter = 1
    terminate = 0
    while terminate < 10:
        print('\n\n### iter {}###  Current_Objvalue: {}, Best_Objvalue: {}'.format(iter, currentValue, bestValue))

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
                    print("   best_move: {}, Objvalue: {} => Best Improving => Admissible".format(bestMove, currentValue))
                    terminate = 0
                else:
                    print("   ##Termination: {}## best_move: {}, Objvalue: {} => Least non-improving => " "Admissible".format(terminate, bestMove, currentValue))
                    terminate += 1

                tabuStructure[bestMove]['tabuTime'] = iter + tabuTenure
                iter += 1
                break

            else:

                if moveValue > bestValue:
                    # make the move
                    currentSolution, currentValue = utils.neighbour(blueprint, currentSolution, bestMove[0], bestMove[1], bestMove[2], bestMove[3])
                    bestSolution = currentSolution
                    bestValue = currentValue
                    print("   best_move: {}, Objvalue: {} => Aspiration => Admissible".format(bestMove, currentValue))
                    terminate = 0
                    iter += 1
                    break
                else:
                    tabuStructure[bestMove]["MoveValue"] = float('-inf')
                    terminate += 1
                    print("   best_move: {}, Objvalue: {} => Tabu => Inadmissible".format(bestMove, currentValue))
                    break
    # print('#' * 50, "Performed iterations: {}".format(iter), "Best found Solution: {} , Objvalue: {}".format(bestSolution, bestValue), sep="\n")
    return bestSolution

if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")

    startTime = time.process_time()

    while True:
        solution = utils.generateMaxRoutersSolution(blueprint)
        if not utils.validSolution(blueprint, solution):
            continue
        if utils.value(blueprint, solution) is None:
            continue
        break
    # v1 = value(blueprint, solution)
    # v2 = value(blueprint, solution)
    # print(v1)
    # print(v2)

    print("Before Tabu Search:", solution, ":", utils.value(blueprint, solution))
    s2 = TabuSearch(blueprint, solution)
    print("After Tabu Search:", s2, ":", utils.value(blueprint, s2))

    endTime = time.process_time()
    print("Time: {endTime - startTime} seconds")
    blueprint.reset()
