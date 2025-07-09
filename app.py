import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv

# ── Load environment variables ───────────────────────────
load_dotenv()

# ── Flask setup ─────────────────────────────────────────
#   static_folder="static", static_url_path="" makes
#   Flask serve / → static/index.html automatically
app = Flask(__name__, static_folder="static", static_url_path="")

# ── MongoDB setup ───────────────────────────────────────
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db_name = mongo_uri.rsplit("/", 1)[-1].split("?", 1)[0]
db = client[db_name]
events = db.events

# ── Serve your SPA at / ─────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

# ── Health check at /health ─────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200

# ── Webhook receiver ────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def webhook():
    print("── Incoming Webhook ────────────────────")
    print("Headers:", json.dumps(dict(request.headers), indent=2))
    print("Body:", request.data.decode("utf-8")[:500], "...")
    event = request.headers.get("X-GitHub-Event", "")
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        print("❌ JSON parse error:", e)
        return jsonify({"msg": "Bad JSON"}), 400

    if event not in ("push", "pull_request", "ping"):
        return jsonify({"msg": f"Ignored event '{event}'"}), 200
    if event == "ping":
        return jsonify({"msg": "pong"}), 200

    author = payload.get("sender", {}).get("login", "unknown")
    doc = {
        "type":      event,
        "author":    author,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if event == "push":
        doc["to_branch"] = payload.get("ref", "").split("/")[-1]
    else:
        pr     = payload["pull_request"]
        action = payload.get("action", "")
        doc.update({
            "from_branch": pr["head"]["ref"],
            "to_branch":   pr["base"]["ref"],
            "action":      "merged" if action=="closed" and pr.get("merged") else action
        })

    events.insert_one(doc)
    print("✅ Stored:", doc)
    return jsonify({"msg": "Event stored"}), 201

# ── Fetch latest events ──────────────────────────────────
@app.route("/events", methods=["GET"])
def get_events():
    docs = list(events.find().sort("timestamp", -1).limit(10))
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs), 200

# ── Run Server ──────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
