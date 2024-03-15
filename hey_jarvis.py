import speech_recognition as sr
import pyttsx3

# pip install SpeechRecognition pyttsx3

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def say(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Use PocketSphinx for offline recognition
        command = recognizer.recognize_sphinx(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    say("Hello sir, good morning!.")
    while True:
        command = listen()
        if "jarvis" in command:
            say("Yes, sir. How may I help you today?")
        else:
            say("I'm sorry, sir. I don't understand.")
