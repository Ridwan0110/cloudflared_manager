from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

# Load data or initialize
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# POST /update: Receives tunnel URL
@app.route('/update_url', methods=['POST'])
def update_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request"}), 400

    current_data = load_data()
    current_data["url"] = data["url"]
    save_data(current_data)

    return jsonify({"message": "URL updated successfully"}), 200

# GET /current: Returns latest URL
@app.route('/get_url', methods=['GET'])
def get_url():
    current_data = load_data()
    return jsonify(current_data)

# Optional root endpoint
@app.route('/')
def index():
    return "Cloudflared Manager Server is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
