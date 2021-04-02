import utils
from hillClimbing import *
import aStar

class Node:
    def __init__(self, coord, kruskalParent = None, kruskalRank = 0):
        self.coord = coord
        self.kruskalParent = kruskalParent
        self.kruskalRank = kruskalRank

    def __eq__(self, o) -> bool:
        if o is None: return False
        return self.coord == o.coord

    def retrieveRoot(self):
        if self.kruskalParent is None:
            return self
        current = self.kruskalParent
        previous = self
        while current != None:
            previous = current
            current = current.kruskalParent
        return previous

class Edge:
    def __init__(self, nodeFrom : Node, nodeTo : Node, cost):
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.cost = 0

    # def calcCostPrediction(self):
    #     if self.cost != 0:
    #         return self.cost
    #     for edge in self.edges:
    #         self.cost += edge.cost
    #     return self.cost

    def kruskal(self):
        sortedEdges = sorted(self.edges)
        selectedEdges = []
        i = 0
        while len(selectedEdges) < len(self.nodes) - 1:
            bestEdge = sortedEdges[i]
            i = i + 1
            fromRoot = bestEdge.nodeFrom.retrieveRoot()
            toRoot = bestEdge.nodeTo.retrieveRoot()
            if fromRoot != toRoot:
                selectedEdges.append(bestEdge)
                chooseRoot(bestEdge.nodeFrom, bestEdge.nodeTo)

        return Graph(self.nodes, selectedEdges)

    def getPaths(self, blueprint):
        backboneCells = []
        for edge in self.edges:
            path = aStar.aStar(blueprint, edge.nodeFrom.coord, edge.nodeTo.coord)
            backboneCells.extend(path)
        return backboneCells

def chooseRoot(node1 : Node, node2 : Node):
    node1 = node1.retrieveRoot()
    node2 = node2.retrieveRoot()
    if node1.kruskalRank < node2.kruskalRank:
        node1.kruskalParent = node2
    elif node1.kruskalRank > node2.kruskalRank:
        node2.kruskalParent = node1
    else:
        node2.kruskalParent = node1
        node1.kruskalRank += 1

def buildGraphWithSolution(solution, backboneCoord):
    nodes = {}
    edges = []
    aux = solution.copy()
    aux.append(backboneCoord)
    for coord in aux:
        if coord == (-1, -1):
            continue
        nodes[coord] = Node(coord)
    for i in range(len(aux)):
        for j in range(len(aux)):
            if i >= j or (aux[i] == (-1, -1) or aux[j] == (-1, -1)):
                continue

            edges.append(Edge(nodes[aux[i]], nodes[aux[j]], utils.distance(aux[i], aux[j])))

    return Graph(list(nodes.values()), edges)

