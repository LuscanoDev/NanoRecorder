import cv2
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import filedialog
import threading

class ScreenRecorder:
    def __init__(self):
        self.recording = False

        # Get the size of the screen using pyautogui
        self.SCREEN_SIZE = tuple(pyautogui.size())

        # Define the codec and create VideoWriter object
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = None

        # Create the GUI
        self.root = tk.Tk()
        self.root.title("NanoRecorder")

        # Set the size and position of the window
        self.root.geometry("400x150")
        self.root.resizable(False, False)
        self.root.configure(bg="#FFFFFF")

        # Add a label for the file path
        self.path_label = tk.Label(self.root, text="Output file: ", font=("Helvetica", 10), bg="#FFFFFF")
        self.path_label.pack(pady=10)

        # Add a button to select the output file location
        self.file_button = tk.Button(self.root, text="Select File", font=("Helvetica", 10), command=self.select_file)
        self.file_button.pack()

        # Add a button to start recording
        self.start_button = tk.Button(self.root, text="Start Recording", font=("Helvetica", 10), command=self.start_recording)
        self.start_button.pack(pady=10)

        # Add a button to stop recording
        self.stop_button = tk.Button(self.root, text="Stop Recording", font=("Helvetica", 10), command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

    def select_file(self):
        # Ask the user to select the output file location
        self.file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        self.path_label.config(text="Output file: " + self.file_path)

    def start_recording(self):
        # Start recording the screen
        if not self.file_path:
            return
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Define the VideoWriter object with the selected file path
        self.out = cv2.VideoWriter(self.file_path, self.fourcc, 20.0, self.SCREEN_SIZE)

        # Create a thread to handle the screen recording
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def record_screen(self):
        while self.recording:
            # Capture the screen
            img = pyautogui.screenshot()

            # Convert the image into numpy array
            img = np.array(img)

            # Convert the color space from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the current position of the mouse
            mouse_x, mouse_y = pyautogui.position()

            # Draw a circle at the current mouse position
            cv2.circle(img, (mouse_x, mouse_y), 5, (0, 0, 255), -1)

            # Write the frame into the file
            self.out.write(img)

        self.out.release()

    def stop_recording(self):
        # Stop recording the screen
        self.recording = False
        self.recording_thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    recorder = ScreenRecorder()
    recorder.run()
