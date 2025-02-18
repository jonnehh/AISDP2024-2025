from flask import Flask, request, jsonify
import requests
import os
import json
app = Flask(__name__)

# OpenAI API Key (建议使用环境变量管理)
OPENAI_API_KEY = "API_KEY"

def transcribe(audio_file):
    """处理音频文件并调用 Whisper API 进行转录"""
    try:
        files = {"file": (audio_file.filename, audio_file, "audio/wav")}
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        data = {"model": "whisper-1"}
        
        response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files, data=data)
        response_json = response.json()
        
        return response_json.get("text", "Failed to transcribe")
    except Exception as e:
        return str(e)

def llm_reply(message,ocr_result=None):

    
    prompt = f"""

    ### Instructions ###
    1. **Extract the following fields (if applicable):**
    - **medicine_name**: The name of the medicine.
    - **dosage_time**: The specified time to take the medicine (only for reminders).
    - **function**: The purpose of the medicine (only for function queries).

    2. **Normalize extracted values:**
    - Convert **time expressions** into `HH:MM` format (`8pm` → `20:00`).
    - If the **medicine name is missing**, return `"unknown"`.

    3. **Return the output in JSON format** with the extracted data.

    ### **Examples** ###
    ####  Example 1: Medication Reminder ####
    **User Input**: "This is Metformin . Metformin's primary function is to lower blood sugar levels, treat type 2 diabetes, and improve insulin sensitivity.I need to take this medicine at 8pm"  
    
    **Output**:
        Extract the relevant details and return them as a valid JSON object. Do not include any markdown formatting, code blocks, or triple backticks. Only return the raw JSON output.
    ```json
    ｛
    "medicine_name": "metformin",
    "function": "lower blood sugar levels, treat type 2 diabetes, and improve insulin sensitivity.",
    "dosage_time": "20:00"
    ｝
  
    user input:
    {ocr_result} 
    {message} 
        """
    
    print(prompt)
    url = "https://api.openai.com/v1/chat/completions"
    api_key ="API_KEY"
    headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    data = {
            "model": "gpt-4o",
            "temperature": 0.7,
            "messages": [
                {
                    "role": "system",
                    "content": prompt ,
                }

            ],
            "max_tokens": 200
        }

    response = requests.post(url, headers=headers, json=data)
    print(response)
    answer=response.json()['choices'][0]['message']['content']
# except:
#     answer="I apologize for the confusion. If you have any questions about mosquitoes or need information related to them, please feel free to ask. I'm here to help!"
    print("✅ dataNlp System Initialized Successfully!")

    return answer  


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """Process API request and return transcription result"""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    
    # Retrieve the message sent from `/upload`
    message = request.form.get("message", "")

    # Transcribe audio
    transcription = transcribe(audio_file)
    print(transcription)

    if not transcription:
        return jsonify({"error": "Empty transcription"}), 400

    # Pass transcription and message to LLM
    json_message = llm_reply(transcription, message)
    data=json.loads(json_message)
    medicine_name = data.get("medicine_name")
    dosage_time = data.get("dosage_time")
    url = "http://flask-data-server.my-app:6050/add_medicine" 
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    return jsonify({"transcription": json_message, "message": message})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)