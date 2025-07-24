import os
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
import pickle

# 3 Objects that detect landmarks, draw landmarks, and styles
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Hands object to detect landmarks
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

# Initialize lists to store data and labels
data = []
labels = []

# Iterate through the directories in DATA_DIR
for dir_ in os.listdir(DATA_DIR):
    # Iterate through the images in each directory
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = []
        # Define image path
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        # Convert the image to RGB to input image to MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect hands with landmarks
        results = hands.process(img_rgb)
        
        # Check if at least 1 hand is detected
        if results.multi_hand_landmarks:
            # Iterate through landmarks on the image
            for hand_landmarks in results.multi_hand_landmarks:
                # Create array from all langmarks on image
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    # Append the x and y coordinates of each landmark
                    data_aux.append(x)
                    data_aux.append(y)
                    
            # Append the data for the current image
            data.append(data_aux)
            # Append the label corresponding to the directory
            labels.append(dir_)
    
        
        
f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
        