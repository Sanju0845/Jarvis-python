import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie
import speech_recognition as sr
import pyttsx3

class SpeechRecognitionThread(QThread):
    commandChanged = pyqtSignal(str)

    def run(self):
        engine = pyttsx3.init()
        engine.say("Initialzing system? All protocols are up to mark?  Hello sir!")
        engine.runAndWait()

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            while True:
                audio = recognizer.listen(source)
                try:
                    command = recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")
                    self.commandChanged.emit(command)
                except sr.UnknownValueError:
                    print("Sorry, I didn't understand that.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

class JarvisGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Jarvis Assistant')
        self.setGeometry(100, 100, 400, 400)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create QLabel to display GIF
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)

        # Load and display the initial GIF
        self.current_gif = 'C:/Users/Sukumar Pavan Soma/Favorites/Downloads/intmainn.gif'
        self.load_gif(self.current_gif)

        # Add the GIF label to the layout
        layout.addWidget(self.gif_label)

        # Set the layout for the window
        self.setLayout(layout)

        # Start speech recognition thread
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.commandChanged.connect(self.process_command)
        self.speech_thread.start()

        # Show the window
        self.show()

    def load_gif(self, path):
        movie = QMovie(path)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        self.gif_label.setMovie(movie)
        movie.start()

    def process_command(self, command):
        if " jarvis" in command:
            self.load_gif('C:/Users/Sukumar Pavan Soma/Favorites/Downloads/jarvisanim.gif')
        if "jarvis" in command:
            self.say("Yes, sir. How may I help you today?")
        
        else:
            self.say("I'm sorry, sir. I don't understand.")

    def say(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = JarvisGUI()
    sys.exit(app.exec_())
