 
import json
import socket
import logging
import time
from confluent_kafka import Consumer

KAFKA_BROKER = 'kafka:29092'
CURRENCY_TOPIC = 'currency-rates'
BITCOIN_TOPIC = 'bitcoin-rates'

def create_consumer(topic, group_id):
    config = {
        "bootstrap.servers": "kafka:29092",
        "group.id": group_id,
        "auto.offset.reset": "latest"
    }
    try:
 
        consumer = Consumer(config)
        consumer.subscribe([topic])
        logging.info("Consumer created")
    except Exception as e:
        logging.exception("nie mogę utworzyć konsumenta")
        consumer = None
    return consumer

def print_currency():
    #time.sleep(60)
    CURRENCY_TOPIC = 'currency-rates'

    consumer = create_consumer(topic=CURRENCY_TOPIC, group_id=CURRENCY_TOPIC)
    print("Consumer created")
    logging.info("Consumer created")
    try:
        while True:
            message = consumer.poll()
            if message is None:
                print("Waiting...")
                logging.info("Waiting...")
            elif message.error():
                print(f"CONSUMER error: {message.error()}")
                logging.error(f"CONSUMER error: {message.error()}")
            else:
                print(f"Consumed event key = {message.key().decode('utf-8')} value = {message.value().decode('utf-8')}")
                logging.info(f"Consumed event key = {message.key().decode('utf-8')} value = {message.value().decode('utf-8')}")

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup.
        consumer.close()
