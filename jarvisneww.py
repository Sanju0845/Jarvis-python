import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie
import speech_recognition as sr
import pyttsx3
import time

class SpeechRecognitionThread(QThread):     #microphone listening
    commandChanged = pyqtSignal(str)

    def run(self):
        engine = pyttsx3.init()
        engine.say("Analyzing system. All protocols up to mark? Hello sir!")
        engine.runAndWait()

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                print("Listening...")
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
        self.listening_start_time = time.time()  # Initialize listening start time
        self.engine = pyttsx3.init()  # Initialize the pyttsx3 engine

    def initUI(self):    #adding first initilizing gif to window
        # Set window properties
        self.setWindowTitle('Jarvis Assistant')
        self.setGeometry(400, 100, 400, 400)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create QLabel to display GIF and listening status
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setStyleSheet("border: 2px solid black;")  # Add border to differentiate GIF area

        # Create QLabel for listening status and commands
        self.text_label = QLabel(self.gif_label)  # Set the GIF label as the parent
        self.text_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)  # Align text to top center
        self.text_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); padding: 5px; border-radius: 5px;")

        # Load and display the initial GIF
        self.current_gif = 'C:/Users/Sukumar Pavan Soma/Favorites/Downloads/intmainn.gif'  # Adjust the paths accordingly
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

    def load_gif(self, path):    #loading intilizing gif
        movie = QMovie(path)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        movie.start()
        self.gif_label.setMovie(movie)

    def process_command(self, command):    #commands for jarvis with second jarvisgui gif
        self.update_text("Listening...")
        if "hey jarvis" in command:
            self.say("Yes, sir. How may I help you today?")
            self.load_gif('C:/Users/Sukumar Pavan Soma/Favorites/Downloads/jarvisanim.gif')  # Load the startup GIF
            self.listening_start_time = time.time()  # Update listening start time
        elif "time entha" in command or "what is time" in command:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.say(f"The current date and time is {current_time}")
            self.listening_start_time = time.time()  # Update listening start time
        elif "shutdown jarvis" in command:
            self.close()  # Close the application if shutdown command is recognized
        elif "lock the pc" in command:
            # Lock the PC
            os.system("rundll32.exe user32.dll,LockWorkStation")
            self.say("Locking the PC, sir.")  # Update assistant response to acknowledge the command
            self.update_text("PC locked")  # Update GUI with confirmation message
        else:
            self.say("I'm sorry, sir. I don't understand.")

        self.update_text(command)

    def say(self, text):      #engine running to listen
        self.engine.say(text)
        self.engine.runAndWait()

    def update_text(self, text):    #show status of printing the listened prompt
        self.text_label.setText(text)

if __name__ == '__main__':       #end
    app = QApplication(sys.argv)
    gui = JarvisGUI()
    sys.exit(app.exec_())
