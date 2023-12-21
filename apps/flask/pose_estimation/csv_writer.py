# Use this file for writing to a new csv to train a new model
# Import Statements
import cv2
import mediapipe as mp
import numpy as np
import csv
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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

video_path = "example.mp4"

# use 0 as argument if webcam is desired
cap = cv2.VideoCapture(video_path)

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Code for creating csv final -> not used in final version
# angles = ['class', 'shLA', 'elLA', 'shRA', 'elRA']
# with open('angles.csv', mode='w', newline='') as f:
#     csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     csv_writer.writerow(angles)

# Used for writing to csv file to train model
# DO NOT FORGET TO UPDATE THIS
class_name = "Pose 6"

# Delay to help with setting up the poses
# time.sleep(2)

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

                # Add to the csv file (not used for the final code)
                angles_row.insert(0, class_name)
                with open('angles.csv', mode='a', newline='') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(angles_row)

        except:
            pass

        cv2.imshow("Window Name", image)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()