from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace this with your actual Hugging Face API key
HF_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Function to get response from Hugging Face model
def generate_response(message):
    payload = {"inputs": message}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        data = response.json()
        return data[0]["generated_text"] if isinstance(data, list) else "Sorry, I couldn't understand that."
    except Exception as e:
        return f"Error: {str(e)}"

# Route to serve the HTML page
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle chat messages
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    reply = generate_response(user_input)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)