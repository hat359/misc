from tkinter import Canvas, Button,Label
from constants import * # importing from constants.py
from copy import deepcopy
from recognizer import Recognizer

class Board:
    def __init__(self, root):
        self.root = root
        self.createWidgets()
        self.setBindings()
        self.points = []
        self.recognizer = Recognizer()

    def createWidgets(self):
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)
        self.resampleButton = Button(self.root, text=RESAMPLE)
        self.resampleButton.place(x=100,y=100)
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)
        self.predictedGestureLabel = Label(self.root)
        self.confidenceLabel = Label(self.root)
        

    def setBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_DRAG_MODE, self.draw) 
        self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        self.board.pack()

        #Creating bindings for clear button
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack()

        self.resampleButton.configure(command=self.onResampleButtonClick)
        self.resampleButton.pack()

        self.predictedGestureLabel.pack()
        self.confidenceLabel.pack()

    def onClearButtonClick(self): # clicking the clear button fires this function.
        self.points.clear() 
        self.board.delete(BOARD_DELETE_MODE) # clears everything on the canvas
        self.predictedGestureLabel.configure(text="")
        self.confidenceLabel.configure(text="")
        print(LOG_BOARD_CLEARED)

    def draw(self, event): # the main function that generates the strokes on the canvas. 
        x1 = (event.x-2)
        y1 = (event.y-2)
        x2 = (event.x+2)
        y2 = (event.y+2)
        self.board.create_oval(x1, y1, x2, y2, fill=BLUE, outline=BLUE)
        self.points.append([event.x,event.y])

    def reDraw(self, points, color,fxn):
        if fxn == "resample":
            for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+200, y1, x2+200, y2, fill=color, outline=color)

        if fxn == "rotated":
            for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+400, y1+100, x2+400, y2+100, fill=color, outline=color)
        
        if fxn == "scaled":
             for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+400, y1, x2+400, y2, fill=color, outline=color)

        
    def mouseUp(self, event):# logs the mouseup event. 
        print(LOG_DRAWING_FINISHED)

    def onResampleButtonClick(self):
        resampledPoints = self.recognizer.resample(deepcopy(self.points), SAMPLING_POINTS)
        self.reDraw(resampledPoints, RED,"resample")
        rotatedPoints = self.recognizer.rotate(resampledPoints)
        self.reDraw(rotatedPoints, ORANGE,"rotated")
        scaledPoints = self.recognizer.scale(rotatedPoints, SCALE_FACTOR)
        translatedPoints = self.recognizer.translate(scaledPoints, ORIGIN)
        self.reDraw(translatedPoints, GREEN,"scaled")
        recognizedGesture = self.recognizer.recognizeGesture(translatedPoints)
        print(recognizedGesture[0])
        self.predictedGestureLabel.configure(text="Predicted Gesture = "  + str(recognizedGesture[0]))
        self.confidenceLabel.configure(text="Confidence = "  + str(recognizedGesture[1]))