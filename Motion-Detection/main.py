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
            
    
    
        
        
        
        
        
        
        
        


 