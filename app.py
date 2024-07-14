from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load the labs data from the JSON file
with open('assets/labs.json') as f:
    labs = json.load(f)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello, World!"})

@app.route('/labs', methods=['GET'])
def get_labs():
    return jsonify(labs)

@app.route('/labs/<string:lab_id>', methods=['GET'])
def get_lab_by_id(lab_id):
    lab = next((lab for lab in labs if lab["id"] == lab_id), None)
    if lab:
        return jsonify(lab)
    else:
        return jsonify({"error": "Lab not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
