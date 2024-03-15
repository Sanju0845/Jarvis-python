import speech_recognition as sr
import pyttsx3
import webbrowser
import pyautogui
import time

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def say(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            say("Sorry, I couldn't hear you. Can you please repeat?")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            say("Sorry, I'm having trouble accessing the speech recognition service.")

if __name__ == '__main__':
    say("Hello, sir!")
    while True:
        command = listen()
        if "hey jarvis" in command:
            say("Yes, sir!")
            time.sleep(2)
        elif "play" in command:
            song = command.replace("play", "").strip()
            url = f"https://www.youtube.com/results?search_query={song}"
            webbrowser.open(url)
            time.sleep(5)
            pyautogui.click(x=440, y=365)
            time.sleep(2)
            pyautogui.click(x=942, y=530)
            time.sleep(2)
        elif "pause" in command:
            pyautogui.hotkey('k')
            time.sleep(1)
        elif "resume" in command:
            pyautogui.hotkey('k')
            time.sleep(1)
        elif "close google" in command:
            say("Closing Google, sir.")
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(1)
        else:
            say("I'm sorry, sir. I don't understand.")
            time.sleep(1)
