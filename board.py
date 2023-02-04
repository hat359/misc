from tkinter import *
from constants import * # importing from constants.py
import math

class Board:
    points=[]
    def __init__(self, root):
        self.root = root
        self.createWidgets()
        self.setBindings()

    def createWidgets(self):
        # Creating canvas
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)
        # Creating clear button
        self.re = Button(self.root, text=RESAMPLE)
        self.re.place(x=100,y=100)
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)
        

    def setBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_DRAG_MODE, self.draw) 
        self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        self.board.pack()


        #Creating bindings for clear button
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack()

        self.re.configure(command=self.onResample)
        self.re.pack()

    def onClearButtonClick(self): # clicking the clear button fires this function. 
        self.board.delete(BOARD_DELETE_MODE) # clears everythin on the canvas
        print(LOG_BOARD_CLEARED)

    def draw(self, event): # the main function that generates the strokes on the canvas. 
        x1 = (event.x-2)
        y1 = (event.y-2)
        x2 = (event.x+2)
        y2 = (event.y+2)
        self.board.create_oval(x1, y1, x2, y2, fill=DRAW_FILL, outline=DRAW_OUTLINE) # creates a point on the canvas. Multiple such points are created which represents a shape. 
        Board.points.append([event.x,event.y])
        
    def mouseUp(self, event):# logs the mouseup event. 
        print(LOG_DRAWING_FINISHED)


    def onResample(self):
        # print(Board.points)
        newpt = self.Resample(Board.points,50)
        for p in Board.points:
            x1 = (p[0]+100-2)
            y1 = (p[1]-2)
            x2 = (p[0]+100+2)
            y2 = (p[1]+2)
            self.board.create_oval(x1, y1, x2, y2, fill='red', outline=DRAW_OUTLINE)
        # print(newpt)
        


    def Resample(self,points, n):
        I = self.PathLength(points) / (n - 1) # interval length
        D = 0.0
        newpoints = [points[0]]
        for i in range(1, len(points)):
            print(len(points))
            d = self.Distance(points[i-1], points[i])
            if (D + d) >= I:
                qx = points[i-1][0] + ((I - D) / d) * (points[i][0] - points[i-1][0])
                qy = points[i-1][1] + ((I - D) / d) * (points[i][1] - points[i-1][1])
                q = [qx, qy]
                newpoints.append(q) # append new point 'q'
                points.insert(i, q) # insert 'q' at position i in points s.t. 'q' will be the next i
                Board.points.insert(i, q)
                D = 0.0
            else:
                D += d
        if len(newpoints) == n - 1: # somtimes we fall a rounding-error short of adding the last point, so add it if so
            newpoints.append(points[-1])
        return newpoints



    def PathLength(self,points):
        d = 0.0
        for i in range(1, len(points)):
            d += self.Distance(points[i - 1], points[i])
        return d

    def Distance(self,p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx**2 + dy**2)


