import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid

import datetime
import json
from pykafka import KafkaClient
from pykafka import SimpleConsumer
import time



with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def withdraw_book(body):
    """ Recieves a book withdrawal event """
    
    trace_id = str(uuid.uuid4())
    logger.info(f"Received event WithdrawalEvent with a trace id of {trace_id}")
    
    body['trace_id'] = trace_id

    producer = topic.get_sync_producer()

    msg = { "type": "WithdrawalEvent",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body } 
    
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    
    
    logger.info(f"Returned event WithdrawalEvent response (id: {trace_id}) with status 201")

    return NoContent, 201

def return_book(body):
    """ Recieves a book return event """

    trace_id = str(uuid.uuid4())
    logger.info(f"Received event ReturnEvent with a trace id of {trace_id}")

    body['trace_id'] = trace_id
    logger.debug(f"topic: {topic}")
    producer = topic.get_sync_producer()

    msg = { "type": "ReturnEvent",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body } 
    
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    
    logger.info(f"Returned event ReturnEvent response (id: {trace_id}) with status 201")

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    retry_count = 0
    while retry_count < int(app_config['connection']['retry_count']):
        logger.info(f"KafkaClient connection attempt #{retry_count}")

        try:
            hostname = f"{app_config['events']['hostname']}:{app_config['events']['port']}"
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config['events']['topic'])]
            logger.debug(f"topic: {topic}")
            app.run(port=8080)
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.error("Kafka connection failed... retrying...")
            time.sleep(int(app_config['connection']['sleep_duration']))
            retry_count+=1

    

