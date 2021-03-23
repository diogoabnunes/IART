"""
Path finding algorithms and precomputation of the blueprint
"""
from math import sqrt
import heapq

def distance(pointA, pointB):
    return sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)

def aStar(startCoord, endCoord, blueprint):
    """    Params are tuples """
    heap = []
    heapq.heapify(heap)   

