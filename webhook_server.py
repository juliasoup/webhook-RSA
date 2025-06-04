# webhook_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(f"[WEBHOOK RECEBIDO]: {data}")
    return jsonify({"status": "recebido"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
