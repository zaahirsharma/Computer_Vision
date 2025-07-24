import os
import cv2
import time

# Directory to save the collected images
DATA_DIR = './data'

# Make sure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# Number of classes and dataset size
number_of_classes = 3
dataset_size = 100


# Booting up camera for capture
cap = cv2.VideoCapture(0)
time.sleep(1)


# Loop to collect images for each class
for j in range(number_of_classes):
    # Create a subdirectory for each class
    storage_title = str(chr(j+65))  # A, B, C, ...
    if not os.path.exists(os.path.join(DATA_DIR, storage_title)):
        os.makedirs(os.path.join(DATA_DIR, storage_title))
    
    print(f'Collecting images for class {j}....')
    
    complete = False
    while True:
        # Read first frame
        ret, frame = cap.read()
        # Check if frame is captured successfully
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the frame and instructions
        cv2.putText(frame, 'Ready? Press "Q" to start collecting images', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Frame', frame)
        
        # Wait for 'Q' key to start collecting images
        if cv2.waitKey(25) == ord('q'):
            break
    
    counter = 0
    while counter < dataset_size:
        # Read the next frame
        ret, frame = cap.read()
        # Check if frame is captured successfully
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the frame
        cv2.imshow('Frame', frame)
        cv2.waitKey(25)
        # Save the frame as an image file for the current class
        cv2.imwrite(os.path.join(DATA_DIR, storage_title, '{}.jpg'.format(counter)), frame)
        
        counter += 1

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
        

