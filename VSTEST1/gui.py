import os
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import speech_recognition as sr
import time
import pyaudio
from vosk import Model, KaldiRecognizer
from voice_to_sign import *  # Import everything from voice_to_sign.py

# Paths
PROJECT_PATH = "E:\\till the uppercase work 12.44\\till the uppercase work 12.44\\VSTEST1"
ALPHABET_IMAGES_PATH = os.path.join(PROJECT_PATH, "alphabetimages")
VIDEOS_PATH = os.path.join(PROJECT_PATH, "mp4videos")
VOSK_MODEL_PATH = os.path.join(PROJECT_PATH, "vosk-model-small-en-us-0.15")

# Load Vosk model
model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

class SignLanguageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Translator")
        self.root.geometry("1000x800")
        
        # Create display frame
        self.display_frame = ttk.Label(root)
        self.display_frame.pack(expand=True, fill='both')
        
        # Override cv2.imshow to display in Tkinter
        def custom_imshow(window_name, frame):
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image=img)
            self.display_frame.config(image=photo)
            self.display_frame.image = photo
            self.root.update()
            return cv2.waitKey(1)
            
        # Replace cv2.imshow with our custom function
        cv2.imshow = custom_imshow
        
        # Start the main loop from voice_to_sign.py
        self.root.after(100, self.start_main)
    
    def start_main(self):
        """Run the main loop from voice_to_sign.py"""
        try:
            if __name__ == "__main__":
                while True:  # Keep running until user chooses to quit
                    print("\nSelect an option:")
                    print("1: Real-time audio to sign")
                    print("2: Audio file to sign")
                    print("3: Text to sign")
                    print("4: Quit")
                    choice = input("Enter choice: ")
                    
                    if choice == "1":
                        recognize_speech_realtime()
                    elif choice == "2":
                        file_path = input("Enter audio file path: ")
                        text = process_audio_file(file_path)
                        print(f"Recognized text: {text}")
                        text_to_sign(text)
                    elif choice == "3":
                        text = input("Enter text: ")
                        text_to_sign(text)
                    elif choice == "4":
                        print("Thank you for using the Sign Language Translator!")
                        break  # Exit the program
                    else:
                        print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = SignLanguageGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 