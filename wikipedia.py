import speech_recognition as sr
import pyttsx3
import webbrowser
import pyautogui
import time
import openai  # Make sure to install OpenAI Python package

engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Set your OpenAI GPT-3.5 API key
openai.api_key = "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"

def say(text, volume=1.0):
    engine.setProperty('volume', volume)
    engine.say(text)
    engine.runAndWait()

def set_volume(volume):
    volume = max(0, min(volume, 100))
    volume /= 100
    engine.setProperty('volume', volume)

def search_openai(query):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can experiment with different models
            prompt=f"Search for: {query}\n",
            temperature=0.7,
            max_tokens=200,
            n=1,
            stop=None
        )
        result = response.choices[0].text.strip()
        return result
    except Exception as e:
        print(f"Error during OpenAI search: {e}")
        return "Sorry, I couldn't complete the search."

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
            time.sleep(2)
        elif "resume" in command:
            pyautogui.hotkey('k')
            time.sleep(2)
        elif "close youtube" in command:
            say("Closing youtube, sir.")
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(2)
        elif "search for" in command:
            search_query = command.split("search for")[1].strip()
            result = search_openai(search_query)
            say(result)
        else:
            say("I'm sorry, sir. I don't understand.")
            time.sleep(2)
