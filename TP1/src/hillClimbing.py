import time
import blueprint as bp
from utils import *


def hillClimbing(blueprint, solution):
    maxRouters = getIndiceOfLastNonEmptyRouter(solution) + 1
    solutionValue = value(blueprint, solution)
    print("\nStarting solution value:", solutionValue)
    iteration = 0
    upgrade = True
    while iteration < 30 and upgrade:
        upgrade = False
        # for numRouters in range(maxRouters, maxRouters//2, -1):
        #     for i in range(numRouters):
        for i in range(maxRouters):
            for j in range(0, 2):
                for k in range(0, 2):
                    neighbourSolution, neighbourValue = neighbour(blueprint, solution, i, j, k, maxRouters)
                    if neighbourSolution is None and neighbourValue is None:
                        continue
                    if compareLists(solution, neighbourSolution):
                        continue

                    if neighbourValue > solutionValue:
                        solutionValue = neighbourValue
                        solution = neighbourSolution.copy()
                        iteration += 1
                        upgrade = True
                        print("Upgrade!", str(i) + "/" + str(50) + ", Current score:", solutionValue)
                        break

                if upgrade:
                    break
            if upgrade:
                break
    print("Final solution value:", solutionValue)
    return solution


def hillClimbingSteepestAscend(blueprint, solution):
    print("\nStarting solution value:", value(blueprint, solution))

    solutionCoveredCells = len(blueprint.getSolutionCoveredCells(solution))
    solutionRouters = routersPlaced(solution)


    upgrade = True
    steepest1 = (solution, solutionCoveredCells, solutionRouters)
    steepest2 = (solution, solutionCoveredCells, solutionRouters)
    steepest3 = (solution, solutionCoveredCells, solutionRouters)
    maxRouters = getIndiceOfLastNonEmptyRouter(solution) + 1
    impossibleSolutions = {}
    while upgrade:
        upgrade = False
        # for numRouters in range(maxRouters, (maxRouters * 3)//4, -1):
        #     for i in range(numRouters):
        for i in range(maxRouters):
            for j in range(0, 2):
                for k in range(0, 2):
                    neighbourSolution = neighbour(blueprint, solution, i, j, k, maxRouters, False)
                    if neighbourSolution == (None, None):
                        continue
                    skip = True
                    try:
                        impossibleSolutions[tuple(neighbourSolution)]
                    except KeyError:
                        skip = False
                    if skip:
                        continue
                    if compareLists(solution, neighbourSolution):
                        continue
                    neighbourCoveredCells = len(blueprint.getSolutionCoveredCells(neighbourSolution))
                    neighbourSolutionRouters = routersPlaced(neighbourSolution)
                    if neighbourCoveredCells * 10 + neighbourSolutionRouters > steepest1[1] * 10 + steepest1[2]:
                        steepest3 = steepest2
                        steepest2 = steepest1
                        steepest1 = (neighbourSolution, neighbourCoveredCells, neighbourSolutionRouters)
                        upgrade = True
        if not upgrade:
            break
        steepestValue = value(blueprint, steepest1[0])
        if steepestValue is not None:
            print("Upgrade! Current score:", steepestValue)
            solution, solutionCoveredCells, solutionRouters = steepest1
            steepest2 = steepest1
            steepest3 = steepest1
            continue
        impossibleSolutions[tuple(steepest1[0])] = True
        steepestValue = value(blueprint, steepest2[0])
        if steepestValue is not None:
            print("Upgrade! Current score:", steepestValue)
            solution, solutionCoveredCells, solutionRouters = steepest2
            steepest1 = steepest2
            steepest3 = steepest2
            continue
        impossibleSolutions[tuple(steepest2[0])] = True
        steepestValue = value(blueprint, steepest3[0])
        if steepestValue is not None:
            print("Upgrade! Current score:", steepestValue)
            solution, solutionCoveredCells, solutionRouters = steepest3
            steepest2 = steepest3
            steepest1 = steepest3
            continue
        impossibleSolutions[tuple(steepest3)] = True

    print("Final solution value:", value(blueprint, solution))
    return solution


