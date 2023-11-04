import os
from kafka import KafkaProducer
import json
from datetime import datetime
from app import logger

PAYMENT_PROCESSING_TOPIC = os.getenv("PAYMENT_PROCESSING_TOPIC")
EARNING_PROCESSING_TOPIC = os.getenv("EARNING_PROCESSING_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_rider_payment(rider_id: int, amount: float, payment_date: datetime):
    logger.info("Sending rider payment task to Kafka")
    data = {"rider_id": rider_id, "amount": amount, "payment_date": payment_date}
    producer.send(PAYMENT_PROCESSING_TOPIC, data)
    producer.flush() # is not needed on production

def send_driver_earning(driver_id: int, amount: float, earning_date: datetime):
    logger.info("Sending driver payment task to Kafka")
    data = {"driver_id": driver_id, "amount": amount, "earning_date": earning_date}
    producer.send(EARNING_PROCESSING_TOPIC, data)
    producer.flush() # is not needed on production