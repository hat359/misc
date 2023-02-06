from templates import template1
from constants import *
from math import sqrt,atan2,cos,sin,pi
from recognizerUtils import *

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
        incrementDistance = getTotalPathLength(points)/(N-1)
        accumulatedDistance = 0.0
        newpoints = [points[0]]
        i = 1
        while i < len(points):
            currentDistance = getDistance(points[i-1],points[i])
            if (accumulatedDistance + currentDistance) >= incrementDistance:
                newPoint = getInterpolatedPoints(points[i-1],points[i], accumulatedDistance, currentDistance,incrementDistance)
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
        centroid = getCentroid(points)
        if angle is None:
            angle = getIndicativeAngle(centroid, points[0])
        newpoints = []
        for i in range(len(points)):
            qx = (points[i][0] - centroid[0]) * cos(angle) - (points[i][1] - centroid[1]) * sin(angle) + centroid[0]
            qy = (points[i][0] - centroid[0]) * sin(angle) + (points[i][1] - centroid[1]) * cos(angle) + centroid[0]
            newpoints.append([qx,qy])
        return newpoints
    
    def scale(self, points, size):
        xStart, YStart, width, height = getBoundingBox(points)
        newpoints = []
        for point in points:
            qx = point[0] * (size / width)
            qy = point[1] * (size / height)
            newpoints.append([qx, qy])
        return newpoints
    
    def translate(self, points, origin):
        centroid = getCentroid(points)
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
            distance = self.DistanceAtBestAngle(points, templatePoints, -Deg2Rad(45), Deg2Rad(45), Deg2Rad(2))
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
        return PathDistance(newpoints, templatePoints)