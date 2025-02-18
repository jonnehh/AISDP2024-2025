from flask import Flask, request, jsonify, render_template
import requests
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

# 读取 OCR 和 RAG 微服务地址
OCR_SERVICE_URL = "http://ocr-service-svc.my-app:5000/ocr"

RAG_SERVICE_URL = "http://rag-service-svc.my-app:5050/massage"

FLASK_SERVER_URL = "http://food-service-svc.my-app:5080/detect_food"

Speech2json_URL = "http://voice2text-service-svc.my-app:6000/transcribe"

ADD_MEDICINE_URL = "http://flask-data-server.my-app:6050/add_medicine" 

get_data_url = "http://flask-data-server.my-app:6050/medicines"

delete_data_url="http://flask-data-server.my-app:6050/delete_medicine/"

medicine_info= None

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 确保目录存在
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/medicines')
def get_medicines():
    response = requests.get(get_data_url)
    medicines = response.json()
    return jsonify(medicines)

@app.route('/delete', methods=['GET'])
def delete_medicines():
    # 从前端获取要删除的药品名称
    medicine_name = request.args.get('name')
    if not medicine_name:
        return jsonify({"message": "No medicine name provided"}), 400
    
    # 拼接删除的完整 URL，请注意对名称进行 URL 编码
    url = delete_data_url + requests.utils.quote(medicine_name)
    try:
        del_response = requests.delete(url)
        if del_response.ok:
            return jsonify({"message": f"Deleted {medicine_name} successfully"})
        else:
            return jsonify({"message": "Deletion failed", "detail": del_response.text}), 500
    except Exception as e:
        return jsonify({"message": f"Deletion error: {str(e)}"}), 500

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/pill_sense')
def pill_sense():
    return render_template('pill_sense.html')

@app.route('/nutri_scan')
def nutri_scan():
    return render_template('nutri_scan.html')

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["audio"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
    file.save(filepath)

    # Message to be sent (medicine function)
    message = medicine_info

    # Send to Whisper API with message
    with open(filepath, "rb") as audio_file:
        response = requests.post(Speech2json_URL, files={"file": audio_file}, data={"message": message})
    
    response="Save successfully！ Information："
    print(response)

    return response.json()



@app.route('/capture', methods=['POST'])
def capture():
    """
    接收前端上传的图片（Base64 编码），将图片数据转发到 OCR 微服务，
    然后将 OCR 识别结果发送到 RAG 进行处理，最后返回完整的结果。
    """
    global medicine_info
    medicine_info=None
    try:
        # 获取前端上传的图片
        data = request.json.get("image")
        if not data:
            return jsonify({"error": "No image received"}), 400

        # 1️⃣ 调用 OCR 微服务
        ocr_response = requests.post(OCR_SERVICE_URL, json={"image": data}, timeout=10)
        
        if ocr_response.status_code != 200:
            return jsonify({"error": "OCR service error"}), 500
        
        ocr_data = ocr_response.json()
        ocr_text = ocr_data.get("data", "")

        # 确保 OCR 结果有效
        if not ocr_text:
            return jsonify({"error": "OCR did not return any text"}), 400
        
        print("OCR Result:", ocr_text)

        # 2️⃣ 调用 RAG 微服务，传递 OCR 结果
        rag_response = requests.post(RAG_SERVICE_URL, json={"massage": ocr_text}, timeout=10)

        if rag_response.status_code != 200:
            return jsonify({"error": "RAG service error"}), 500

        rag_data = rag_response.json()
        rag_result = rag_data.get("data", "")

        print("RAG Result:", rag_result)
        medicine_info=rag_result
        # 3️⃣ 返回 OCR 和 RAG 结果
        return jsonify({
            "status": "success",
            "ocr_result": ocr_text,
            "rag_result": rag_result,
            "name":  rag_result.split()[0] if rag_result else "N/A"  # 可能的药品名称
        })

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Service request failed: {e}")
        return jsonify({"error": "Service request failed"}), 500

@app.route('/detect_food', methods=['POST'])
def detect_food():
    """调用另一个 Flask 服务器的 API 进行食物识别"""
    try:
        data = request.get_json()
        image_data = data.get("image")
        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        # 发送请求到另一个 Flask 服务器
        headers = {"Content-Type": "application/json"}
        response = requests.post(FLASK_SERVER_URL, json={"image": image_data}, headers=headers)
        
        if response.status_code == 200:
            print(response.json())
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to get response from food detection API", "status": response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    # 运行 Flask 服务，监听 888 端口
    app.run(host='0.0.0.0', port=888, debug=True)
