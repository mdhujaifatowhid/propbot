import os
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq

app = Flask(__name__, static_folder=".")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """You are PropBot, an expert real estate AI assistant with deep knowledge of global property markets.

You help users with:
- Buying, selling, and renting properties
- Property valuation and market analysis
- Investment advice and ROI calculations
- Legal processes, documentation, and due diligence
- Mortgage, financing, and loan guidance
- Neighborhood comparisons and location insights

Personality:
- Professional yet warm and approachable
- Give specific, actionable advice
- Use relevant emojis to make responses engaging
- Ask clarifying questions about budget and requirements when helpful
- If you don't know something specific, be honest and suggest consulting a local agent

Always end responses by asking how you can help further."""


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY not configured on server."}), 500

    data = request.json
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided."}), 400

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        max_tokens=1024,
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
