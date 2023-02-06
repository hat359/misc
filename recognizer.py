from templates import template1
from math import sqrt,atan2,cos,sin

class Recognizer:
    def __init__(self):
        self.template = template1.template
    
    def printTemplateStats(self):
        for template,points in self.template.items():
            print(template,len(points))

    def resample(self, points, N):
        incrementDistance = self.getTotalPathLength(points)/(N-1)
        accumulatedDistance = 0.0
        newpoints = [points[0]]
        i = 1
        while i < len(points):
            currentDistance = self.getDistance(points[i-1],points[i])
            if (accumulatedDistance + currentDistance) >= incrementDistance:
                newPoint = self.getInterpolatedPoints(points[i-1],points[i], accumulatedDistance, currentDistance, incrementDistance)
                newpoints.append(newPoint)
                points.insert(i, newPoint)
                accumulatedDistance = 0.0
            else:
                accumulatedDistance += currentDistance
            i += 1
        if len(newpoints) == N - 1:
            newpoints.append(points[-1])
        return newpoints
    
    def rotate(self, points):
        centroid = self.getCentroid(points)
        angle = self.getIndicativeAngle(centroid, points[0])
        newpoints = []
        for i in range(len(points)):
            qx = (points[i][0] - centroid[0]) * cos(angle) - (points[i][1] - centroid[1]) * sin(angle) + centroid[0]
            qy = (points[i][0] - centroid[0]) * sin(angle) + (points[i][1] - centroid[1]) * cos(angle) + centroid[0]
            newpoints.append([qx,qy])
        return newpoints
    
    def scale(self, points, size):
        xStart, YStart, width, height = self.getBoundingBox(points)
        newpoints = []
        for point in points:
            qx = point[0] * (size / width)
            qy = point[1] * (size / height)
            newpoints.append([qx, qy])
        return newpoints
    
    def translate(self, points, origin):
        centroid = self.getCentroid(points)
        newpoints = []
        for point in points:
            qx = point[0] + origin[0] - centroid[0]
            qy = point[1] + origin[1] - centroid[1]
            newpoints.append([qx, qy])
        return newpoints


    def getBoundingBox(self, points):
        minX, maxX, minY, maxY = float('inf'), float('-inf'), float('inf'), float('-inf')
        for point in points:
            minX = min(minX, point[0])
            minY = min(minY, point[1])
            maxX = max(maxX, point[0])
            maxY = max(maxY, point[1])
        return (minX, minY, maxX - minX, maxY - minY)


    def getInterpolatedPoints(self, pointA, pointB, accumulatedDistance, currentDistance, incrementDistance):
        pointX = pointA[0] + ((incrementDistance - accumulatedDistance) / currentDistance) * (pointB[0] - pointA[0])
        pointY = pointA[1] + ((incrementDistance - accumulatedDistance) / currentDistance * (pointB[1] - pointA[1]))
        return [pointX, pointY]

    def getDistance(self, pointA, pointB):
        x_difference = abs(pointA[0] - pointB[0])
        y_difference = abs(pointA[1] - pointB[1])
        return sqrt(x_difference**2 + y_difference**2)

    def getTotalPathLength(self, points):
        total_distance = 0
        for i in range(len(points)-1):
            total_distance += self.getDistance(points[i], points[i+1])
        return total_distance
    
    def getCentroid(self, points):
        xCenter = 0.0
        yCenter = 0.0
        for i in range(len(points)):
            xCenter += points[i][0]
            yCenter += points[i][1]
        return xCenter/len(points), yCenter/len(points)

    def getIndicativeAngle(self, centroid, startPoint):
        return atan2(centroid[1] - startPoint[1], centroid[0] - startPoint[0])

