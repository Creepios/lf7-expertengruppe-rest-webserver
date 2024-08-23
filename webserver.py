import os
import json
import time
from flask import Flask, request, jsonify
import logging

# Set-up der Log-Funktion
def setup_logger(log_file):
    """
    Einrichten des Loggers.

    :param log_file: Dateiname für die Log-Datei
    :return: Logger-Objekt
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Handling der Datei der Logs
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    return logger

logger = setup_logger('api_logs.log')


## Initialisierung der Flask App
app = Flask(__name__)

# Log-Funktion
def log_request(ip_address, endpoint, method, user_agent=None, referrer=None):
    """
    Protokolliert einen Request.

    :param ip_address: IP-Adresse des Clients
    :param endpoint: Aufgerufener Endpoint
    :param method: HTTP-Methode (z.B. GET, POST, etc.)
    :param user_agent: User-Agent-String des Clients
    :param referrer: Referrer-URL des Clients
    """
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


# Standard Pfad
# Wenn dieser Pfad (http://172.20.181.253:5001/) aufgerufen wird, wird dies dargestellt
@app.route("/")
def hello_world():
    """
    Standard-Endpoint, der eine Begrüßung zurückgibt.

    :return: HTML-String mit Begrüßung
    """
    return "<h1>Die Expertengruppe der Experten</h1>"


# Methode zur Erstellung der Daten
#
# Ein API-Call zu dem Pfad /create erstellt einen neuen Eintrag und speichert diesen
# Hier muss ein gewisser Datensatz mit angegeben werden
# 
# Der Aufruf muss aus einem "value" und einem Wert als Integer oder Float bestehen
@app.route("/create", methods=['POST'])
def add_data():
    """
    Erstellt einen neuen Eintrag und speichert ihn.

    :param request: JSON-Request mit "value"-Feld
    :return: JSON-Response mit dem neuen Eintrag
    """
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


## Methode zum Lesen aller Daten
# 
# Der Aufruf über /read liest alle Daten aus, die aktuell zur Verfügung stehen und gibt sie zurück
@app.route("/read", methods=['GET'])
def read_data():
    """
    Liest alle Daten aus und gibt sie zurück.

    :return: JSON-Response mit allen Daten
    """
    logger.info("Received a GET request")
    return jsonify(data)


## Methode zum Lesen des letzten Eintrages
# 
# Über den Aufruf mit /last kann der letzte Wert, welcher zur Verfügung steht, ausgelesen werden
@app.route("/last", methods=['GET'])
def get_last():
    """
    Liest den letzten Eintrag aus und gibt ihn zurück.

    :return: JSON-Response mit dem letzten Eintrag
    """
    if not data:
        logger.error("No data available.")
        return jsonify({"error": "No data available"}), 404
    lastKey = list(data)[-1]
    logger.info("Received a GET request")
    return jsonify({lastKey: data[lastKey]})


## Methode zum Löschen der Daten
#
# Die /delete -Route hat zwei Funktionen 
# 
# Es besteht die Möglichkeit, nur den /delete Pfad zu verwenden.
# Hier werden dann alle Einträge gelöscht, die aktuell vorhanden sind
# 
# Allerdings kann auch ein weiteres Argument angegeben werden.
# Bsp.: http://172.20.181.253:5001/delete?n=2
# In dem Beispiel werden nur die genannte Anzahl gelöscht
#
# Hier wird FIFO benutzt
@app.route("/delete", methods=['DELETE'])
def delete_data():
    """
    Löscht Daten.

    :param n: Anzahl der zu löschenden Einträge (optional)
    :return: JSON-Response mit Erfolgsmeldung
    """
    logger.info("Received a DELETE request")
    n = request.args.get('n')
    if n is None:
        data.clear()
    else:
        n = int(n)
        for _ in range(n):
            if data:
                data.pop(next(iter(data)))
    save_json(data)
    if n is None:
        logger.info("Deleted all items successfully")
        return jsonify({"message": "Deleted all items successfully"})
    else:
        logger.info(f"Deleted {n} items successfully")
        return jsonify({"message": f"Deleted {n} items successfully"})


## Methode zur Überarbeitung der Daten
#
# Über /update können einzelne Einträge bearbeitet werden, ohne diese zu Löschen.
#
# Hier müssen wieder Daten mit übergeben werden
# Daten müssen vorliegen als ein key und einem value
#
# In unserem Beispiel ist der key immer das Datum und Uhrzeit, wann ein Eintrag gesetzt wurde.
# Dieser muss mit einem der aktuell vorhandenen Werte übereinstimmen
# Tue Aug 20 10:24:07 2024
# Der value ist kann dann auf den gewünschten Wert gesetzt werden
@app.route("/update", methods=['PUT'])
def update_data():  
    """
    Aktualisiert einen Eintrag.

    :param request: JSON-Request mit "key" und "value"-Feldern
    :return: JSON-Response mit Erfolgsmeldung
    """
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


## Funktion zum speichern der Daten in einer JSON-Datei
def save_json(data):
    """
    Speichert die Daten in einer JSON-Datei.

    :param data: Daten-Dictionary
    """
    with open('data.json', 'w') as jsonfile:
        json.dump(data, jsonfile)


## Der Main-Wächter
# Dieser Codeblock wird nur ausgeführt, wenn das Skript
# direkt gestartet wird (z.B. durch Ausführen des Skripts in der Kommandozeile).
# Wenn das Skript als Modul von einem anderen Skript importiert wird, wird
# dieser Codeblock übersprungen.
#
# Der Flask-Webservers wird hier auf den Port 5001 festgelegt
if __name__ == '__main__':
    print("Server is running")
    app.run(debug=True, port=5001, host='0.0.0.0')
