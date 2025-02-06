from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pyttsx3  # For text-to-speech notifications

app = Flask(__name__)

# In-memory storage for reminders
reminders = []

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Function to speak notifications
def notify_user(message):
    print(f"🔔 {message}")
    tts_engine.say(message)
    tts_engine.runAndWait()

# Function to check reminders
def check_reminders():
    now = datetime.now().strftime("%H:%M")
    for reminder in reminders:
        if reminder["time"] == now and not reminder.get("notified"):
            notify_user(f"It's time to take {reminder['medicine']}!")
            reminder["notified"] = True  # Mark reminder as notified

# Schedule the reminder checker to run every minute
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_reminders, trigger="interval", seconds=60)
scheduler.start()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Digital Assistant"}), 200

@app.route("/add_reminder", methods=["POST"])
def add_reminder():
    time = request.args.get("time")
    medicine = request.args.get("medicine")
    if not time or not medicine:
        return jsonify({"error": "Time and medicine are required"}), 400

    # Add the reminder
    reminders.append({"time": time, "medicine": medicine, "notified": False})
    return jsonify({"status": "success", "message": f"Reminder set for {medicine} at {time}"}), 200

@app.route("/get_reminders", methods=["GET"])
def get_reminders():
    return jsonify({"reminders": reminders}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
