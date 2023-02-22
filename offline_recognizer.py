from xml_parser import Parser
from recognizer import Recognizer
from copy import deepcopy
from random import randint
from json import dumps
import csv

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
        logcsv = []
        total=0
        correct=0
        for user in self.preProcessedData: # For each user
            score[user] = {}
            for example in range(1,3): # For each example from 1 to 9
                score[user][example] = {}
                for i in range(1,2): # For iterations from 1 to 10
                    # print(len(self.preProcessedData[user]['medium']))
                    # print(len(self.preProcessedData[user]['medium']['arrow']))
                    # print(len(self.preProcessedData[user]['medium']['arrow'][0]))
                    training_set, testing_set = self.getSplitData(self.preProcessedData[user]['medium'], example)
                    # print(len(training_set))
                    # print(len(testing_set))
                    recognizer = Recognizer(training_set)

                    for gesture,points in testing_set.items():
                        # print(gesture)
                        if gesture not in score[user][example]:
                            score[user][example][gesture] = 0
                        recognizedGesture, _, _,Nbest = recognizer.recognizeGesture(points)
                        # print(recognizedGesture)
                        log = {'User':user,'Gesture':gesture,'Iteration':i,'Example':example,'TrainingSize':len(training_set),'TrainingContents':training_set,'RecognizedGesture':recognizedGesture.split('/')[0],'CorrectIncorrect':0 if recognizedGesture.split('/')[0]==gesture else 1,'RecoResult':list(Nbest.values())[0],'RecoResultBestMatch[specific-instance]':recognizedGesture,'Nbest':Nbest}
                        
                        logcsv.append(log)
                        recognizedGesture = recognizedGesture.split('/')[0] if recognizedGesture!=None else ''
                        if recognizedGesture == gesture:
                            score[user][example][gesture] += 1
                            correct+=1
                        total+=1

        print((correct/total)*100)               
        self.writeToFile(dumps(score), 'score.json')
        self.writeToCsv(logcsv,'logfile.csv')
    

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
                

    def writeToCsv(self,dict_data,filename):
        csv_columns = ['User','Gesture','Iteration','Example','TrainingSize','TrainingContents','RecognizedGesture','CorrectIncorrect','RecoResult','RecoResultBestMatch[specific-instance]','Nbest']
        csv_file=filename
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
