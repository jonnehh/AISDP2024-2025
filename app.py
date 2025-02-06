from flask import Flask, request, jsonify, render_template
from rag_module import RAGProcessor
from ocr_module import process_image




# 初始化 Flask 应用
app = Flask(__name__)

# 初始化 RAG 模块
rag = RAGProcessor("processed_text.json")

@app.route('/')
def index():
    """返回前端 HTML 页面"""
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    """处理上传图片并返回 OCR 和 RAG 结果"""
    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image received"}), 400

    # 调用 OCR 模块
    text_results = process_image(data)

    # 调用 RAG 模块检索相关信息
    user_message = " ".join(text_results)
    response = rag.retrieve_context(user_message)

    # 打印日志
    print("User Message:", user_message)
    print("RAG Response:", response)
    answer=rag.llm_reply(user_message,response)
    # 返回 OCR 和 RAG 的结果给前端
    return jsonify({"ocr_result": text_results, "rag_result":answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
