from flask import Flask, request
import time
import json

data = {}

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Die Expertengruppe der Experten</h1>"

@app.route("/create", methods=['POST'])
def add_data():
    received_data = request.args.get('data')
    print(received_data)
    data[str(time.ctime())] = received_data
    save_json(data)
    return data

@app.route("/last", methods=['GET'])
def get_last():
    lastKey = list(data)[-1]
    return data[lastKey]

@app.route("/all", methods=['GET'])
def get_all():
    return json.dumps(data, indent=4)


def read_json():
    with open('data.json', 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

def save_json(data):
    with open('data.json', 'w') as jsonfile:
        json.dump(data, jsonfile)



if __name__ == '__main__':
    print("Server is running")
    data = read_json()
    app.run(debug=True)
    