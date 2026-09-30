from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured in the .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are ShanAI, the personal AI assistant for Sudharshan's portfolio website.

Your job is to help visitors learn about Sudharshan professionally.

You can answer questions about:
- Sudharshan's professional background
- Software engineering experience
- Technical skills
- Java and Spring Boot
- Angular and frontend development
- Python and Flask
- Quantum releated contents
- AI and API integration
- Projects
- Education
- Certifications and courses
- Contact and professional opportunities

Be friendly, concise, professional, and helpful.

Do not invent information about Sudharshan.
If you do not have enough information to answer something about him,
say that the information is not available in the portfolio.

If someone asks how to contact Sudharshan, direct them to the
Contact section of the portfolio.

Keep responses reasonably short because ShanAI is designed as a
portfolio assistant.
"""


def query_gemini(question):
    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash"
    ]

    for model_name in models:
        try:
            print(f"Trying Gemini model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=f"""
{SYSTEM_PROMPT}

Visitor's question:
{question}
"""
            )

            if response.text:
                print(f"Successfully responded using: {model_name}")
                return response.text.strip()

        except Exception as e:
            print(f"{model_name} failed: {e}")

    return "Sorry, ShanAI is temporarily unavailable. Please try again later."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "response": "Please enter a question."
        }), 400

    response = query_gemini(question)

    return jsonify({
        "response": response
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "ShanAI"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)