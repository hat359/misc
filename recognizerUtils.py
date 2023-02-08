from math import sqrt,pi,atan2,cos,sin
from constants import *

def getDistance(pointA, pointB):
    x_difference = abs(pointA[0] - pointB[0])
    y_difference = abs(pointA[1] - pointB[1])
    return sqrt(x_difference**2 + y_difference**2)

def radians(angle):
    return angle*pi/180.0

def getTotalPathLength(points):
    total_distance = 0
    for i in range(len(points)-1):
        total_distance += getDistance(points[i], points[i+1])
    return total_distance

def PathDistance(pointSetA, pointSetB):
    distance = 0.0
    for i in range(len(pointSetA)):
        distance += getDistance(pointSetA[i], pointSetB[i])
    return distance / len(pointSetA)

def getRotatedPoints(point, centroid, angle):
    newX = (point[0] - centroid[0]) * cos(angle) - (point[1] - centroid[1]) * sin(angle) + centroid[0]
    newY = (point[0] - centroid[0]) * sin(angle) + (point[1] - centroid[1]) * cos(angle) + centroid[1]
    return [newX, newY]

def getIndicativeAngle(centroid, startPoint):
    return atan2(centroid[1] - startPoint[1], centroid[0] - startPoint[0])

def getCentroid(points):
    xCenter = 0.0
    yCenter = 0.0
    for i in range(len(points)):
        xCenter += points[i][0]
        yCenter += points[i][1]
    return xCenter/len(points), yCenter/len(points)

def getInterpolatedPoints(pointA, pointB, accumulatedDistance, currentDistance, incrementDistance):
    pointX = pointA[0] + ((incrementDistance - accumulatedDistance) / currentDistance) * (pointB[0] - pointA[0])
    pointY = pointA[1] + ((incrementDistance - accumulatedDistance) / currentDistance * (pointB[1] - pointA[1]))
    return [pointX, pointY]

def getBoundingBox(points):
    minX, maxX, minY, maxY = float('inf'), float('-inf'), float('inf'), float('-inf')
    for point in points:
        minX = min(minX, point[0])
        minY = min(minY, point[1])
        maxX = max(maxX, point[0])
        maxY = max(maxY, point[1])
    return (minX, minY, maxX - minX, maxY - minY)

def getConvergentAngle(leftBound, rightBound, direction):
    if direction == 'left':
        return GOLDEN_RATIO*leftBound+(1.0-GOLDEN_RATIO)*rightBound
    else:
        return (1.0-GOLDEN_RATIO)*leftBound+GOLDEN_RATIO*rightBound