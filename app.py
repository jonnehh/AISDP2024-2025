from flask import Flask, request, jsonify
from ultralytics import YOLO
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load class messages from JSON file
def load_class_messages(file_path="class_messages.json"):
    with open(file_path, "r") as file:
        return json.load(file)

class_messages = load_class_messages()

# Load the YOLO model
model = YOLO("best.pt")

@app.route("/food_detection", methods=["POST"])
def detect_food():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    results = model.predict(source=image_path, imgsz=640, conf=0.6)
    class_names = model.names

    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = class_names[class_id]
            message = class_messages.get(class_name, f"Detected: {class_name} with {confidence:.2f} confidence.")
            detections.append({"class": class_name, "confidence": confidence, "message": message})

    return jsonify(detections), 200, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)