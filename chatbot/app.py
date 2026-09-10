import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv
import chatbot_config

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=chatbot_config.SYSTEM_INSTRUCTION,
                temperature=0.3
            )
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"}, 500)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
