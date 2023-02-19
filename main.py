from tkinter import Tk #tkinter library for GUI 
from board import Board #board.py contains all the functions. 
from xml_parser import Parser
from recognizer import Recognizer
from copy import deepcopy

def main():
    # onlineRecognizer()
    offlineRecognizer()

def onlineRecognizer():
    root = Tk() #initializig the tkinter lib. 
    board = Board(root) 
    root.mainloop()

def offlineRecognizer():
    parser = Parser()
    recognizer = Recognizer()
    offlineData = parser.getOfflineData()
    preProcessedData = deepcopy(offlineData)
    for user in offlineData:
        for speed in offlineData[user]:
            for gesture in offlineData[user][speed]:
                preProcessedData[user][speed][gesture] = []
                for points in offlineData[user][speed][gesture]:
                    preProcessedData[user][speed][gesture].append(recognizer.getPreProcessPoints(points))
    print(len(preProcessedData['s02']['medium']['arrow'][0]))
    print(len(offlineData['s02']['medium']['arrow'][0]))

if __name__ == '__main__':
    main()