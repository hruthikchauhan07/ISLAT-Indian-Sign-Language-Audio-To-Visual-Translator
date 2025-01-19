


import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string

# Function to resize an image before displaying it
def resize_image(image_path, output_size=(800, 400)):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize(output_size, Image.LANCZOS)  # Using LANCZOS instead of ANTIALIAS
        resized_path = "resized_image.jpeg"
        img.save(resized_path)  # Save resized image
        return resized_path
    else:
        print(f"Image file {image_path} does not exist.")
        return None


def func():
    r = sr.Recognizer()  # Initialize recognizer
    isl_gif = ['hello', 'good morning', 'thank you', 'where is the bathroom', 'i am fine', 'yes', 'no']  # Add more phrases

    arr = list(string.ascii_lowercase)

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print('Say something...')
            audio = r.listen(source)
            try:
                a = r.recognize_google(audio).lower()
                print(f"You said: {a}")

                for c in string.punctuation:
                    a = a.replace(c, "")

                if a == 'goodbye':
                    print("Exiting voice recognition.")
                    break

                elif a in isl_gif:
                    class ImageLabel(tk.Label):
                        """A label that displays images and plays GIFs."""
                        def load(self, im):
                            if isinstance(im, str):
                                im = Image.open(im)
                            self.loc = 0
                            self.frames = []
                            try:
                                for i in count(1):
                                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                                    im.seek(i)
                            except EOFError:
                                pass
                            try:
                                self.delay = im.info['duration']
                            except:
                                self.delay = 100

                            if len(self.frames) == 1:
                                self.config(image=self.frames[0])
                            else:
                                self.next_frame()

                        def unload(self):
                            self.config(image=None)
                            self.frames = None

                        def next_frame(self):
                            if self.frames:
                                self.loc += 1
                                self.loc %= len(self.frames)
                                self.config(image=self.frames[self.loc])
                                self.after(self.delay, self.next_frame)

                    gif_path = os.path.join("D:/Downloads/ISLAT/Indian-Sign-Language-Audio-Visual-Translator/ISL_Gif", f"{a}.gif")
                    if os.path.exists(gif_path):
                        root1 = tk.Tk()
                        root1.title("Sign Language Interpreter")
                        lbl = ImageLabel(root1)
                        lbl.pack()
                        lbl.load(gif_path)
                        root1.mainloop()
                    else:
                        print(f"Gif file {gif_path} does not exist.")

                else:  # If phrase is not found, break it into individual letters
                    for char in a:
                        if char in arr:
                            image_address = os.path.join("D:/Downloads/ISLAT/Indian-Sign-Language-Audio-Visual-Translator/letters", f"{char}.jpg")
                            if os.path.exists(image_address):
                                img = Image.open(image_address)
                                img_array = np.asarray(img)
                                plt.imshow(img_array)
                                plt.axis('off')
                                plt.draw()
                                plt.pause(0.8)
                            else:
                                print(f"Image file {image_address} does not exist.")

            except Exception as e:
                print(f"Could not listen: {e}")
            plt.close()

# Main loop for UI interaction
while True:
    image_path = "D:/Downloads/ISLAT/Indian-Sign-Language-Audio-Visual-Translator/mainpage.jpeg"
    resized_image_path = resize_image(image_path, output_size=(800, 400))  # Resize before display

    if resized_image_path:
        msg = "INDIAN SIGN LANGUAGE AUDIO VISUAL TRANSLATOR [ISLAT]"
        choices = ["Live Voice", "All Done!"]
        reply = buttonbox(msg, image=resized_image_path, choices=choices)

        if reply == choices[0]:
            func()
        elif reply == choices[1]:
            print("Exiting program.")
            break
    else:
        break

print("Program terminated.")


