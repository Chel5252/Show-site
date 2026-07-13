from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_ADMIN = os.environ.get("TG_ADMIN")

@app.route("/send", methods=["POST", "OPTIONS"])
def send():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})
    d = request.json
    text = (
        f"🔔 НОВАЯ ЗАЯВКА С САЙТА!\n\n"
        f"👤 Имя: {d['name']}\n"
        f"📞 Телефон: {d['phone']}\n"
        f"💅 Услуга: {d['service']}\n"
        f"🕐 Время: {d['datetime']}"
    )
    requests.get(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        params={"chat_id": TG_ADMIN, "text": text}
    )
    return jsonify({"ok": True})

# ---------- ОТДАЧА MINI APP ----------
@app.route("/app")
def mini_app():
    return render_template("app.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
