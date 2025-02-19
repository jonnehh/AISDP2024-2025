from flask import Flask, request, jsonify, render_template
from rag_module import RAGProcessor

app = Flask(__name__)

rag = RAGProcessor()


@app.route('/massage', methods=['POST'])
def capture():
    text_results = request.json.get("massage")
    if not text_results:
        return jsonify({"error": "No massage received"}), 400
    
    answer=rag.llm_reply(text_results)

    return jsonify({"status": "success", "data":  answer}), 200, {"Content-Type": "application/json"}


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