# TO CLEAN THIS
if __name__ == "__main__":
    # seed = random.randrange(999999999)
    # rng = random.Random(seed)
    # print("Seed is:", seed)
    # random.seed(seed)
    random.seed(672582778)
    blueprint = bp.Blueprint("../inputs/charleston_road.in")

    # print("Generating initial solution...")
    # startTime = time.process_time()
    # solution = generateSolution(blueprint)
    regularStartTime = time.process_time()
    # print("Generated initial solution.")
    # print(f"Time: {regularStartTime - startTime} seconds\n")

    solution = [(138, 137), (215, 66), (137, 24), (191, 62), (160, 151), (61, 63), (106, 86), (120, 57), (115, 118), (50, 85), (162, 91), (141, 114), (63, 54), (59, 34), (110, 149), (119, 115), (140, 102), (79, 79), (97, 123), (189, 73), (180, 76), (159, 80), (93, 96), (132, 99), (50, 123), (142, 39), (95, 115), (155, 40), (178, 149), (33, 84), (139, 128), (113, 41), (186, 146), (38, 57), (48, 86), (190, 95), (182, 78), (194, 110), (46, 66), (150, 106), (162, 108), (189, 50), (81, 65), (110, 71), (164, 40), (136, 135), (70, 74), (35, 114), (66, 145), (146, 71), (183, 52), (207, 97), (116, 65), (167, 94), (185, 61), (125, 30), (71, 140), (129, 127), (175, 139), (191, 59), (122, 39), (68, 67), (90, 110), (114, 37), (182, 49), (67, 42), (198, 135), (103, 77), (174, 104), (57, 81), (197, 136), (141, 153), (33, 117), (191, 138), (161, 38), (157, 63), (90, 39), (158, 48), (70, 47), (186, 132), (182, 86), (118, 82), (72, 90), (128, 37), (210, 121), (91, 150), (132, 139), (65, 53), (102, 42), (80, 125), (200, 113), (167, 65), (138, 29), (78, 36), (147, 57), (86, 60), (121, 93), (72, 83), (164, 104), (122, 111), (42, 89), (52, 38), (67, 146), (202, 52), (51, 116), (132, 124), (109, 70), (102, 113), (111, 130), (61, 151), (189, 66), (127, 24), (52, 124), (184, 39), (43, 124), (173, 134), (128, 111), (111, 49), (189, 99), (63, 74), (89, 61), (55, 91), (32, 123), (147, 153), (73, 101), (51, 86), (155, 73), (130, 67), (71, 85), (122, 95), (136, 105), (142, 118), (67, 62), (160, 103), (135, 87), (170, 30), (77, 102), (202, 83), (136, 47), (107, 48), (49, 43), (77, 147), (162, 126), (168, 99), (55, 49), (135, 24), (66, 36), (97, 122), (139, 125), (168, 114), (56, 80), (61, 87), (88, 104), (136, 108), (146, 25), (112, 134), (102, 27), (83, 108), (140, 135), (102, 30), (67, 60), (70, 105), (155, 76), (74, 124), (129, 106), (36, 96), (152, 41), (57, 105), (65, 91), (49, 44), (149, 29), (28, 97), (158, 118), (128, 125), (94, 58), (107, 59), (55, 90), (157, 26), (66, 87), (185, 126), (115, 49), (139, 126), (75, 75), (103, 141), (117, 90), (114, 99), (160, 115), (184, 31), (89, 101), (179, 70), (205, 117), (99, 112), (58, 149), (205, 121), (114, 64), (210, 131), (62, 42), (50, 144), (119, 52), (84, 145), (121, 99), (72, 49), (136, 33), (52, 33), (150, 116), (146, 46), (24, 114), (55, 26), (69, 29), (118, 43), (200, 60), (206, 131), (177, 101), (151, 150), (186, 105), (131, 124), (75, 136), (196, 59), (127, 143), (160, 104), (32, 66), (64, 35), (135, 77), (65, 25), (38, 79), (154, 88), (195, 102), (191, 100), (90, 152), (66, 81), (66, 140), (55, 88), (165, 117), (137, 120), (171, 108), (121, 65), (164, 143), (144, 72), (112, 74), (160, 67), (139, 104), (98, 99), (140, 54), (74, 100), (24, 103), (164, 152), (126, 106), (75, 89), (77, 90), (99, 69), (87, 96), (106, 116), (47, 136), (159, 28), (106, 84), (68, 39), (102, 99), (49, 62), (214, 75), (148, 48), (152, 78), (137, 117), (142, 137), (51, 133), (77, 38), (55, 101), (45, 85), (93, 132), (192, 38), (37, 105), (48, 58), (131, 50), (72, 123), (56, 90), (90, 57), (69, 89), (62, 86), (151, 148), (166, 128), (76, 92), (29, 50), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1)]


    # s2 = hillClimbing(blueprint, solution)
    # regularEndTime = time.process_time()
    # blueprint.plotSolution(s2)
    # blueprint.printSolutionPaths(s2)
    # blueprint.printSolutionCoverage(s2)
    # print(f"Time: {regularEndTime - regularStartTime} seconds\n")

    steepestStartTime = time.process_time()
    s3 = hillClimbingSteepestAscend(blueprint, solution)
    steepestEndTime = time.process_time()

    blueprint.plotSolution(s3)
    blueprint.printSolutionPaths(s3)
    blueprint.printSolutionCoverage(s3)
    print(f"Time: {steepestEndTime - steepestStartTime} seconds")
    blueprint.reset()
