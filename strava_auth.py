import os
import requests
from flask import Flask, request, redirect, jsonify

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Fitness Tracker Website!"

@app.route("/login")
def login():
    strava_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=activity:read_all"
    return redirect(strava_url)

@app.route("/exchange_token")
def exchange_token():
    code = request.args.get("code")
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=payload)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
