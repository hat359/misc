Team Members - Harsh Athavale & Abdul Samadh Azath 


Component A - Read in Dataset. 
    The xml files were stored locally from the 1$ website and stored in 
    the xml_logs folder. The xml_parser.py file reads in the gesture points 
    for each gesture for each speed for each user. 


Component 2 - Connect to Recognizer 
    We created a new file named offline_recognizer.py. 

    1. In this we load the xml data into a python dictionary.
    2. We load the previously created recognizer module in this and use it to preprocess the data using the preProcessOfflineData(Line 19) function. 
    
    

Component 3 - Loop over Dataset

    1. We split the data into training and testing templates using the getSplitData(Line 88) function and load 
       the recognizer with training set for each user, example and gesture.
    2. We then test the inputs using testing data against the training examples in the same order and output the N-best list. 
    3. The Nbest list is calculated in the recognizer.py(Line 94) file. 
    3. We record the accuracy of recognitions for each user and the overall accuracy of the recognitions. 


Component 4 - Output Results 

    We output all the following results to the logfile.csv file using the writeToCsv function (Line 111). 

    'User','Gesture Type','RandomIteration','#ofTrainingExamples',
    'TotalSizeOfTrainingSet','Training Set Contents','Candidate',
    'RecoResult','Correct or Incorrect','RecoResultScore',
    'RecoResultBestMatch','RecoResultNBestSorted'

    We also output the overall accuracy and the accuracy per user per example. 


    NOTE --> To view the accuracy in the logfile scroll to the end of the logfile. 