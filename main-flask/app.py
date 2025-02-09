from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# 读取 OCR 和 RAG 微服务地址
OCR_SERVICE_URL = os.environ.get("OCR_SERVICE_URL", "http://127.0.0.1:5000/ocr")
RAG_SERVICE_URL = os.environ.get("RAG_SERVICE_URL", "http://127.0.0.1:5050/massage")

@app.route('/')
def index():
    """返回前端 HTML 页面"""
    return render_template('ocr.html')

@app.route('/capture', methods=['POST'])
def capture():
    """
    接收前端上传的图片（Base64 编码），将图片数据转发到 OCR 微服务，
    然后将 OCR 识别结果发送到 RAG 进行处理，最后返回完整的结果。
    """
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

if __name__ == '__main__':
    # 运行 Flask 服务，监听 888 端口
    app.run(host='0.0.0.0', port=888, debug=True)
