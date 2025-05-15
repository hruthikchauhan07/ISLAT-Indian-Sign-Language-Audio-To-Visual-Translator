#let's go 
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
def resize_image(image_path, output_size=(800,500)):
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
    isl_gif = ['address', 'ahemdabad', 'all', 'any questions', 'are you angry', 'are you hungry', 'assam', 'august', 
    'banana', 'banaras', 'banglore', 'be careful', 'bridge', 'cat', 'christmas', 'church', 'clinic', 'dasara', 
    'december', 'did you finish homework', 'do you have money', 'do you want something to drink', 'do you watch TV', 
    'dont worry', 'flower is beautiful', 'good afternoon', 'good morning', 'good question', 'grapes', 'hello', 
    'hindu', 'hyderabad', 'i am a clerk', 'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 
    'i go to a theatre', 'i had to say something but I forgot', 'i like pink colour', 'i love to shop', 'job', 
    'july', 'june', 'karnataka', 'kerala', 'krishna', 'lets go for lunch', 'mango', 'may', 'mile', 'mumbai', 
    'nagpur', 'nice to meet you', 'open the door', 'pakistan', 'please call me later', 'police station', 
    'post office', 'pune', 'punjab', 'saturday', 'shall I help you', 'shall we go together tommorow', 'shop', 
    'sign language interpreter', 'sit down', 'stand up', 'take care', 'temple', 'there was traffic jam', 
    'thursday', 'toilet', 'tomato', 'tuesday', 'usa', 'village', 'wednesday', 'what is the problem', 
    'what is today\'s date', 'what is your father do', 'what is your name', 'whats up', 'where is the bathroom', 
    'where is the police station', 'you are wrong']

    arr = list(string.ascii_lowercase) + list(string.digits)

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

                if a == 'goodbye world':
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
                        root1.title("Indian Sign Language Interpreter")
                        lbl = ImageLabel(root1)
                        lbl.pack()
                        lbl.load(gif_path)
                        root1.mainloop()
                    else:
                        print(f"Gif file {gif_path} does not exist.")

                else:  # If phrase is not found, break it into individual letters or digits
                    for idx, char in enumerate(a):
                        if char in arr:
                            if char.isdigit():
                                # Generate and display the digit as an image using matplotlib
                                plt.clf()
                                plt.text(0.5, 0.5, char, fontsize=120, ha='center', va='center')
                                plt.axis('off')
                                plt.draw()
                                plt.pause(0.8)
                                # Flicker effect for consecutive same digits
                                if idx + 1 < len(a) and a[idx + 1] == char:
                                    plt.clf()
                                    plt.pause(0.1)
                            else:
                                image_address = os.path.join("D:/Downloads/ISLAT/Indian-Sign-Language-Audio-Visual-Translator/letters", f"{char}.jpg")
                                if os.path.exists(image_address):
                                    img = Image.open(image_address)
                                    img_array = np.asarray(img)
                                    plt.imshow(img_array)
                                    plt.axis('off')
                                    plt.draw()
                                    plt.pause(0.8)
                                    # Flicker effect for consecutive same letters
                                    if idx + 1 < len(a) and a[idx + 1] == char:
                                        plt.clf()
                                        plt.pause(0.1)
                                else:
                                    print(f"Image file {image_address} does not exist.")

            except Exception as e:
                print(f"Sorry, I could not process your speech. Please try speaking again louder:   {e}")
            plt.close()

# Main loop for UI interaction
while True:
    image_path = "D:/Downloads/ISLAT/mainpage.jpeg"
    resized_image_path = resize_image(image_path, output_size=(800, 600))  # Resize before display

    if resized_image_path:
        msg = "INDIAN SIGN LANGUAGE AUDIO VISUAL TRANSLATOR [ISLAT]"
        choices = ["Input Live Voice", "Terminate!"]
        reply = buttonbox(msg, image=resized_image_path, choices=choices)

        if reply == choices[0]:
            func()
        elif reply == choices[1]:
            print("Exiting program.....")
            break
    else:
        break

print("Program terminated!!.")
