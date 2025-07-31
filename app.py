from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load environment variables from .env (optional but recommended)
load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HF_TOKEN")  # Or hardcode for now, but .env is safer

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_huggingface(prompt):
    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct:novita",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return f"⚠️ HuggingFace Error: {data.get('error', 'No details')}"
    except Exception as e:
        return f"❌ Internal Error: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400

    response = query_huggingface(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
