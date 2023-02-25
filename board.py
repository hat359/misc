#Authors - Harsh Athavale & Abdul Samadh Azath

from tkinter import Canvas, Button, Label, Text
from constants import * # importing from constants.py
from copy import deepcopy
from recognizer import Recognizer
from database import Database
from random import shuffle

class Board:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        if self.mode == 'recognition':
            self.createCanvas()
            self.createClearButton()
            self.createPredictionLabels()
            self.points = []
            self.recognizer = Recognizer()
            self.startPointX = 0
            self.startPointY = 0
        elif self.mode == 'collection':
            self.gestureList = GESTURE_LIST
            self.currentUserId = 'sampleUser'
            self.currentGesture = 'sampleGesture'
            self.points = []
            self.startPointX = 0
            self.startPointY = 0
            self.createCanvas()
            self.createClearButton()
            # # To be added
            # 1. DB module to store user points with user id in a json - Done
            self.db = Database()
            self.db.addUser('sampleUser')
            # 2. Show sample drawing on top right
            # 3. Add button to submit user input - Done
            self.createSubmitButton()
            # 4. Add label to show prompt to be drawn - Done
            self.createPromptLabel()
            self.setPromptLabel('Prompt label sample text.')
            # 5. Add logic to show prompt and store points - Inprogress
            # 6. Add text box to get user ID and any other user data
            # 7. Convert json(database.json) to xml
    
    # def collectFromUser(self, userId):
    #     # Delete any existing user with same userId in DB and start fresh
    #     self.db.addUser(userId)
    #     for iteration in range(10):
    #         shuffle(self.gestureList)
    #         for gesture in self.gestureList:
    #             self.setPromptLabel('Please draw a {}'.format(gesture))

    
    def createCanvas(self):
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)
        self.setMouseBindings()
        self.board.pack()

    def createUserIdTextBox(self):
        self.userIdTextBox = Text(self.root, width=TEXT_BOX_WITDH, height=TEXT_BOX_HEIGHT)

    def createClearButton(self):
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack()

    def createSubmitButton(self):
        self.submitButton = Button(self.root, text=SUBMIT_BUTTON_TEXT)
        self.submitButton.configure(command=self.onSubmitButtonClick)
        self.submitButton.pack()

    def createPredictionLabels(self):
        self.predictedGestureLabel = Label(self.root)
        self.confidenceLabel = Label(self.root)
        self.timelabel = Label(self.root)
        # Create bindings for predicted gesture label and confidence label
        self.predictedGestureLabel.pack()
        self.confidenceLabel.pack()
        self.timelabel.pack()
    
    def setPredictionLabels(self, recognizedGesture, score, time):
        self.predictedGestureLabel.configure(text="Predicted Gesture = "  + str(recognizedGesture))
        self.confidenceLabel.configure(text="Confidence = "  + str(round(score,2))) 
        self.timelabel.configure(text="Time = "  + str(round(time*1000,2)) + " ms" )

    def clearPredictionLables(self):
        self.predictedGestureLabel.configure(text="")
        self.timelabel.configure(text="")
        self.confidenceLabel.configure(text="")
    
    def createPromptLabel(self):
        self.promptLabel = Label(self.root)
        self.promptLabel.pack()
    
    def setPromptLabel(self,message):
        self.promptLabel.configure(text=message)

    def setMouseBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_CLICK,self.getLastCoordinates)
        self.board.bind(MOUSE_DRAG_MODE, self.draw)
        if self.mode == 'recognition':
            self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        
    # Handler for clear button click
    def onClearButtonClick(self):
        self.points.clear() 
        # Clears everything on the canvas
        self.board.delete(BOARD_DELETE_MODE)
        print(LOG_BOARD_CLEARED)
    
    def onSubmitButtonClick(self):
        print("Before:",self.db.getData())
        self.db.addGesture(self.currentUserId, self.currentGesture, deepcopy(self.points))
        print("After:", self.db.getData())
        self.points.clear()

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
        self.setPredictionLabels(recognizedGesture, score, time)
        print(LOG_DRAWING_FINISHED)