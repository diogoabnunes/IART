import time
import blueprint as bp
from utils import *
import utils


def getTabuStructure(blueprint,solution):
    """
    Initializes the tabu data structure
    :param blueprint:
    :param solution:
    :return: Returns a dictionnary with tuples of the format (routerNumber, xOrY, upOrDown, numberOfRouters) as keys
    """

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
    """
    Implementation of tabu search algorithm
    :param blueprint:
    :param solution:
    :return: Returns the best found solution of router coords
    """

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
        
        number = 0
        
        # searching all the possible neighbours for the current solution
        for i in tabuStructure:
            candidateSolution, candidateValue = utils.neighbour(blueprint, currentSolution, i[0], i[1], i[2], i[3])
            if candidateValue is not None:
                tabuStructure[i]['MoveValue'] = candidateValue
            else: 
                tabuStructure[i]['MoveValue'] = 0

    
        while True:
            # selecting the move with the highest value from all neighbours
            bestMove = max(tabuStructure, key=lambda x: tabuStructure[x]['MoveValue'])
            moveValue = tabuStructure[bestMove]["MoveValue"]
            tabuTime = tabuStructure[bestMove]["tabuTime"]

            # not in the tabu list
            if tabuTime < iter:
                
                # make the move
                currentSolution, currentValue = utils.neighbour(blueprint, currentSolution, bestMove[0], bestMove[1], bestMove[2], bestMove[3])
                if currentValue is None:
                    currentValue = 0
                
                if moveValue > bestValue:
                    bestSolution = currentSolution
                    bestValue = currentValue
                    print("   Best Move: {}, Value: {} => Best Improving => Admissible".format(bestMove, currentValue))
                    terminate = 0
                
                # update tabu time for the move
                else:
                    print("   ## Termination: {} ## Best Move: {}, Value: {} => Least non-improving => " "Admissible".
                          format(terminate, bestMove, currentValue))
                    terminate += 1

                tabuStructure[bestMove]['tabuTime'] = iter + tabuTenure
                iter += 1
                break

            # in tabu
            else:

                    
                if moveValue > bestValue:
                    
                    # make the move
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
                
    print('\n', '#' * 50, "Performed iterations: {}".format(iter), "Best found Solution: {} , Value: {}".
          format(bestSolution, bestValue), sep="\n")
    return bestSolution


if __name__ == "__main__":
    blueprint = bp.Blueprint("../inputs/example.in")


    solution = utils.generateSolution(blueprint)
    #solution = [(110, 78), (117, 53), (127, 54), (151, 84), (99, 148), (48, 126), (108, 108), (77, 152), (116, 147), (55, 25), (129, 92), (149, 64), (173, 113), (168, 122), (45, 42), (32, 97), (189, 93), (84, 76), (91, 96), (114, 114), (151, 68), (136, 106), (137, 74), (86, 93), (112, 70), (180, 42), (57, 114), (66, 70), (112, 80), (206, 107), (56, 147), (81, 126), (172, 130), (156, 113), (101, 105), (42, 55), (152, 147), (112, 83), (179, 80), (73, 49), (29, 65), (136, 56), (156, 135), (114, 43), (120, 115), (90, 67), (127, 145), (190, 104), (78, 146), (69, 102), (118, 110), (146, 93), (105, 137), (94, 117), (174, 97), (122, 147), (23, 71), (212, 109), (183, 84), (173, 45), (196, 88), (103, 63), (67, 118), (160, 90), (143, 142), (103, 44), (61, 37), (200, 41), (133, 107), (166, 44), (136, 131), (57, 29), (114, 140), (148, 67), (183, 149), (23, 47), (190, 114), (37, 62), (213, 73), (200, 45), (89, 81), (192, 130), (65, 72), (65, 50), (146, 48), (31, 97), (112, 57), (142, 83), (154, 92), (50, 68), (118, 42), (159, 75), (149, 87), (140, 145), (162, 40), (50, 82), (81, 94), (83, 38), (205, 78), (130, 38), (87, 92), (197, 91), (25, 81), (181, 110), (148, 84), (106, 25), (192, 42), (168, 48), (24, 118), (160, 108), (68, 133), (25, 66), (45, 138), (189, 35), (189, 85), (61, 72), (24, 103), (92, 26), (136, 46), (145, 64), (111, 50), (93, 120), (46, 48), (172, 139), (186, 97), (74, 64), (131, 47), (164, 142), (141, 67), (147, 37), (171, 38), (152, 109), (213, 44), (94, 74), (106, 105), (85, 106), (30, 95), (182, 33), (57, 77), (68, 68), (50, 111), (89, 96), (119, 42), (33, 117), (64, 111), (183, 134), (170, 30), (175, 38), (187, 116), (110, 126), (34, 131), (179, 48), (54, 115), (160, 73), (160, 47), (143, 152), (126, 98), (92, 133), (134, 44), (81, 56), (194, 74), (185, 98), (183, 144), (137, 120), (102, 85), (188, 117), (55, 71), (52, 112), (88, 87), (69, 50), (88, 109), (94, 149), (99, 61), (186, 69), (107, 57), (94, 138), (156, 129), (91, 88), (125, 147), (58, 101), (162, 92), (64, 88), (24, 128), (92, 57), (138, 28), (24, 100), (53, 138), (194, 54), (174, 34), (199, 136), (208, 133), (131, 73), (47, 140), (167, 127), (112, 75), (178, 109), (58, 119), (181, 63), (82, 54), (186, 142), (47, 54), (142, 109), (206, 104), (85, 50), (75, 147), (85, 24), (156, 54), (164, 78), (167, 29), (97, 104), (117, 128), (119, 111), (33, 107), (103, 151), (24, 113), (158, 43), (62, 85), (29, 79), (137, 80), (181, 82), (174, 52), (101, 58), (73, 143), (26, 84), (46, 128), (26, 118), (114, 77), (142, 60), (163, 96), (78, 110), (23, 50), (96, 41), (189, 82), (44, 85), (128, 70), (81, 120), (96, 100), (32, 126), (158, 39), (164, 103), (52, 140), (98, 43), (213, 65), (114, 80), (201, 43), (157, 65), (178, 97), (48, 55), (197, 132), (50, 125), (105, 27), (102, 76), (23, 81), (212, 51), (126, 88), (215, 89), (83, 85), (57, 35), (118, 119), (102, 138), (31, 89), (105, 44), (29, 105), (68, 48), (163, 47), (171, 131), (161, 139), (23, 92), (92, 37), (180, 53), (82, 49), (203, 113), (179, 151), (103, 38), (23, 102), (166, 85), (30, 117), (64, 39), (199, 111), (106, 45), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1)]


    print("Before Tabu Search:", solution, ":", utils.value(blueprint, solution))

    startTime = time.process_time()
    s2 = tabuSearch(blueprint, solution)
    endTime = time.process_time()

    print("Before Tabu Search:", solution, ":", utils.value(blueprint, solution))
    #print("\nAfter Tabu Search:", s2, ":", utils.value(blueprint, s2))

    blueprint.printSolutionCoverage(s2)
    blueprint.printSolutionPaths(s2)
    totalTime = endTime - startTime
    print("\nTime: {} seconds".format(totalTime))
    blueprint.reset()
