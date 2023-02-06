from templates import template1
from constants import *
from math import sqrt,atan2,cos,sin,pi

class Recognizer:
    def __init__(self):
        self.template = template1.template
        self.preProcessTemplates()
        
    def preProcessTemplates(self):
        template = self.template
        self.template = {}
        for gesture in template.keys():
            points = template[gesture]
            points = self.resample(points, SAMPLING_POINTS)
            points = self.rotate(points)
            points = self.scale(points, SCALE_FACTOR)
            points = self.translate(points, ORIGIN)
            self.template[gesture] = points
        self.printTemplateStats()
    
    def getGestureFromTemplate(self, gesture):
        return self.template[gesture]
    
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
    
    def rotate(self, points, angle=None):
        centroid = self.getCentroid(points)
        if angle is None:
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

    def recognizeGesture(self, points):
        bestDistance = float("inf")
        recognizedGesture = None
        for gesture, templatePoints in self.template.items():
            distance = self.DistanceAtBestAngle(points, templatePoints, -self.Deg2Rad(45), self.Deg2Rad(45), self.Deg2Rad(2))
            if distance < bestDistance:
                bestDistance = distance
                recognizedGesture = gesture
        score = 1 - bestDistance/(0.5*sqrt(SCALE_FACTOR**2 + SCALE_FACTOR**2))
        return recognizedGesture, score

    def DistanceAtBestAngle(self, candidatePoints, templatePoints, a, b, threshold):
        Phi = 0.5 * (-1.0 + sqrt(5.0))
        x1 = Phi * a + (1.0 - Phi) * b
        f1 = self.DistanceAtAngle(candidatePoints, templatePoints, x1)
        x2 = (1.0 - Phi) * a + Phi * b
        f2 = self.DistanceAtAngle(candidatePoints, templatePoints, x2)
        while abs(b - a) > threshold:
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = Phi * a + (1.0 - Phi) * b
                f1 = self.DistanceAtAngle(candidatePoints, templatePoints, x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = (1.0 - Phi) * a + Phi * b
                f2 = self.DistanceAtAngle(candidatePoints, templatePoints, x2)
        return min(f1, f2)
    
    def DistanceAtAngle(self, candidatePoints, templatePoints, angle):
        newpoints = self.rotate(candidatePoints, angle)
        return self.PathDistance(newpoints, templatePoints)


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

    def Deg2Rad(self, angle):
        return angle * pi / 180.0

    def PathDistance(self, pointA, pointB):
        distance = 0.0
        for i in range(len(pointA)):
            distance += self.getDistance(pointA[i], pointB[i])
        return distance / len(pointA)
