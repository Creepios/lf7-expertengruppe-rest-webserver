import os
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

data = {}
if os.path.exists('data.json'):
    with open('data.json', 'r') as jsonfile:
        data = json.load(jsonfile)

@app.route("/")
def hello_world():
    return "<h1>Die Expertengruppe der Experten</h1>"

@app.route("/create", methods=['POST'])
def add_data():
    received_data = request.get_json()
    if "value" in received_data and isinstance(received_data["value"], (float, int)): 
        data[str(time.ctime())] = float(received_data["value"])
        save_json(data)
        return jsonify(data)
    else:
        return jsonify({"error": "Invalid data. Please provide a single float or double value."}), 400
    
@app.route("/read", methods=['GET'])
def read_data():
    return jsonify(data)

@app.route("/delete", methods=['DELETE'])
def delete_data():
    data.clear()
    save_json(data)
    return jsonify({"message": "Data deleted successfully"})

@app.route("/update", methods=['PUT'])
def update_data():
    received_data = request.get_json()
    if "key" in received_data and "value" in received_data:
        key = received_data["key"]
        if key in data:
            if isinstance(received_data["value"], (float, int)):
                data[key] = float(received_data["value"])
                save_json(data)
                return jsonify({"message": "Data updated successfully"})
            else:
                return jsonify({"error": "Invalid data. Please provide a single float or double value."}), 400
        else:
            return jsonify({"error": "Key not found"}), 404
    else:
        return jsonify({"error": "Invalid request. Please provide key and value."}), 400


def save_json(data):
    with open('data.json', 'w') as jsonfile:
        json.dump(data, jsonfile)

if __name__ == '__main__':
    print("Server is running")
    app.run(debug=True)
