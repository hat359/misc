PART 1

Component A - Setup a development environment
    We have setup our python development environment using VSCode and we would be using the tkinter library to handle the GUI requirements. We used the python debugger (pdb) to debug the code. We also log whenever the user clears the canvas and when the drawing is over (time to recognise!).

The project is divided into 3 files. Their usecases are listed below:

    1. main.py
        This file will function as the main script of the whole project. It creats a tkinter object called root on line 5. It creates a board object of our user defined class Board on line 6 and starts the tkinter mainloop on line 7.

    2. board.py
        This python module contains the class Board to handle tkinter logic.

    3. constants.py
        This python module contains constants which will be used throughout the project.

Component B - Instantiating a Canvas
    This logic is handled in the board.py module. In the createWidgets() method we instantiate the canvas on line 12.

Component C - Listening for mouse touch events
    This logic is handled in the board.py module. To listen to mouse touch events we bind the canvas with the draw() method on line 18 and mouseUp() method on line 19. The draw() method spans lines 31-36. It handles touch events and makes a small oval on the coordinates where the mouse drag event happens.

Component D - Clearing the canvas
    This logic is handled in the board.py module. We instantiate a button for clearing the canvas on line 14 in board.py. We bind the clear button with a handler method onClearButtonClick() which spans line 27-29. This method deletes everything on the canvas when called. It also logs when the user has clicked the clear canvas button.

Running the Code - 
    Run the code from the main.py file. 

    For example -> python3 -u "/Users/harsh/Desktop/Spring-2023/HCIRA/main.py"

Interaction - 
    1. Draw on the canvas with mouse or touch (laptops with touch screens). 
    2. Click on the clear button to clear the canvas.   



Part 2 

Component A - Store the points
When a mouse drag or screen touch event happens the draw method of board.py(lines 45-51) is triggered. It draws the points as well as stores the input in the points array on line 51.

Component B - Storing the templates
The template with 16 gestures is loaded in the template directory in the template.py file. It is then loaded into the recognizer module on line 8 on recognizer.py.

Component C -Implement the 1$ algorithm
Resampling 
    The resampling is triggered when the drawing is over(when mouse is up). It fires up the onMouseUp function in the recognizer.py file. 
    It calculates the average distance between each point and if the distance between two adjacent points is greater 
    than the calculated average distance it inserts a new point in between them by interpolating it. 

Rotate 
    The centroid of the figure is calculated by running the rotate function in the recognizer.py file. It finds the indicative angle, which is the angle made between x-asix and the line passing through the centroid and the start-point of the figure. It the rotates the drawing by that indicative angle.

Scale 
    The scale function is run which first calculates the coordinates of the bounding box and its height and width which basically indicates the total height and width of the figure. It then calculates the new points by multiplying each point by a constant value. This value is calculated by dividing the scale factor by the width for all the x coordinates and by height for all the y coordinates.

Translate 
    The translate function is run which takes an input of the destination coordinates to where the figure is to be translated.It then calculates the distance between the centroid and the destination coordinates(which is the origin) and then adds the difference to the x and y coordinates of each point.

Recognition
    After resampling, rotating, scaling and translating both the user defined input and all the gestures in the template. For each user input, and for each gesture we find the best angle for which the distance between that user input and gesture is minimum. Then we compare these distances and find the gesture which has the minimum distance from user input which will be the ouput of the recognition. We also return the confidence score of the recignition for that gesture.

Component D - Output the result

When the recognizer.py module return the predicted gesture and the confidence score we print them using their respective lables on the canvas. We also display the resampled(red), rotated(orange) and scaled(green) figures seperately. 
