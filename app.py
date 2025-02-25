from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import firebase_admin
from fetch_strava_data import get_activity_data 
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

# Get credentials path
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set in the environment variables")

# Initialize Firebase
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Flask app
app = Flask(__name__)



@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Fitness Tracker API!"})

# Add User Route
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    user_ref = db.collection("users").document(data["email"])
    user_ref.set(data)
    return jsonify({"message": "User added successfully!"})

# Get Users Route
@app.route("/get_users", methods=["GET"])
def get_users():
    users = db.collection("users").stream()
    user_list = [{user.id: user.to_dict()} for user in users]
    return jsonify(user_list)



# Fetch fitness data from Strava
@app.route("/get_fitness_data", methods=["GET"])
def get_fitness_data():
    data = get_activity_data()
    return jsonify(data)



# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
