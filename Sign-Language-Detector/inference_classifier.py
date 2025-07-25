import cv2
import time
import mediapipe as mp
import pickle
import numpy as np


# Load the trained model
model_dict = pickle.load(open('./model.pickle', 'rb'))
model = model_dict['model']



# Initialize the video capture object
cap = cv2.VideoCapture(0)
time.sleep(1)

# 3 Objects that detect landmarks, draw landmarks, and styles
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Hands object to detect landmarks
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)


while True:
    
    data_aux = []
    x_ = []
    y_ = []
    
    # Read a frame from the camera
    ret, frame = cap.read()
    
    H, W, _ = frame.shape
    
    # Check if the frame was captured successfully
    if not ret:
        print("Failed to capture frame from camera.")
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
    # Process the image and detect hands with landmarks
    results = hands.process(frame_rgb)
    
    # Check if at least 1 hand is detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
        # Iterate through landmarks on the image
        for hand_landmarks in results.multi_hand_landmarks:
            # Create array from all langmarks on image
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                # Append the x and y coordinates of each landmark
                data_aux.append(x)
                data_aux.append(y)
                x_.append(x)
                y_.append(y)
        
        # Get the corners of the rectangle around the detected hand
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10
        
        # Use model to predict the sign language gesture, import data_aux numpy array as list
        prediction = model.predict([np.asarray(data_aux)])
        
        predicted_char = prediction[0]
        print(f"Predicted Character: {predicted_char}")
    
        # Draw a rectangle around the detected hand
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        # Put the predicted character on the frame
        cv2.putText(frame, predicted_char, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,0), 3, cv2.LINE_AA)
    
    # Display instructions on the frame
    cv2.putText(frame, 'Press "Q" to exit', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
    # Display the frame in a window
    cv2.imshow('Camera Feed', frame)
    # Wait for 10 milliseconds 
    cv2.waitKey(1)
    
    if cv2.waitKey(1) == ord('q'):
        break


# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
    





