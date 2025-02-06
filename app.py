import os
import json
from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load class messages from JSON file
def load_class_messages(file_path="class_messages.json"):
    with open(file_path, "r") as file:
        return json.load(file)

class_messages = load_class_messages()

# Load the YOLO model
model = YOLO("C:/Users/divin/OneDrive/Desktop/Y3S2_projects/AISDP/Code/model_results/train/weights/best.pt")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        # Save uploaded file
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Run YOLO inference
        results = model.predict(source=image_path, imgsz=640, conf=0.6)
        class_names = model.names  # Mapping of class IDs to names

        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])  
                confidence = float(box.conf[0])  

                class_name = class_names[class_id]
                message = class_messages.get(class_name, f"Detected: {class_name} with {confidence:.2f} confidence.")

                detections.append({"class": class_name, "confidence": confidence, "message": message})

        return render_template("results.html", image_path=image_path, detections=detections)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
