from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="static", static_url_path="")

API_KEY = os.environ.get("API_KEY")  # Use environment variable for security
MODEL = "models/gemini-2.0-flash"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent"

# Serve the frontend index.html at root URL
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Serve other static files (JS, CSS, images) automatically through static_url_path=""

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"answer": "Please provide a prompt."})

    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": API_KEY
    }
    json_data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(ENDPOINT, headers=headers, params=params, json=json_data)
    if response.status_code == 200:
        resp_json = response.json()
        answer = resp_json['candidates'][0]['content']['parts'][0]['text']
        answer = answer.replace("Gemini", "SrujanAI")
        return jsonify({"answer": answer})
    else:
        return jsonify({"answer": "Error from AI service: " + response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
