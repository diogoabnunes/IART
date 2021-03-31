import random
import time
import blueprint as bp
import state as state
import utils

def getTabuStructure(blueprint,solution):
    dict = {}
    index = 0
    for i in solution:
        aux1 = [index, 0, 0, len(solution)]
        aux2 = [index, 0, 1, len(solution)]
        aux3 = [index, 1, 0, len(solution)]
        aux4 = [index, 1, 1, len(solution)]
        aux5 = [index, 0, -1, len(solution)]
        dict[aux1] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux2] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux3] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux4] = {'tabuTime': 0, 'MoveValue': 0}
        dict[aux5] = {'tabuTime': 0, 'MoveValue': 0}
        index = i + 1

    return dict

def TabuSearch(blueprint, solution):
    # Parameters
    tabuTenure = 10
    tabuStructure = getTabuStructure(blueprint,solution)
    bestSolution = solution
    bestValue = state.value(blueprint, bestSolution)
    currentSolution = solution
    currentValue = state.value(blueprint, currentSolution)

    iter = 1
    terminate = 0
    while terminate < 50:
        print('\n\n### iter {}###  Current_Objvalue: {}, Best_Objvalue: {}'.format(iter, currentValue, bestValue))

        for i in tabuStructure:
            candidateSolution = state.neighbour(blueprint, currentSolution, i[0], i[1], i[2], i[3])
            candidateValue = state.value(blueprint,candidateSolution)
            tabuStructure[i]['MoveValue'] = candidateValue

        while True:
            bestMove = max(tabuStructure, key =lambda x: tabuStructure[x]['MoveValue'])
            moveValue = tabuStructure[bestMove]["MoveValue"]
            tabuTime = tabuStructure[bestMove]["tabuTime"]