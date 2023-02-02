from tkinter import *
from constants import *

class Board:
    def __init__(self, root):
        self.root = root
        self.createWidgets()
        self.setBindings()

    def createWidgets(self):
        # Creating canvas
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)
        # Creating clear button
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)

    def setBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_DRAG_MODE, self.draw) 
        self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        self.board.pack()


        #Creating bindings for clear button
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack()

    def onClearButtonClick(self):
        self.board.delete(BOARD_DELETE_MODE)
        print(LOG_BOARD_CLEARED)

    def draw(self, event):
        x1 = (event.x-2)
        y1 = (event.y-2)
        x2 = (event.x+2)
        y2 = (event.y+2)
        self.board.create_oval(x1, y1, x2, y2, fill=DRAW_FILL, outline=DRAW_OUTLINE)

    def mouseUp(self, event):
        print(LOG_DRAWING_FINISHED)