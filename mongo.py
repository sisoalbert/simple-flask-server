from flask import Flask, request, jsonify, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv() 

app = Flask(__name__)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'inserted_id': str(result.inserted_id)})

@app.route('/records', methods=['GET'])
def get_records():
    records = list(collection.find({}, {'_id': 0}))
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)
