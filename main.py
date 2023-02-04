from tkinter import Tk #tkinter library for GUI 
from board import Board #board.py contains all the functions. 

def main():
    root = Tk() #initializig the tkinter lib. 
    board = Board(root) 
    root.mainloop()

if __name__ == '__main__':
    main()