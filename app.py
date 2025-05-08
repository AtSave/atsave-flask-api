from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

@app.route("/query-logs", methods=["GET"])
def query_logs():
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/device_logs?order=timestamp.desc&limit=20"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify({"error": response.text}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)