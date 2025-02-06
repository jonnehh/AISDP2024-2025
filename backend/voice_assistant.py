import pyttsx3
import speech_recognition as sr

class VoiceAssistant:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.commands = {
            "add reminder": self.add_reminder,
            "show reminders": self.show_reminders,
            "delete all reminders": self.delete_all_reminders
        }

    def speak(self, text):
        """Speak the given text aloud."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listen for a voice command."""
        with sr.Microphone() as source:
            print("Listening...")
            self.speak("I'm listening.")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
            except sr.RequestError:
                self.speak("There was an error with the recognition service.")
            except Exception as e:
                self.speak("An error occurred.")
                print(f"Error: {e}")
            return None

    def add_reminder(self):
        """Interactively add a reminder."""
        self.speak("What time should I set the reminder for?")
        time = self.listen()
        if time:
            self.speak("What medicine should I remind you to take?")
            medicine = self.listen()
            if medicine:
                return {"time": time, "medicine": medicine}
        self.speak("Failed to add the reminder.")
        return None

    def show_reminders(self):
        """Respond with a list of reminders."""
        # Replace with API call to get reminders
        return "Here are your reminders."

    def delete_all_reminders(self):
        """Delete all reminders."""
        # Replace with API call to delete reminders
        return "All reminders have been deleted."

    def handle_command(self, command):
        """Handle recognized voice commands."""
        for trigger, action in self.commands.items():
            if trigger in command:
                response = action()
                if response:
                    if isinstance(response, dict):
                        self.speak(f"Reminder set for {response['medicine']} at {response['time']}.")
                    else:
                        self.speak(response)
                return
        self.speak("Sorry, I don't know that command.")


if __name__ == "__main__":
    assistant = VoiceAssistant()
    print("Testing Voice Assistant. Speak commands like 'add reminder' or 'show reminders'.")
    while True:
        command = assistant.listen()
        if command:
            assistant.handle_command(command)
