import os
import json
import time
from flask import Flask, request, jsonify
import logging


def setup_logger(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    return logger

logger = setup_logger('api_logs.log')

app = Flask(__name__)

def log_request(ip_address, endpoint, method, user_agent=None, referrer=None):
    logger.info(f"Received {method} request from {ip_address} to {endpoint} (User-Agent: {user_agent}, Referrer: {referrer})")

@app.before_request
def log_request_before():
    ip_address = request.remote_addr
    endpoint = request.path
    method = request.method
    user_agent = request.user_agent.string
    referrer = request.referrer
    log_request(ip_address, endpoint, method, user_agent, referrer)

@app.after_request
def log_request_after(response):
    ip_address = request.remote_addr
    endpoint = request.path
    method = request.method
    user_agent = request.user_agent.string
    referrer = request.referrer
    log_request(ip_address, endpoint, method, user_agent, referrer)
    return response

data = {}
if os.path.exists('data.json'):
    with open('data.json', 'r') as jsonfile:
        data = json.load(jsonfile)

@app.route("/")
def hello_world():
    return "<h1>Die Expertengruppe der Experten</h1>"

@app.route("/create", methods=['POST'])
def add_data():
    logger.info("Received a POST request")
    received_data = request.get_json()
    if "value" in received_data and isinstance(received_data["value"], (float, int)): 
        data[str(time.ctime())] = float(received_data["value"])
        save_json(data)
        logger.info("Data added successfully")
        return jsonify(data)
    else:
        logger.error("Invalid data. Please provide a single float or double value.")
        return jsonify({"error": "Invalid data. Please provide a single float or double value."}), 400
    
@app.route("/read", methods=['GET'])
def read_data():
    logger.info("Received a GET request")
    return jsonify(data)

@app.route("/last", methods=['GET'])
def get_last():
    if not data:
        logger.error("No data available.")
        return jsonify({"error": "No data available"}), 404
    lastKey = list(data)[-1]
    logger.info("Received a GET request")
    return jsonify({lastKey: data[lastKey]})

@app.route("/delete", methods=['DELETE'])
def delete_data():
    logger.info("Received a DELETE request")
    data.clear()
    save_json(data)
    logger.info("Data deleted successfully")
    return jsonify({"message": "Data deleted successfully"})

@app.route("/update", methods=['PUT'])
def update_data():
    logger.info("Received a PUT request")
    received_data = request.get_json()
    if "key" in received_data and "value" in received_data:
        key = received_data["key"]
        if key in data:
            if isinstance(received_data["value"], (float, int)):
                data[key] = float(received_data["value"])
                save_json(data)
                logger.info("Data updated successfully")
                return jsonify({"message": "Data updated successfully"})
            else:
                logger.error("Invalid data. Please provide a single float or double value.")
                return jsonify({"error": "Invalid data. Please provide a single float or double value."}), 400
        else:
            logger.error("Key not found")
            return jsonify({"error": "Key not found"}), 404
    else:
        logger.error("Invalid request. Please provide key and value.")
        return jsonify({"error": "Invalid request. Please provide key and value."}), 400


def save_json(data):
    with open('data.json', 'w') as jsonfile:
        json.dump(data, jsonfile)

if __name__ == '__main__':
    print("Server is running")
    app.run(debug=True, port=5001, host='0.0.0.0')
