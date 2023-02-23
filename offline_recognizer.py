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
        # Load offline data
        self.offlineData = self.parser.getOfflineData()
        # Pre process offline data
        self.preProcessOfflineData()
        # Recognize offline data
        self.recognizeOfflineData()

    def preProcessOfflineData(self):
        self.preProcessedData = deepcopy(self.offlineData)
        for user in self.offlineData:
            for speed in self.offlineData[user]:
                for gesture in self.offlineData[user][speed]:
                    self.preProcessedData[user][speed][gesture] = []
                    for points in self.offlineData[user][speed][gesture]:
                        # Pre processing loaded xml data using the preprocesser function in recognizer
                        self.preProcessedData[user][speed][gesture].append(self.recognizer.getPreProcessPoints(points))
        # print(len(self.preProcessedData['s02']['medium']['arrow'][0]))
        # print(len(self.offlineData['s02']['medium']['arrow'][0]))
    
    def recognizeOfflineData(self):
        score = {}
        logcsv = []
        total=0
        correct=0
        iterations = 1
        examples_start, examples_end = 1,9
        for user in self.preProcessedData: # For each user
            if user != 's07':
                continue
            score[user] = {}
            for example in range(examples_start,examples_end+1): # For each example from 1 to 9
                score[user][example] = {}
                for i in range(1,iterations+1): # For iterations from 1 to 10
                    # print(len(self.preProcessedData[user]['medium']))
                    # print(len(self.preProcessedData[user]['medium']['arrow']))
                    # print(len(self.preProcessedData[user]['medium']['arrow'][0]))
                    
                    # Get training and testing set
                    training_set, testing_set = self.getSplitData(self.preProcessedData[user]['medium'], example, user)
                    # print(len(training_set))
                    # print(len(testing_set))
                    recognizer = Recognizer(training_set)

                    for gesture_raw,points in testing_set.items():
                        gesture = gesture_raw.split('-')[0]
                        if gesture not in score[user][example]:
                            score[user][example][gesture] = 0
                        recognizedGesture_raw, recognitionScore, _,Nbest = recognizer.recognizeGesture(points)
                        recognizedGesture = recognizedGesture_raw.split('-')[0]
                        # print(recognizedGesture)
                        log = {}
                        log['User'] = user
                        log['Gesture Type'] = gesture
                        log['RandomIteration'] = i
                        log['#ofTrainingExamples'] = example
                        log['TotalSizeOfTrainingSet'] = len(training_set)
                        log['Training Set Contents'] = [key for key in training_set]
                        log['Candidate'] = gesture_raw
                        log['RecoResult'] = recognizedGesture
                        log['Correct or Incorrect'] = 1 if recognizedGesture == gesture else 0
                        log['RecoResultScore'] = round(recognitionScore,3)
                        log['RecoResultBestMatch'] = recognizedGesture_raw
                        log['RecoResultNBestSorted'] = self.getTopN(Nbest,50)
                        
                        logcsv.append(log)
                        if recognizedGesture == gesture:
                            score[user][example][gesture] += 1
                            correct+=1
                        total+=1
        totalAverageAccuracy = (correct/total)*100    
        self.writeToFile(dumps(score), 'score.json')
        self.writeToCsv(logcsv,'logfile.csv', totalAverageAccuracy, score, iterations, examples_end-examples_start+1)
    

    def getSplitData(self, gestures, E, user):
        training_set = {}
        testing_set = {}
        for gesture,points in gestures.items(): # For each gesture pick E training examples and 1 testing example
            for i in range(0,E):
                training_set["{}-{}-E{}".format(gesture,user,i+1)] = points[i]
            testing_example = randint(E,9)
            testing_set["{}-{}-E{}".format(gesture,user, testing_example+1)] = points[testing_example]
        return training_set, testing_set
    
    def writeToFile(self, data, filename):
        file = open(filename, 'w')
        file.write(data)
        file.close()
    
    def getTopN(self, Nbest, N):
        if len(Nbest) > N:
            return {value[0]:value[1] for i, value in enumerate(Nbest.items()) if i <= N}
        else:
            return Nbest
            
    def writeToCsv(self,dict_data,filename, totalAverageAccuracy, score, iterations, eRange):
        csv_columns = ['User','Gesture Type','RandomIteration','#ofTrainingExamples','TotalSizeOfTrainingSet','Training Set Contents','Candidate','RecoResult','Correct or Incorrect','RecoResultScore','RecoResultBestMatch','RecoResultNBestSorted']
        csv_file=filename
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
                writer.writerow({})
                writer.writerow({'User':'Total Average Accuracy', 'Gesture Type':totalAverageAccuracy})
                for user in score:
                    for example in score[user]:
                        gestureSum = 0
                        for gesture in score[user][example]:
                            gestureSum += score[user][example][gesture]
                        gestureAccuracy = ((gestureSum/(16*iterations)))*100
                        writer.writerow({'User':'Accuracy for User:{} E:{}'.format(user,example),'Gesture Type':gestureAccuracy})
        except IOError:
            print("I/O error")
