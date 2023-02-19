from templates import template1
from constants import *
from math import sqrt
from recognizerUtils import *
from time import time

class Recognizer:
    def __init__(self, training_set=None):
        if training_set == None:
            self.template = template1.template
            self.preProcessTemplates()
        else:
            self.template = training_set

    def getPreProcessPoints(self, points):
        points = self.resample(points, SAMPLING_POINTS)
        points = self.rotate(points)
        points = self.scale(points, SCALE_FACTOR)
        points = self.translate(points, ORIGIN)
        return points

    # Apply the resampling, rotating, scaling and translate operations to templates    
    def preProcessTemplates(self):
        template = self.template
        self.template = {}
        for gesture in template.keys():
            points = template[gesture]
            points = self.getPreProcessPoints(points)
            self.template[gesture] = points
        # self.printTemplateStats()
    
    # Get individual gestures from template
    def getGestureFromTemplate(self, gesture):
        return self.template[gesture]
    
    # Used to print all the gesture names and the number of points in each gesture
    def printTemplateStats(self):
        for template,points in self.template.items():
            print(template,len(points))

    # Resample the points in a a user drawn gesture
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
    
    # Rotate the points in a user drawn gesture with a given angle or around the centroid
    def rotate(self, points, angle=None):
        centroid = getCentroid(points)
        if angle is None:
            angle = getIndicativeAngle(centroid, points[0])
        newpoints = []
        for i in range(len(points)):
            newpoints.append(getRotatedPoints(points[i],centroid,angle))
        return newpoints
    
    # Scale with respect to a bounding box which tightly encloses the gesture
    def scale(self, points, size):
        width, height = getBoundingBox(points)
        newpoints = []
        for point in points:
            newpoints.append([point[0]*(size/width), point[1]*(size/height)])
        return newpoints
    
    # Translate the points to the origin
    def translate(self, points, origin):
        centroid = getCentroid(points)
        newpoints = []
        for point in points:
            newpoints.append([point[0]+origin[0]-centroid[0], point[1]+origin[1]-centroid[1]])
        return newpoints

    # Recognize the gesture by comparing the user drawn gesture with template
    def recognizeGesture(self, points):
        startTime = time()
        bestDistance = float("inf")
        recognizedGesture = None
        for gesture, templatePoints in self.template.items():
            distance = self.DistanceAtBestAngle(points, templatePoints, radians(-45), radians(45), radians(2))
            if distance < bestDistance:
                bestDistance = distance
                recognizedGesture = gesture
        # Calculate confidence of best matching gesture template
        score = 1 - bestDistance/(0.5*sqrt(SCALE_FACTOR**2 + SCALE_FACTOR**2))
        endTime = time()
        return recognizedGesture, score, endTime - startTime

    # Get the optimal angle for best distance bewteen user drawn gesture and all templates
    def DistanceAtBestAngle(self, candidatePoints, templatePoints, leftBound, rightBound, threshold):
        leftConvergentAngle = getConvergentAngle(leftBound, rightBound, 'left')
        distanceUsingLCA = self.DistanceAtAngle(candidatePoints, templatePoints, leftConvergentAngle)
        rightConvergentAngle = getConvergentAngle(leftBound, rightBound, 'right')
        distanceUsingRCA = self.DistanceAtAngle(candidatePoints, templatePoints, rightConvergentAngle)
        while abs(rightBound - leftBound) > threshold:
            if distanceUsingLCA < distanceUsingRCA:
                # Search to the left of right bound
                rightBound = rightConvergentAngle
                rightConvergentAngle = leftConvergentAngle
                distanceUsingRCA = distanceUsingLCA
                leftConvergentAngle = getConvergentAngle(leftBound, rightBound, 'left')
                distanceUsingLCA = self.DistanceAtAngle(candidatePoints, templatePoints, leftConvergentAngle)
            else:
                # Search to the right of left bound
                leftBound = leftConvergentAngle
                leftConvergentAngle = rightConvergentAngle
                distanceUsingLCA = distanceUsingRCA
                rightConvergentAngle = getConvergentAngle(leftBound, rightBound, 'right')
                distanceUsingRCA = self.DistanceAtAngle(candidatePoints, templatePoints, rightConvergentAngle)
        return min(distanceUsingLCA, distanceUsingRCA)
    
    # Get distance between user drawn gesture and template after rotating with a given angle
    def DistanceAtAngle(self, candidatePoints, templatePoints, angle):
        newpoints = self.rotate(candidatePoints, angle)
        return PathDistance(newpoints, templatePoints)