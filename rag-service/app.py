from flask import Flask, request, jsonify, render_template
from rag_module import RAGProcessor

# 初始化 Flask 应用
app = Flask(__name__)

# 初始化 RAG 模块
rag = RAGProcessor()


@app.route('/massage', methods=['POST'])
def capture():
    """处理上传图片并返回 OCR 和 RAG 结果"""
    text_results = request.json.get("massage")
    if not text_results:
        return jsonify({"error": "No massage received"}), 400
    
    answer=rag.llm_reply(text_results)
    
    # 返回 OCR 和 RAG 的结果给前端
    return jsonify({"status": "success", "data":  answer}), 200, {"Content-Type": "application/json"}


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
