from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import json
from dotenv import load_dotenv
import os
load_dotenv() 

app = Flask(__name__)
CORS(app)

# Load the labs data from the JSON file
with open('assets/labs.json') as f:
    labs = json.load(f)

# Define a list of valid API keys
VALID_API_KEYS = {os.getenv("VALID_API_KEY")}

def check_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key not in VALID_API_KEYS:
         abort(403, description="Invalid API key")
    

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello, World!"})

@app.route('/labs', methods=['GET'])
def get_labs():
    check_api_key()
    return jsonify(labs)

@app.route('/labs/<string:lab_id>', methods=['GET'])
def get_lab_by_id(lab_id):
    check_api_key()
    lab = next((lab for lab in labs if lab["id"] == lab_id), None)
    if lab:
        return jsonify(lab)
    else:
        return jsonify({"error": "Lab not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
