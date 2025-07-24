import cv2
import sys
import time

# Function to select the tracker based on user choice for desired algorithm
def select_tracker(tracker_type):
    # If-else chain to check which type was selected
    if tracker_type == 'BOOSTING':
        return cv2.legacy.TrackerBoosting_create()
    elif tracker_type == 'MIL':
        return cv2.TrackerMIL_create()
    elif tracker_type == 'KCF':
        return cv2.TrackerKCF_create()
    elif tracker_type == 'TLD':
        return cv2.legacy.TrackerTLD_create()
    elif tracker_type == 'MEDIANFLOW':
        return cv2.legacy.TrackerMedianFlow_create()
    elif tracker_type == 'MOSSE':
        return cv2.legacy.TrackerMOSSE_create()
    elif tracker_type == 'CSRT':
        return cv2.TrackerCSRT_create()
    else:
        raise ValueError("Invalid tracker type. Choose from: BOOSTING, MIL, KCF, TLD, MEDIANFLOW, MOSSE, CSRT.")
    
    
def main():
    # Listing out tracker types for later print use
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
    # Print out options for user to select tracker type
    print("Select tracker type: \n")
    for i, _tracker in enumerate(tracker_types, 1):
        print(f"{i}. {_tracker}")
        
    # Get user input for tracker type selection 
    tracker_choice = int(input("Enter the number corresponding to your choice: \n")) - 1
    tracker_type = tracker_types[tracker_choice]
    
    tracker = select_tracker(tracker_type)
    
    # Prompt user for video file path or use webcam
    video_path = input("Enter the path to the video file (Leave blank to use webcam): \n")
    if not video_path:
        # Use webcam if no path is provided
        # On new macOS, the webcam is usually at index 1
        video = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    else:
        # Use the provided video file path
        video = cv2.VideoCapture(video_path)
        
    
    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        sys.exit()
        
    # Read the first frame from the video, store it in 'frame' with boolean ok for successful read
    ok, frame = video.read()
    
    # If no video path is provided, create static image of webcame frame for tracker selection
    if not video_path:
        time.sleep(1)
        ok, frame = video.read()
        cv2.imshow("Webcam", frame)
            
    
    if not ok:
        print("Error: Could not read video frame.")
        sys.exit()
        
    
    # Use OpenCV to select a bounding box for the object to track
    bbox = cv2.selectROI(frame, False)
    
    # Initialize the tracker with the first frame and the bounding box
    ok = tracker.init(frame, bbox)
    
    
    # Start tracking loop
    while True:
        # Read the next frame from the video
        ok, frame = video.read()
        
        # Check if frame was read successfully or end of video
        if not ok:
            break
        
        # Update the tracker with the new frame and get the updated bounding box
        ok, bbox = tracker.update(frame)
        
        # Check if object successfully found the object within the frame
        if ok: 
            # Define top left point of bounding box
            p1 = (int(bbox[0]), int(bbox[1]))
            # Define bottom right point of bounding box
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            # Draw rectangle on frame to show tracked object
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # In case of failed tracking
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        
        # Text to show which tracker is being used
        cv2.putText(frame, tracker_type, (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        
        # Show text on how to quit program
        cv2.putText(frame, "Press ESC to exit", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        
        cv2.imshow("Tracking", frame)
        
        # Check if ESC key was pressed to exit (27)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    # Release video capture and close all OpenCV windows
    video.release()
    cv2.destroyAllWindows()
    
    
if __name__ == "__main__":
    main()
        
    
    
    
    