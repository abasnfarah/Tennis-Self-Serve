Dependencies, requirements, and how to use these files

Make sure to have installed the following:
    opencv, mediapipe, numpy, pickle, and pandas
If wanting to train your own models, also install
    scikit-learn
Run the following commands to install them:
> pip install mediapipe opencv-python
> pip install scikit-learn

The main file and function you will need to interact with is 
"generate_feedback(video_path)" found in the "pose_estimator.py" 
file. Import the file, and call this function, passing in the 
path to a video, such as "example.mp4". The function returns a 
string, currently formatted to provide very rudimentary feedback. 
This is subject to updates. There is another function called 
"play_feedback(text)" with takes in text as a parameter and plays 
the text. I am not certain how this will work on mobile but I know 
it works on a laptop. 
A requirement that I know needs to be met is that mediapipe 
does not work with python 3.13, I needed to use 3.11. 

If anything else is confusing let me know I am not sure what else
needs to be clarified.