from flask import Flask
from flask_apscheduler import APScheduler
from currency_bitcoin_producer import run_producer

app = Flask(__name__)
scheduler = APScheduler()

def scheduleTask():
    run_producer()

@app.route('/status', methods=['GET'])
def get_status():
    return 200


if __name__ == '__main__':
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", minutes=1)
    scheduler.start()
    app.run(debug=True, host='0.0.0.0')
