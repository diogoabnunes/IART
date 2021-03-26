import blueprint as bp

class State:
    def __init__(self):
        self.grid = bp.grid
        self.placedRouters = []
        self.targets = []
        self.coveredTargets = []
        self.t = 0
    
    '''
    def placeRouter(self, coords, radius):
        self.placedRouters.add(coords)

        upperCoverage = coords[1]-radius
        leftCoverage = coords[0]-radius
        rightCoverage = coords[0]+radius
        bottomCoverage = coords[1]+radius
        return 0
    '''      

    def getNumCables(): # toChange
            return 1

    def getNumRouters(): #toChange
        return len(self.placedRouters)

    def targetCellsCovered(): #toChange
        return 1


        # a, b: (3, 7)
        # x, y: (0, 4)
        # min(a, x) = 0
        # max(a, x) = 3
        # min(b, y) = 4
        # max(b, y) = 7

        # 0 <= w <= 3 AND 4 <= v <= 7
        # no wall cell inside [w, v]