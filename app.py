from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are "PropBot", a smart and professional AI assistant for a real estate agency.

YOUR ROLE:
- Help clients find, buy, sell, and rent properties
- Answer questions about property prices, locations, and market trends
- Guide clients through the buying/selling process
- Explain legal steps, documentation, and due diligence
- Assist with mortgage, financing, and loan questions
- Provide investment advice and ROI calculations

PERSONALITY:
- Professional yet warm and approachable
- Speak English or match the language the client uses
- Use emojis occasionally but keep it minimal
- Be concise and helpful — no fluff
- If you don't know something specific, honestly say so and suggest consulting a local agent

WHEN HELPING WITH PROPERTY SEARCH:
- Ask about budget, preferred location, property type, and size
- Give realistic market insight
- Mention key things to check before buying (title deed, survey, encumbrances etc.)

Always end by asking how you can help further."""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    history = data.get("history", [])

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Something went wrong. Please try again.", "error": str(e)}), 500

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
