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
        self.lx = 0
        self.ly=0

    def createWidgets(self):
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)
        self.predictedGestureLabel = Label(self.root)
        self.confidenceLabel = Label(self.root)
        

    def setBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_CLICK,self.lastcoordinates)
        self.board.bind(MOUSE_DRAG_MODE, self.draw) 
        self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        self.board.pack()

        #Creating bindings for clear button
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack()

        # Create bindings for predicted gesture label and confidence label
        self.predictedGestureLabel.pack()
        self.confidenceLabel.pack()

    # Handler for clear button click
    def onClearButtonClick(self):
        self.points.clear() 
        # Clears everything on the canvas
        self.board.delete(BOARD_DELETE_MODE)
        self.predictedGestureLabel.configure(text="")
        self.confidenceLabel.configure(text="")
        print(LOG_BOARD_CLEARED)

    def lastcoordinates(self,event):
        global lx,ly
        self.lx,self.ly=event.x,event.y

    # Draws when mouse drag or screen touch event occurs
    def draw(self, event):
        global lx,ly
        self.board.create_line((self.lx, self.ly, event.x, event.y),fill='red')
        self.points.append([event.x,event.y])
        self.lx, self.ly = event.x,event.y

    # Draws different states of user input (resampled,rotated,scaled)
    def reDraw(self, points, color,fxn):
        # if fxn == "resample":
        #     for i in range(len(points)):
        #         x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
        #         self.board.create_oval(x1+200, y1, x2+200, y2, fill=color, outline=color)

        # if fxn == "rotated":
        #     for i in range(len(points)):
        #         x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
        #         self.board.create_oval(x1+400, y1+100, x2+400, y2+100, fill=color, outline=color)
        
        # if fxn == "scaled":
        #      for i in range(len(points)):
        #         x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
        #         self.board.create_oval(x1+400, y1, x2+400, y2, fill=color, outline=color)
        print('done')

    # Mouse up event handler
    def mouseUp(self, event):
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
        print(LOG_DRAWING_FINISHED)