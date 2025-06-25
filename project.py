import pyttsx3
import webbrowser
import os
import psutil
import winsound
import datetime
import speech_recognition as sr
import tkinter as tk
import threading


# Initialize Text-to-Speech
speaker = pyttsx3.init()
speaker.setProperty('rate', 150)

def speak(text):
    speaker.say(text)
    speaker.runAndWait()


def beep():
    duration = 300
    freq = 700
    winsound.Beep(freq, duration)

# Time-based Greeting
now = datetime.datetime.now()
hour = int(now.strftime("%H"))

if 0 <= hour < 12:
    greeting = "Good Morning"
elif hour == 12:
    greeting = "Good Noon"
elif 12 < hour < 17:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

# Setup recognizer & mic
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.7
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.3

mic = sr.Microphone(device_index=0)

# Do ambient noise adjustment once
with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.2)

# Initial Greeting
speak(f"Hlo! {greeting}")
speak("I am your Personal Voice Assistant..")

def run_assistant():
# Voice Command Loop
    while True:
        with mic as source:
            print("waiting to wake me up.!!")
            try:
                wake = recognizer.listen(source, timeout=100, phrase_time_limit=5)
                wake_text = recognizer.recognize_google(wake)

                print("Heard:", wake_text)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                speak("Network issue.")
                continue

        if wake_text.lower() in ["hlo voxa", "voxa"]:   
            beep() 
            speak("Yes ! I am Listening.")
            speak("How can I help You Today?")
            with mic as source:
                print("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio)
                    print("You said:", text)
                except sr.WaitTimeoutError:
                    print("No speech detected. Waiting again...")
                    continue
                except sr.UnknownValueError:
                    speak("Sorry, I could not understand the audio.")
                    continue
                except sr.RequestError:
                    speak("Weak Internet Connection.")
                    continue

        # Commands

            command = text.lower()
            if command in ["open youtube", "youtube"]:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com/")

            elif command in ["google", "open google"]:
                speak("Opening Google")
                webbrowser.open("https://www.google.com/")

            elif command in ["weather", "open weather", "what's is the today's weather", "today's weather"]:
                speak("Okay wait..")
                webbrowser.open("https://www.google.com/search?q=current+weather")

            elif command in ["chatgpt", "open chat gpt"]:
                speak("Opening ChatGPT")
                webbrowser.open("https://chatgpt.com/?model=auto")

            elif command in ["image", "showing images"]:
                speak("Which type of image you want to see?")
                print("Listening for image type...")
                with mic as source:
                    try:
                        audio2 = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                        image_type = recognizer.recognize_google(audio2)
                        print("You said:", image_type)
                        speak(f"Showing {image_type} images")
                        webbrowser.open(f"https://www.google.com/search?q={image_type}+images")
                    except sr.UnknownValueError:
                        speak("Sorry, I could not understand the image type.")
                    except sr.WaitTimeoutError:
                        speak("You didn't say anything for image type.")
                    continue

            elif command in ["current time", "time", "and what about the current time", "please tell me current time"]:
                curr_time = datetime.datetime.now().strftime("%I:%M %p")
                print(f"The current time is {curr_time}")
                speak(f"The current time is {curr_time}")

            elif command in ["today's date", "date", "and what about the today's date", "please tell me today's date"]:
                date = datetime.datetime.now().strftime("%d %B %Y")
                day = datetime.datetime.now().strftime("%A")
                print(f"Today's Date is {date} and day is {day}")
                speak(f"Today's Date is {date} and day is {day}")

            elif command in ["wikipedia", "open wikipedia"]:
                speak("What do you want to search?")
                print("Listening for Wikipedia search...")
                with mic as source:
                    try:
                        audio3 = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                        search = recognizer.recognize_google(audio3)
                        print("You searched:", search)
                        speak(f"Showing {search} page on Wikipedia")
                        webbrowser.open(f"https://en.wikipedia.org/wiki/{search}")
                    except sr.UnknownValueError:
                        speak("Sorry, I could not understand your search.")
                    except sr.WaitTimeoutError:
                        speak("You didn’t say anything.")
                    continue
        


            elif "play music" in command:
                speak("Which type of song wanna you hear..")
                print("Listening for song type...")
                with mic as source:
                    try:
                        audio4 = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                        music = recognizer.recognize_google(audio4)
                        print("You searched:", music)
                        speak(f"Playing {music} song on YouTube.")
                        webbrowser.open(f"https://www.youtube.com/results?search_query={music}+music")
                    except sr.UnknownValueError:
                        speak("Sorry, I could not understand your search.")    
        
            elif command in ["calculator", "open calculator"]:
                speak("Opening Calculator")
                os.system("calc.exe")
            
            elif text.lower() in ["open notepad", "start notepad"]:
                speak("Opening Notepad")
                os.system("notepad.exe")
            
            elif text.lower() in ["open settings", "settings", "open windows settings", "open setting", "setting", "open windows setting"]:
                speak("Opening Settings")
                os.system("start ms-settings:")

            elif text.lower() in ["battery", "battery percent" , "what is my battery percent", "battery sattus"]:
                battery = psutil.sensors_battery()
                percent=battery.percent
                if (percent<=25):
                    speak(f"{percent} percent is your battery percentage and You need to plug your laptop")
                else:    
                    speak(f"{percent} percent is your battery percentage")


            elif command in ["exit", "shutdown", "leave", "shut up"]:
                speak("Okay, permit to Exit")
                break

        
        elif wake_text.lower() != "wake up":
            continue





def start_gui():
    root = tk.Tk()
    root.configure(bg="black")
    root.title("Voice Assistant Controller")
    root.geometry("300x250")

    tk.Label(root, text="𝐕𝐨𝐢𝐜𝐞 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭", font=("Arial", 25)).pack(pady=10)
    
    def start_thread():
        threading.Thread(target=run_assistant).start()

    tk.Button(root, text="🎙𝐒𝐭𝐚𝐫𝐭 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭", command=start_thread, bg="green", fg="white",font=("Arial", 15)).pack(pady=10)
    tk.Button(root, text="❌ 𝐄𝐱𝐢𝐭", command=root.quit, bg="red", fg="white",font=("Arial", 15)).pack(pady=10)

    root.mainloop()

# Launch the GUI
start_gui()
