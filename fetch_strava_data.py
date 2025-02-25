import os
import requests
import json

# Load the access token from the saved JSON file
def get_access_token():
    try:
        with open("access_token.json", "r") as token_file:
            token_data = json.load(token_file)
            return token_data.get("access_token")
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Fetch fitness data from Strava
def get_activity_data():
    access_token = get_access_token()
    if not access_token:
        return {"error": "Access token not available. Please authenticate first."}

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch activities", "details": response.json()}

    return response.json()
