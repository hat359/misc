from math import sqrt,pi,atan2,cos,sin
from constants import *

# Returns euclidean distance between two points
def getDistance(pointA, pointB):
    x_difference = abs(pointA[0] - pointB[0])
    y_difference = abs(pointA[1] - pointB[1])
    return sqrt(x_difference**2 + y_difference**2)

# Converts andle from degrees to radians
def radians(angle):
    return angle*pi/180.0

# Gets the total path length of gesture my adding all distances between points
def getTotalPathLength(points):
    total_distance = 0
    for i in range(len(points)-1):
        total_distance += getDistance(points[i], points[i+1])
    return total_distance

# Returns path distance between two gestures
def PathDistance(pointSetA, pointSetB):
    distance = 0.0
    for i in range(len(pointSetA)):
        distance += getDistance(pointSetA[i], pointSetB[i])
    return distance / len(pointSetA)

# Returns points which have been rotated about the centroid by some angle
def getRotatedPoints(point, centroid, angle):
    newX = (point[0] - centroid[0]) * cos(angle) - (point[1] - centroid[1]) * sin(angle) + centroid[0]
    newY = (point[0] - centroid[0]) * sin(angle) + (point[1] - centroid[1]) * cos(angle) + centroid[1]
    return [newX, newY]

# Returns angle between the line made by the start point and centroid and x axis
def getIndicativeAngle(centroid, startPoint):
    return atan2(centroid[1] - startPoint[1], centroid[0] - startPoint[0])

# Returns centroid of the gesture
def getCentroid(points):
    xCenter = 0.0
    yCenter = 0.0
    for i in range(len(points)):
        xCenter += points[i][0]
        yCenter += points[i][1]
    return xCenter/len(points), yCenter/len(points)

# Get location of interpolated point between pointA and pointB
def getInterpolatedPoints(pointA, pointB, accumulatedDistance, currentDistance, incrementDistance):
    pointX = pointA[0] + ((incrementDistance - accumulatedDistance) / currentDistance) * (pointB[0] - pointA[0])
    pointY = pointA[1] + ((incrementDistance - accumulatedDistance) / currentDistance * (pointB[1] - pointA[1]))
    return [pointX, pointY]

# Return width and height of tight bounding box of gesture
def getBoundingBox(points):
    minX, maxX, minY, maxY = float('inf'), float('-inf'), float('inf'), float('-inf')
    for point in points:
        minX = min(minX, point[0])
        minY = min(minY, point[1])
        maxX = max(maxX, point[0])
        maxY = max(maxY, point[1])
    return (maxX - minX, maxY - minY)

# Get left or right convergent angle
def getConvergentAngle(leftBound, rightBound, direction):
    if direction == 'left':
        return GOLDEN_RATIO*leftBound+(1.0-GOLDEN_RATIO)*rightBound
    else:
        return (1.0-GOLDEN_RATIO)*leftBound+GOLDEN_RATIO*rightBound