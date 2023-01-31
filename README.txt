PART 1

Component A - Setup a development environment
We have setup our python development environment using VSCode and we would be using the tkinter library to handle the GUI requirements. We used the python debugger (pdb) to debug the code. We also log whenever the user clears the canvas.

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
This logic is handled in the board.py module. To listen to mouse touch events we bind the canvas with the draw() method on line 18. The draw() method spans lines 30-35. It handles touch events and makes a small oval on the coordinates where the mouse drag event happens.

Component D - Clearing the canvas
This logic is handled in the board.py module. We instantiate a button for clearing the canvas on line 14 in board.py. We bind the clear button with a handler method onClearButtonClick() which spans line 26-28. This method deletes everything on the canvas when called. It also logs when the user has clicked the clear canvas button.