from templates import template1
from constants import *
from math import sqrt
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
            newpoints.append(getRotatedPoints(points[i],centroid,angle))
        return newpoints
    
    def scale(self, points, size):
        xStart, YStart, width, height = getBoundingBox(points)
        newpoints = []
        for point in points:
            newpoints.append([point[0]*(size/width), point[1]*(size/height)])
        return newpoints
    
    def translate(self, points, origin):
        centroid = getCentroid(points)
        newpoints = []
        for point in points:
            newpoints.append([point[0]+origin[0]-centroid[0], point[1]+origin[1]-centroid[1]])
        return newpoints

    def recognizeGesture(self, points):
        bestDistance = float("inf")
        recognizedGesture = None
        for gesture, templatePoints in self.template.items():
            distance = self.DistanceAtBestAngle(points, templatePoints, radians(-45), radians(45), radians(2))
            if distance < bestDistance:
                bestDistance = distance
                recognizedGesture = gesture
        score = 1 - bestDistance/(0.5*sqrt(SCALE_FACTOR**2 + SCALE_FACTOR**2))
        return recognizedGesture, score

    def DistanceAtBestAngle(self, candidatePoints, templatePoints, leftBound, rightBound, threshold):
        leftConvergentAngle = getConvergentAngle(leftBound, rightBound, 'left')
        distanceUsingLCA = self.DistanceAtAngle(candidatePoints, templatePoints, leftConvergentAngle)
        rightConvergentAngle = getConvergentAngle(leftBound, rightBound, 'right')
        distanceUsingRCA = self.DistanceAtAngle(candidatePoints, templatePoints, rightConvergentAngle)
        while abs(rightBound - leftBound) > threshold:
            if distanceUsingLCA < distanceUsingRCA:
                rightBound = rightConvergentAngle
                rightConvergentAngle = leftConvergentAngle
                distanceUsingRCA = distanceUsingLCA
                leftConvergentAngle = getConvergentAngle(leftBound, rightBound, 'left')
                distanceUsingLCA = self.DistanceAtAngle(candidatePoints, templatePoints, leftConvergentAngle)
            else:
                leftBound = leftConvergentAngle
                leftConvergentAngle = rightConvergentAngle
                distanceUsingLCA = distanceUsingRCA
                rightConvergentAngle = getConvergentAngle(leftBound, rightBound, 'right')
                distanceUsingRCA = self.DistanceAtAngle(candidatePoints, templatePoints, rightConvergentAngle)
        return min(distanceUsingLCA, distanceUsingRCA)
    
    def DistanceAtAngle(self, candidatePoints, templatePoints, angle):
        newpoints = self.rotate(candidatePoints, angle)
        return PathDistance(newpoints, templatePoints)