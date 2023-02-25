#Authors - Harsh Athavale & Abdul Samadh Azath

from tkinter import Tk #tkinter library for GUI 
from board import Board #board.py contains all the functions. 
from offline_recognizer import OfflineRecognizer
from recognizer import Recognizer

def main():
    startOnlineRecognizer()
    # startOfflineRecognizer()

def startOnlineRecognizer():
    root = Tk() #initializig the tkinter lib. 
    recognizer = Recognizer()
    board = Board(root, recognizer) 
    root.mainloop()

def startOfflineRecognizer():
    offlineRecognizer = OfflineRecognizer()

if __name__ == '__main__':
    main()