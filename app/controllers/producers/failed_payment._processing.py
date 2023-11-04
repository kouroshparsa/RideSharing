import os
from kafka import KafkaProducer
import json
from app.dto.payment import RiderPayment
from app import logger


TOPIC_NAME = os.getenv("FAILED_PAYMENT_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def resend_rider_payment(rider_payment: RiderPayment):
    logger.info("Sending failed rider payment task to Kafka")
    data = rider_payment.model_dump_json()
    producer.send(TOPIC_NAME, data)
    producer.flush() # is not needed on production
