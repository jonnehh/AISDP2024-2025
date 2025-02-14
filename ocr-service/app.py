from flask import Flask, request, jsonify, render_template
from ocr_module import process_image

import os
os.environ['FLAGS_enable_ir_optim'] = 'false'


# 初始化 Flask 应用
app = Flask(__name__)


@app.route('/ocr', methods=['POST'])
def capture():
    """处理上传图片并返回 OCR 和 RAG 结果"""
    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image received"}), 400

    # 调用 OCR 模块
    text_results = process_image(data)

    # 调用 RAG 模块检索相关信息
    user_message = " ".join(text_results)


    print("User Message:", user_message)

    return jsonify({"status": "success", "data":  user_message}), 200, {"Content-Type": "application/json"}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
