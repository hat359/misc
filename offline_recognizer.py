from xml_parser import Parser
from recognizer import Recognizer
from copy import deepcopy
from random import randint
from json import dumps

class OfflineRecognizer():
    def __init__(self):
        self.parser = Parser()
        self.recognizer = Recognizer()
        self.offlineData = self.parser.getOfflineData()
        self.preProcessOfflineData()
        self.recognizeOfflineData()

    def preProcessOfflineData(self):
        self.preProcessedData = deepcopy(self.offlineData)
        for user in self.offlineData:
            for speed in self.offlineData[user]:
                for gesture in self.offlineData[user][speed]:
                    self.preProcessedData[user][speed][gesture] = []
                    for points in self.offlineData[user][speed][gesture]:
                        self.preProcessedData[user][speed][gesture].append(self.recognizer.getPreProcessPoints(points))
        # print(len(self.preProcessedData['s02']['medium']['arrow'][0]))
        # print(len(self.offlineData['s02']['medium']['arrow'][0]))
    
    def recognizeOfflineData(self):
        score = {}
        for user in self.preProcessedData: # For each user
            score[user] = {}
            for example in range(1,10): # For each example from 1 to 9
                score[user][example] = {}
                for i in range(1,11): # For iterations from 1 to 10
                    # print(len(self.preProcessedData[user]['medium']))
                    # print(len(self.preProcessedData[user]['medium']['arrow']))
                    # print(len(self.preProcessedData[user]['medium']['arrow'][0]))
                    training_set, testing_set = self.getSplitData(self.preProcessedData[user]['medium'], example)
                    # print(len(training_set))
                    # print(len(testing_set))
                    recognizer = Recognizer(training_set)
                    for gesture,points in testing_set.items():
                        if gesture not in score[user][example]:
                            score[user][example][gesture] = 0
                        recognizedGesture, _, _ = recognizer.recognizeGesture(points)
                        recognizedGesture = recognizedGesture.split('/')[0] if recognizedGesture!=None else ''
                        if recognizedGesture == gesture:
                            score[user][example][gesture] += 1
        self.writeToFile(dumps(score), 'score.json')
    

    def getSplitData(self, gestures, E):
        training_set = {}
        testing_set = {}
        for gesture,points in gestures.items(): # For each gesture pick E training examples and 1 testing example
            for i in range(0,E):
                training_set["{}/{}".format(gesture,i)] = points[i]
            testing_set[gesture] = points[randint(E,9)]
        return training_set, testing_set
    
    def writeToFile(self, data, filename):
        file = open(filename, 'w')
        file.write(data)
        file.close()
                

