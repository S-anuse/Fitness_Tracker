import os
import requests
from flask import Flask, request, redirect, jsonify

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__)

ACCESS_TOKEN = None

@app.route("/")
def home():
    return "Welcome to the Fitness Tracker Website!"

@app.route("/login")
def login():
    strava_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=activity:read_all"
    return redirect(strava_url)

@app.route("/exchange_token")
def exchange_token():
    global ACCESS_TOKEN  # Update the global variable
    code = request.args.get("code")
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=payload)
    token_data = response.json()
    ACCESS_TOKEN = token_data.get("access_token")
    return jsonify(response.json())

@app.route("/get_activities")
def get_activities():
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        return jsonify({"error": "Access token not available. Please authenticate first."}), 401

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch activities", "details": response.json()}), response.status_code

    return jsonify(response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

