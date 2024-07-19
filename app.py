from flask import Flask, abort, request, jsonify, render_template
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv() 

app = Flask(__name__)
CORS(app)

database = os.getenv("MONGODB_DB")
collection = os.getenv("MONGODB_COLLECTION")


# Replace the following with your MongoDB connection string
# For local MongoDB use: client = MongoClient('mongodb://localhost:27017/')
# For MongoDB Atlas use your connection string, e.g.,
# client = MongoClient('your_atlas_connection_string')

# Create a new client and connect to the server
client = MongoClient(os.getenv("MONGODB_SRV"), server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client[database]
collection = db[collection]

# Define a list of valid API keys
VALID_API_KEYS = {os.getenv("VALID_API_KEY")}

def check_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key not in VALID_API_KEYS:
        abort(403, description="Invalid API key")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'inserted_id': str(result.inserted_id)})

@app.route('/update', methods=['PUT'])
def update_record():
    data = request.json
    result = collection.update_one({'id': data['id']}, {'$set': data})
    return jsonify({'updated_count': result.modified_count})

@app.route('/delete', methods=['DELETE'])
def delete_record():
    data = request.json
    result = collection.delete_one({'id': data['id']})
    return jsonify({'deleted_count': result.deleted_count})

@app.route('/search', methods=['GET'])
def search_records():
    query = request.args.get('query')
    records = list(collection.find({'$text': {'$search': query}}, {'_id': 0}))
    return jsonify(records)

@app.route('/records', methods=['GET'])
def get_records():
    records = list(collection.find({}, {'_id': 0}))
    return jsonify(records)

#PAGINATION
@app.route('/labs', methods=['GET'])
def get_labs():
    check_api_key()
    records = list(collection.find({}, {'_id': 0}))
    return jsonify(records)

@app.route('/labs/<string:lab_id>', methods=['GET'])
def get_lab_by_id(lab_id):
    check_api_key()
    lab = collection.find_one({'id': lab_id}, {'_id': 0})
    if lab:
        return jsonify(lab)
    else:
        return jsonify({"error": "Lab not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
