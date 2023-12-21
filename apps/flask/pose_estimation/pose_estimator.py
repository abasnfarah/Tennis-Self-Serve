# Import Statements
import cv2
import mediapipe as mp
import numpy as np
import csv
import os
import pickle
import pandas as pd
import pyttsx3

NUM_POSES = 6

# Function used to calculate the angle of a joint
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

# This function creates a numpy array of the user's averaged joint angles through all the phases of the serve
def write_user(avg_shR,avg_shL,avg_elR,avg_elL):
    # write the header row
    user_data = np.empty((NUM_POSES+1, 5), dtype=object)
    angles = ['class', 'shLA', 'elLA', 'shRA', 'elRA']
    class_name = ["Pose 1", "Pose 2", "Pose 3", "Pose 4", "Pose 5", "Pose 6"]
    user_data[0] = angles
    user_data[1:,0] = class_name
    user_data[1:,1] = avg_shL
    user_data[1:,2] = avg_elL
    user_data[1:,3] = avg_shR
    user_data[1:,4] = avg_elR
    return user_data

# This function writes the string to be returned as feedback to the user
def write_feedback(user_data):
    with open('pro_angles.csv', mode='r', newline='') as pro:
        # read in each as numpy array
        pro_data = np.genfromtxt(pro, delimiter=',', skip_header=1, usecols=(1, 2, 3, 4))
        # iterate over each row
        diff = pro_data - user_data
        abs_diff = np.abs(diff)
        # Find the index of the maximum absolute value
        max_diff_index = np.unravel_index(np.argmax(abs_diff), abs_diff.shape)
        # Get the element with the largest absolute value
        max_abs_value = abs_diff[max_diff_index]
        long_text = ["left shoulder angle", "left elbow angle", "right shoulder angle", "right elbow angle"]
        str = f"The biggest difference between you and the pro was during pose {max_diff_index[0]}, where your {long_text[max_diff_index[1]]} was off by {round(max_abs_value)}."
        return str

# This function plays the given text. I have no idea how it would work on the app.
def play_feedback(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# This function takes the file path of video
def generate_feedback(video_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # use 0 as argument if webcam is desired
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        exit()

    fdbk_shLA = [[] for _ in range(NUM_POSES)]
    fdbk_shRA = [[] for _ in range(NUM_POSES)]
    fdbk_elLA = [[] for _ in range(NUM_POSES)]
    fdbk_elRA = [[] for _ in range(NUM_POSES)]

    not_vis = 0

    with open('serve_est.pkl', 'rb') as f:
        model = pickle.load(f)

    with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract Landmarks, Find Angles, Export Angles
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                shLC = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elLC = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrLC = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                hiLC = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                
                shRC = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elRC = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrRC = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                hiRC = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                landmark_indices = [11, 12, 13, 14, 15, 16, 23, 24]
                if any(landmarks[index].visibility < 0.5 for index in landmark_indices):
                    # pass
                    # throw some sort of error out: saying joint not visible
                    not_vis = not_vis + 1
                else:
                    # Find angles
                    shLA = calculate_angle(hiLC, shLC, elLC)
                    elLA = calculate_angle(shLC, elLC, wrLC)
                    shRA = calculate_angle(hiRC, shRC, elRC)
                    elRA = calculate_angle(shRC, elRC, wrRC)
                    # Export angles 
                    angles_row = list(np.array([shLA, elLA, shRA, elRA]).flatten())

                    # Make Detections
                    X_names = ['shLA', 'elLA', 'shRA', 'elRA']
                    X = pd.DataFrame([angles_row], columns=X_names)
                    serve_class = model.predict(X)[0]
                    serve_probs = model.predict_proba(X)[0]
                    serve_prob = round(serve_probs[np.argmax(serve_probs)], 2)

                    # Display the class and probability, for testing
                    text_to_display = f"Class: {serve_class}, Probability: {serve_prob}"
                    # print(text_to_display)
                    cv2.putText(image, text_to_display, (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(shRA)), tuple(np.multiply(shRC, [1920, 1080]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(round(elRA)), tuple(np.multiply(elRC, [1920, 1080]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(round(shLA)), tuple(np.multiply(shLC, [1920, 1080]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(round(elLA)), tuple(np.multiply(elLC, [1920, 1080]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                    
                    # display pose
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

                    # Update Feedback Data Structure
                    if serve_prob > 0.5:
                        # extract the pose number
                        pose_num = int(serve_class.split()[1]) - 1
                        # append shoulder angle
                        fdbk_shRA[pose_num].append(shRA)
                        fdbk_shLA[pose_num].append(shLA)
                        # append elbow angle
                        fdbk_elRA[pose_num].append(elRA)
                        fdbk_elLA[pose_num].append(elLA)

            except:
                pass
            
            # Do not have it show in the app, idk what would happen
            # cv2.imshow("Window Name", image)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()

    # calculate averages
    avg_shR = [0]*NUM_POSES
    avg_shL = [0]*NUM_POSES
    avg_elR = [0]*NUM_POSES
    avg_elL = [0]*NUM_POSES
    for i in range(NUM_POSES):
        avg_shR[i] = sum(fdbk_shRA[i]) / len(fdbk_shRA[i])
        avg_shL[i] = sum(fdbk_shLA[i]) / len(fdbk_shLA[i])
        avg_elR[i] = sum(fdbk_elRA[i]) / len(fdbk_elRA[i])
        avg_elL[i] = sum(fdbk_elLA[i]) / len(fdbk_elLA[i])

    # Write averages to csv
    user_data = write_user(avg_shR,avg_shL,avg_elR,avg_elL)
    fdbk = write_feedback(user_data)
    return(fdbk)
