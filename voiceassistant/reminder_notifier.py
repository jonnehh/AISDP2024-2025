import requests
import psycopg2
import pygame
import os
import time
from dotenv import load_dotenv

load_dotenv()

# API Keys
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
ELEVEN_LABS_VOICE_ID = os.getenv("ELEVEN_LABS_VOICE_ID")

# Database Configuration
DB_CONFIG = {
    "dbname": "reminders_db",
    "user": "postgres",
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "localhost",
    "port": "5432"
}

class ReminderNotifier:
    def __init__(self):
        pygame.mixer.init()

    def get_upcoming_reminders(self):
        """Fetch reminders that match the current time."""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            current_time = time.strftime('%H:%M')
            cursor.execute("SELECT medicine FROM reminders WHERE TO_CHAR(reminder_time, 'HH24:MI') = %s", (current_time,))
            reminders = cursor.fetchall()
            cursor.close()
            conn.close()
            return [r[0] for r in reminders] if reminders else []
        except Exception as e:
            print(f"❌ Database Error: {e}")
            return []

    def generate_speech(self, text):
        """Generate speech using Eleven Labs API."""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_LABS_VOICE_ID}"
        headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json"}
        response = requests.post(url, json={"text": text}, headers=headers)
        if response.status_code == 200:
            with open("reminder.mp3", "wb") as f:
                f.write(response.content)
            return "reminder.mp3"
        return None

    def play_audio(self, file):
        """Play the reminder audio."""
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def check_and_notify(self):
        """Check and announce reminders."""
        reminders = self.get_upcoming_reminders()
        for medicine in reminders:
            text = f"Time to take your medicine! {medicine}."
            print(f"🔔 Announcing: {text}")
            file = self.generate_speech(text)
            if file:
                self.play_audio(file)

if __name__ == "__main__":
    notifier = ReminderNotifier()
    while True:
        notifier.check_and_notify()
        time.sleep(60)
