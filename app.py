from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = generate_password_hash(data.get("password"))
    company = data.get("company_name", "")
    payload = {
        "email": email,
        "password": password,
        "company_name": company
    }
    resp = requests.post(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS, json=payload)
    if resp.status_code in (200, 201):
        return jsonify({"status": "registered"}), 201
    return jsonify({"error": resp.text}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    query_url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}"
    resp = requests.get(query_url, headers=HEADERS)
    if resp.status_code != 200 or not resp.json():
        return jsonify({"error": "user not found"}), 404
    user = resp.json()[0]
    if not check_password_hash(user["password"], password):
        return jsonify({"error": "invalid password"}), 403
    return jsonify({
        "message": "login success",
        "user_id": user["id"],
        "company": user["company_name"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)