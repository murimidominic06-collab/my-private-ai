from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ===== Weka KEYS zako hapa =====
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_GEMINI_KEY_HAPA")
MY_PRIVATE_API_KEY = os.environ.get("MY_API_KEY", "nairobi-ai-2024-secret-xyz")
# =================================

def jibu_kila_kitu(swali):
    if "PASTE_YOUR" in GEMINI_API_KEY or len(GEMINI_API_KEY) < 10:
        return "⚠️ Bado hujaweka GEMINI_API_KEY. Nenda https://aistudio.google.com/app/apikey"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": swali}]}],
        "systemInstruction": {"parts": [{"text": "You are Programming and CodeWriting AI from Nairobi. You are a super expert in coding, business, studies, writing. Answer in Swahili/English clearly. If asked illegal stuff, politely refuse and teach legal alternative."}]}
    }
    try:
        r = requests.post(url, json=payload, timeout=60)
        data = r.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {e} | Response: {r.text if 'r' in locals() else 'no response'}"

@app.route("/", methods=["GET", "POST"])
def home():
    jibu = ""
    if request.method == "POST":
        swali = request.form.get("swali", "")
        if swali:
            jibu = jibu_kila_kitu(swali)

    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="UTF-8"><title>Programming and CodeWriting AI</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
    body{{background:#0f0f0f;color:#fff;font-family:sans-serif;padding:15px}}
   .box{{max-width:750px;margin:auto;background:#1e1e1e;padding:25px;border-radius:15px}}
    textarea{{width:100%;height:110px;border-radius:10px;padding:12px;background:#2a2a2a;color:white;border:1px solid #444;box-sizing:border-box}}
    button{{background:#4285f4;color:white;padding:12px 25px;border:none;border-radius:10px;margin-top:10px;font-weight:bold;cursor:pointer;width:100%}}
   .jibu{{background:#000;padding:18px;border-radius:10px;margin-top:18px;white-space:pre-wrap;border-left:4px solid #4285f4;min-height:50px}}
    code{{background:#000;padding:10px;display:block;border-radius:8px;margin-top:10px;word-break:break-all}}
    </style></head>
    <body>
    <div class="box">
    <h1 style="text-align:center;color:#4285f4">🤖 Programming and CodeWriting AI</h1>
    <p style="text-align:center;opacity:0.7">Engine yako inajua kila kitu LEGAL!</p>
    <form method="POST"><textarea name="swali" placeholder="Uliza chochote... ex: Andika code ya calculator ya Python"></textarea><button type="submit">Uliza AI Yangu 🚀</button></form>
    <div class="jibu">{jibu if jibu else "Jibu litaonekana hapa..."}</div>
    <hr style="margin:25px 0;opacity:0.2">
    <h3>🔐 Private API yako kama Gemini:</h3>
    <code>
    URL: /api/chat<br>
    METHOD: POST<br>
    HEADER: x-api-key: {MY_PRIVATE_API_KEY}<br>
    BODY: {{"message": "swali lako"}}
    </code>
    </div></body></html>
    """

@app.route("/api/chat", methods=["POST"])
def private_api():
    user_key = request.headers.get("x-api-key")
    if user_key!= MY_PRIVATE_API_KEY:
        return jsonify({"error": "Unauthorized! Tumia x-api-key sahihi.", "hint": "Header: x-api-key: YOUR_KEY"}), 401

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Tuma JSON: {'message': 'swali lako'}"}), 400

    msg = data.get("message")
    answer = jibu_kila_kitu(msg)
    return jsonify({
        "status": "success",
        "model": "Programming and CodeWriting AI - Private",
        "question": msg,
        "answer": answer
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)