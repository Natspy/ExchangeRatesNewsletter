from flask import Flask, jsonify
from threading import Thread
from currency_bitcoin_consumer import run_consumer
from consumer_print import print_currency

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app.route('/start_consumer', methods=['GET'])
def start_consumer():
    task = Thread(target=print_currency)
    task.run
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
