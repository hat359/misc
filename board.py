#Authors - Harsh Athavale & Abdul Samadh Azath

from tkinter import Canvas, Button,Label
from constants import * # importing from constants.py
from copy import deepcopy
from recognizer import Recognizer

class Board:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        if self.mode == 'recognition':
            self.createCanvas()
            self.createClearButton()
            self.createPredictionLabels()
            self.setMouseBindings()
            self.setClearButtonBindings()
            self.setPredictionLabelsBindings()
            self.points = []
            self.recognizer = Recognizer()
            self.startPointX = 0
            self.startPointY = 0
        elif self.mode == 'collection':
            self.points = []
            self.startPointX = 0
            self.startPointY = 0
            self.createCanvas()
            self.createClearButton()
            self.setMouseBindings()
            self.setClearButtonBindings()
            # # To be added
            # 1. DB module to store user points with user id in a json
            # 2. Show sample drawing on top right
            # 3. Add button to submit user input
            # 4. Add label to show prompt to be drawn
            # 5. Add logic to show prompt and store points
            # 6. Add text box to get user ID and any other user data
            # 7. Convert json to xml 
    
    def createCanvas(self):
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)

    def createClearButton(self):
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)

    def createPredictionLabels(self):
        self.predictedGestureLabel = Label(self.root)
        self.confidenceLabel = Label(self.root)
        self.timelabel = Label(self.root)     

    def setMouseBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_CLICK,self.getLastCoordinates)
        self.board.bind(MOUSE_DRAG_MODE, self.draw)
        if self.mode == 'recognition':
            self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        self.board.pack()
    
    def setClearButtonBindings(self):
        #Creating bindings for clear button
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack()

    def setPredictionLabelsBindings(self):
        # Create bindings for predicted gesture label and confidence label
        self.predictedGestureLabel.pack()
        self.confidenceLabel.pack()
        self.timelabel.pack()

    # Handler for clear button click
    def onClearButtonClick(self):
        self.points.clear() 
        # Clears everything on the canvas
        self.board.delete(BOARD_DELETE_MODE)
        print(LOG_BOARD_CLEARED)

    def getLastCoordinates(self,event):
        self.startPointX,self.startPointY=event.x,event.y

    # Draws when mouse drag or screen touch event occurs
    def draw(self, event):
        self.board.create_line((self.startPointX, self.startPointY, event.x, event.y),fill=BLUE,width=5)
        self.points.append([event.x,event.y])
        self.startPointX, self.startPointY = event.x,event.y

    # Draws different states of user input (resampled,rotated,scaled)
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

    def populateLabels(self, recognizedGesture, score, time):
        self.predictedGestureLabel.configure(text="Predicted Gesture = "  + str(recognizedGesture))
        self.confidenceLabel.configure(text="Confidence = "  + str(round(score,2))) 
        self.timelabel.configure(text="Time = "  + str(round(time*1000,2)) + " ms" )

    def clearLables(self):
        self.predictedGestureLabel.configure(text="")
        self.timelabel.configure(text="")
        self.confidenceLabel.configure(text="")

    # Mouse up event handler
    def mouseUp(self, event):
        resampledPoints = self.recognizer.resample(deepcopy(self.points), SAMPLING_POINTS)
        # self.reDraw(resampledPoints, RED,"resample")
        rotatedPoints = self.recognizer.rotate(resampledPoints)
        # self.reDraw(rotatedPoints, ORANGE,"rotated")
        scaledPoints = self.recognizer.scale(rotatedPoints, SCALE_FACTOR)
        translatedPoints = self.recognizer.translate(scaledPoints, ORIGIN)
        # self.reDraw(translatedPoints, GREEN,"scaled")
        recognizedGesture, score, time , _= self.recognizer.recognizeGesture(translatedPoints)
        self.populateLabels(recognizedGesture, score, time)
        print(LOG_DRAWING_FINISHED)