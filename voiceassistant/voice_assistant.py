import openai
import psycopg2
import requests
import pyaudio
import wave
import re
import os
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

# Load API Keys securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_CONFIG = {
    "dbname": "reminders_db",
    "user": "postgres",
    "password": os.getenv("POSTGRES_PASSWORD"),  # Store it securely
    "host": "localhost",
    "port": "5432"
}

class VoiceAssistant:
    def __init__(self):
        self.audio_filename = "recorded_audio.wav"

    def record_audio(self, duration=5):
        """Records audio from the microphone and saves it as a WAV file."""
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("🎤 Recording... Speak now!")

        frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * duration))]

        print("✅ Recording finished!")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.audio_filename, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

    def transcribe_audio(self):
        """Sends recorded audio to OpenAI Whisper API for transcription."""
        try:
            with open(self.audio_filename, "rb") as audio_file:
                headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
                files = {"file": (self.audio_filename, audio_file, "audio/wav")}
                data = {"model": "whisper-1"}
                response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files, data=data)
                return response.json().get("text", "Error in transcription")
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I couldn't process that."

    def extract_reminder_details(self, text):
        """Extracts time and medicine name from a transcribed command."""
        try:
            time_match = re.search(r"(\d{1,2}[:\.]?\d{0,2}\s?(?:AM|PM|am|pm)?)", text)
            if time_match:
                time = time_match.group(1).replace(".", ":").upper().strip()
                parsed_time = parser.parse(time, fuzzy=True).strftime('%H:%M:%S')
                match = re.search(r"(?i)(?:remind me to take|set a reminder(?: at)?)\s+(.+?)\s+(?:at|for)\s+", text)
                if match:
                    return {"time": parsed_time, "medicine": match.group(1).strip()}
        except Exception as e:
            print(f"❌ Error parsing time: {e}")
        return None

    def save_reminder_to_db(self, medicine, time):
        """Stores the extracted reminder details in PostgreSQL."""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reminders (medicine, reminder_time) VALUES (%s, %s)", (medicine, time))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Reminder saved: {medicine} at {time}")
        except Exception as e:
            print(f"❌ Error saving to DB: {e}")

    def listen_and_process(self):
        """Records, transcribes, extracts details, and stores the reminder."""
        self.record_audio(duration=5)
        transcribed_text = self.transcribe_audio()
        print(f"📝 Transcribed: {transcribed_text}")

        details = self.extract_reminder_details(transcribed_text)
        if details:
            print(f"✅ Extracted Reminder: {details}")
            self.save_reminder_to_db(details["medicine"], details["time"])
        else:
            print("❌ Could not understand the command.")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.listen_and_process()
