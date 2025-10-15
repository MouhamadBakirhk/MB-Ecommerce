from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
from difflib import get_close_matches

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").strip()

    reply = None

    # --- 1️⃣ جلب الأسئلة من DB Laravel ---
    try:
        response_db = requests.get("http://127.0.0.1:8000/api/chat").json()
        questions = [m['question'] for m in response_db]
        answers = [m['answer'] for m in response_db]

        # fuzzy match
        matches = get_close_matches(user_message, questions, n=1, cutoff=0.6)
        if matches:
            idx = questions.index(matches[0])
            reply = answers[idx]
    except Exception as e:
        print("Error fetching chat from Laravel:", e)

    # --- 2️⃣ إذا ما في جواب قريب، نسأل AI ---
    if not reply:
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meituan/longcat-flash-chat:free",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant who replies naturally in Arabic or English."},
                    {"role": "user", "content": user_message}
                ]
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers, json=payload
            )
            response_json = response.json()
            print("OpenRouter Response:", response_json)

            if "choices" in response_json and len(response_json["choices"]) > 0:
                choice = response_json["choices"][0]
                reply = choice.get("message", {}).get("content") or choice.get("text", "No reply")
            elif "error" in response_json:
                reply = response_json["error"].get("message", "Error occurred")
        except Exception as e:
            reply = f"Error connecting to AI: {str(e)}"

        # --- 3️⃣ خزّن السؤال والجواب الجديد في DB Laravel ---
        try:
            requests.post("http://127.0.0.1:8000/api/chat", json={
                "question": user_message,
                "answer": reply
            })
        except Exception as e:
            print("Error saving chat to Laravel:", e)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
