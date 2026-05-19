"""Net Worth Dashboard — local Flask server v1.0.0

Run:  python server.py
Open: http://127.0.0.1:5001
"""

import json
import os
import sys
from flask import Flask, abort, jsonify, request, send_from_directory

VERSION = "1.0.3"

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "networth.json")

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))


# ── Static / frontend ────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


# ── Data API (all requests stay on localhost) ────────────────────────────────

@app.route("/api/data", methods=["GET"])
def get_data():
    if not os.path.exists(DATA_FILE):
        abort(404, description="No data file found. Use the Import button to load networth.json.")
    with open(DATA_FILE, "r") as f:
        return jsonify(json.load(f))


@app.route("/api/data", methods=["POST"])
def post_data():
    data = request.get_json(force=True, silent=True)
    if not data or "months" not in data or "assets" not in data:
        abort(400, description="Invalid payload — expected {months, assets, home, liabilities}.")
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"ok": True, "months": len(data["months"])})


@app.route("/api/export")
def export_data():
    if not os.path.exists(DATA_FILE):
        abort(404, description="No data to export.")
    with open(DATA_FILE, "r") as f:
        content = f.read()
    return app.response_class(
        response=content,
        status=200,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=networth.json"},
    )


# ── Error handlers ────────────────────────────────────────────────────────────

@app.errorhandler(400)
@app.errorhandler(404)
def http_error(e):
    return jsonify({"error": str(e.description)}), e.code


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"Net Worth Dashboard v{VERSION}")
    print(f"Open http://127.0.0.1:{port} in your browser")
    print("Press Ctrl-C to stop\n")
    app.run(host="127.0.0.1", port=port, debug=False)
