 
import json
import socket
import logging
from datetime import datetime
import numpy as np
from confluent_kafka import Consumer
from mailer import send_email

rates_limit = 100
subject = "Exchange rates - Newsletter"
recipients = ["nataliakarczewskapp@gmail.com"]


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
    currency = {}
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
                
                message_values = json.loads(message.value().decode('utf-8'))

                rate = message_values['rate']

                try: 
                    currency[message.key()].append(rate)
                
                except:
                    currency[message.key()] = []
                    currency[message.key()].append(rate)

                if len(currency[message.key()]) > rates_limit:
                    currency[message.key()].pop(0)

                if len(currency[message.key()]) > 10:
                
                    sma3 = np.average(np.array(currency[message.key()])[-70:])

                    sma10 = np.average(np.array(currency[message.key()]))

                    if sma3 > 1.01 * sma10:
                        current_date = datetime.now().strftime("%d.%m.%Y")
                        body = "Calculation at {}: SMA3 value {:.6f}, SMA10 value {:.6f}. BUY! Currency code: {}".format(current_date, sma3, sma10, str(message.key())[1:])
                        send_email(subject, body, recipients)
                        logging.info("Message sent: " + body)
                    elif sma3 < 0.99 * sma10:
                        current_date = datetime.now().strftime("%d.%m.%Y")
                        body = "Calculation at {}: SMA3 value {:.6f}, SMA10 value {:.6f}. SELL! Currency code: {}".format(current_date, sma3, sma10, str(message.key())[1:])
                        send_email(subject, body, recipients)
                        logging.info("Message sent: " + body)
                    else:
                        pass

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup.
        consumer.close()
