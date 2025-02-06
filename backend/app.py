from flask import Flask, render_template, redirect, url_for, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from voice_assistant import VoiceAssistant
import threading

app = Flask(__name__)
reminders = []
voice_assistant = VoiceAssistant()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Run voice assistant in a separate thread
        def run_voice_assistant():
            command = voice_assistant.listen()
            if command:
                voice_assistant.handle_command(command)
        
        threading.Thread(target=run_voice_assistant).start()
    return render_template("index.html")


@app.route("/add_reminder", methods=["POST"])
def add_reminder():
    time = request.form.get("time")
    medicine = request.form.get("medicine")
    if time and medicine:
        reminders.append({"time": time, "medicine": medicine, "notified": False})
        return redirect(url_for("home"))
    return jsonify({"error": "Invalid input"}), 400

@app.route("/reminders", methods=["GET"])
def show_reminders():
    return jsonify(reminders)

@app.route("/delete_reminders", methods=["DELETE"])
def delete_reminders():
    reminders.clear()
    return jsonify({"message": "All reminders deleted."})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, threaded=False)

