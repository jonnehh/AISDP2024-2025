from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
import json
import base64

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 加载类别信息
def load_class_messages(file_path="class_messages.json"):
    with open(file_path, "r") as file:
        return json.load(file)

class_messages = load_class_messages()

# 加载 YOLO 模型
model = YOLO("best.pt")


@app.route("/detect_food", methods=["POST"])
def detect_food():
    data = request.json
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "No image data received"}), 400

    # 将 Base64 数据转换为图片文件
    image_data = image_data.split(",")[1]  # 去掉开头的 "data:image/jpeg;base64,"
    image_bytes = base64.b64decode(image_data)
    image_path = os.path.join(UPLOAD_FOLDER, "captured.jpg")

    with open(image_path, "wb") as file:
        file.write(image_bytes)

    # 运行 YOLO 进行检测
    results = model.predict(source=image_path, imgsz=640, conf=0.6)
    class_names = model.names

    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = class_names[class_id]
            message = class_messages.get(class_name, {"message": f"Detected: {class_name} with {confidence:.2f} confidence."})

            detections.append({
                "class": class_name,
                "confidence": confidence,
                "message": message
            })

    return jsonify(detections), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080, debug=True)
