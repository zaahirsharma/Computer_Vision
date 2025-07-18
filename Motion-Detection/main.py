import cv2
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class MotionDetectionApp:
    def __init__(self, root):
        # Store root window as an instance variable to access across class
        self.root = root
        # Set title of motion detection window
        self.root.title("Motion Detection App")
        # Set window size
        self.root.geometry("300x150")
        
        # Create start button calling the start_detection method
        self.start_button = ttk.Button(root, text="Start Motion Detection", command=self.start_detection)
        # Add button to window with padding
        self.start_button.pack(pady=10)
        
        # Create stop button calling the stop_detection method
        self.stop_button = ttk.Button(root, text="Stop Motion Detection", command=self.stop_detection, state=tk.DISABLED)
        # Add button to window with padding
        self.stop_button.pack(pady=10)
        
        # Add status label to show current state of motion detection
        self.status_label = ttk.Label(root, text="Status: Not running")
        # Add label to window with padding
        self.status_label.pack(pady=5)
        
        # Initialize flag to check if motion detection is running
        self.running = False
        # Initialize video capture object
        self.cap = None
        
        
    # Method to start motion detection
    def start_detection(self):
        # Set running flag to True
        self.running = True
        # Disable start button since motion detection is running
        self.start_button.configure(state=tk.DISABLED)
        # Enable stop button since motion detection is running
        self.stop_button.configure(state=tk.NORMAL)
        # Update status label to show motion detection is running
        self.status_label.configure(text="Status: Running")
        # Call detect_motion to motion detection process
        self.detect_motion()
        
    
    # Method to stop motion detection
    def stop_detection(self):
        # Set running flag to False
        self.running = False
        # Enable start button since motion detection is stopped in order to restart motion detection
        self.start_button.configure(state=tk.NORMAL)
        # Disable stop button since motion detection is stopped
        self.stop_button.configure(state=tk.DISABLED)
        # Update status label to show motion detection is stopped
        self.status_label.configure(text="Status: Not running")
        
        # Check if have active video capture object
        if self.cap:
            # Release video capture object
            self.cap.release()
            # Close all OpenCV windows
            cv2.destroyAllWindows()
            
    
    # Method to detect motion using OpenCV 
    def detect_motion(self):
        # Use webcam for motion detection
        # On new macOS, the webcam is usually at index 1
        self.cap = cv2.VideoCapture(1)  
        
        # Allow camera to warm up
        time.sleep(1)  
        # Read the first frame
        _, prev_frame = self.cap.read()  
        
        # Convert the first frame to grayscale for easier processing
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to the first frame to reduce noise
        prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
        
        # Loop until motion detection is stopped
        while(self.running):
            _, frame = self.cap.read()
            # Convert the frame to grayscale for easier processing
            frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            # Apply Gaussian blur to the frame to reduce noise
            frame = cv2.GaussianBlur(prev_gray, (21, 21), 0)
            
            # Compute the absolute difference between the current frame and the previous frame
            # Detect any changes to confirm motion
            delta_frame = cv2.absdiff(prev_gray, frame)
            # Threshold the delta frame to get a binary image
            thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
            # Dilate the thresholded image to fill in holes, white regions larger (motion areas)
            thresh = cv2.dilate(thresh, None, iterations=2)
            
            # Find contours (outlines of the white areas) in the thresholded image to detect motion areas
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Process each contour to check if it is large enough to be considered motion
            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue
                # Draw a rectangle around the detected motion area
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display the current frame with motion detection rectangles
            cv2.imshow("Motion Detection", frame)
            # Check for key press to exit the loop
            key = cv2.waitKey(1) & 0xFF
            
            # If 'q' is pressed or running flag is False, break the loop
            if key == ord('q') or not self.running:
                break
            
            # Update the previous frame and previous gray frame for the next iteration
            prevy_gray = gray.copy()
            
        # Stop motion detection
        self.stop_detection()
        
        
        
        
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Instance of MotionDetectionApp
    app = MotionDetectionApp(root)
    
    # Start the main loop of the application
    root.mainloop()

                
                
    
        
        
        
        
        
        
        
        


 