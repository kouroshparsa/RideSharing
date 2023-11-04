import os
from kafka import KafkaProducer
import json
from app import logger
from app.dto.driver import Location

TOPIC_NAME = os.getenv("LOCATION_MONITORING_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def update_location(driver_id: int, loc: Location):
    logger.info("Sending driver location to Kafka")
    data = {"driver_id": driver_id, "longitude": loc.longitude, "latitude": loc.latitude}
    producer.send(TOPIC_NAME, value=data)
    producer.flush() # is not needed on production
