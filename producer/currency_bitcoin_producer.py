import time
import json
import logging
import requests
import socket
from confluent_kafka import Producer

# Kafka configuration
KAFKA_BROKER = 'kafka:29092'
CURRENCY_TOPIC = 'currency-rates'
BITCOIN_TOPIC = 'bitcoin-rates'

# API endpoints
NBP_API_URL = 'http://api.nbp.pl/api/exchangerates/tables/A?format=json'
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_producer():
    config = {
        "bootstrap.servers": 'kafka:29092',
        #"client.id": socket.gethostname(),
        #"enable.idempotence": True,
        #"batch.size": 64000,
        #"linger.ms": 10,
        #"acks": "all",
        #"retries": 5,
        #"delivery.timeout.ms": 1000
    }
    try:
        producer = Producer(config)
        logging.info("Kafka producer created successfully")
    except Exception as e:
        logging.exception("Cannot create producer")
        producer = None
    return producer

def fetch_currency_rates():
    producer = create_producer()
    try:
        response = requests.get(NBP_API_URL)
        if response.status_code == 200:
            data = response.json()[0]['rates']
            for rate in data:
                rate_record = {
                    "timestamp": int(time.time()),
                    "currency": rate['currency'],
                    "code": rate['code'],
                    "rate": rate['mid']
                }
                print(f"Fetched currency rate: {rate_record}")  # Print the data
                producer.produce(CURRENCY_TOPIC, key=rate['code'], value=json.dumps(rate_record))
            logging.info("Currency rates fetched and sent to Kafka")
        else:
            logging.error(f"Failed to fetch currency rates: {response.status_code}")
    except Exception as e:
        logging.exception("Failed to fetch currency rates")
    producer.flush()

def fetch_bitcoin_rate():
    producer = create_producer()
    try:
        response = requests.get(COINGECKO_API_URL)
        if response.status_code == 200:
            data = response.json()
            rate_record = {
                "timestamp": int(time.time()),
                "currency": "bitcoin",
                "rate": data['bitcoin']['usd']
            }
            print(f"Fetched bitcoin rate: {rate_record}")  # Print the data
            producer.produce(BITCOIN_TOPIC, key="bitcoin", value=json.dumps(rate_record))
            logging.info("Bitcoin rate fetched and sent to Kafka")
        else:
            logging.error(f"Failed to fetch bitcoin rate: {response.status_code}")
    except Exception as e:
        logging.exception("Failed to fetch bitcoin rate")
    producer.flush()

def run_producer():
    fetch_currency_rates()
    fetch_bitcoin_rate()
