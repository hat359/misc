from tkinter import *
from board import Board

def main():
    root = Tk()
    board = Board(root)
    root.mainloop()

if __name__ == '__main__':
    main()