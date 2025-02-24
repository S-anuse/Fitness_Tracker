from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("firebase-adminsdk.json")  # Ensure this file exists
firebase_admin.initialize_app(cred)
db = firestore.client()

# Home Route (✅ Move this above if __name__ == "__main__")
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

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
