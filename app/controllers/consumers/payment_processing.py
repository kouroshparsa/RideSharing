"""
The purpose of this module is to charge the riders for the trip
If the operation fails, the payment request will be passed to a "RETRY_TOPIC"
"""
import os
import json
from kafka import KafkaConsumer
from app import logger
from app.models.model import Payment
from app.dto.payment import RiderPayment
from app.database import SessionLocal
from app.controllers.producers import failed_payment_processing


TOPIC_NAME = os.getenv("PAYMENT_PROCESSING_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")
session = SessionLocal()

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER],
                         value_deserializer = lambda v: json.loads(v.decode('ascii')),
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         consumer_timeout_ms=1000,
                         group_id='g1')

def charge_payment_gateway(rider_id: int, amount: float):
    """ payment gateway """
    print(f"Charged rider:{rider_id} ${amount}")

def save_to_db(rider_payment: RiderPayment):
    new_driver = Payment(rider_id=rider_payment.rider_id,
                         amount=rider_payment.amount,
                         payment_date=rider_payment.payment_date)
    session.add(new_driver)
    session.commit()

def main():
    """ picks up tasks to consume """
    try:
        consumer.subscribe(topics=[TOPIC_NAME])
        while True:
            msg = consumer.poll(60000) # this is in milliseconds

            if msg is None or msg == {}:
                continue

            for _,records in msg.items():
                for rec in records:
                    logger.info("Received a payment task from Kafka")
                    rider_payment = RiderPayment.model_validate(rec)
                    try:
                        charge_payment_gateway(rider_payment.rider_id, rider_payment.amount)
                    except Exception as ex:
                        logger.error(ex)
                        failed_payment_processing.resend_rider_payment(rider_payment)
                        continue
                    
                    save_to_db(rider_payment)

    except KeyboardInterrupt:
        logger.info('Caught KeyboardInterrupt, stopping.')
    finally:
        if consumer is not None:
            consumer.close() # autocommit=True by default so it will update the offset

if __name__ == '__main__':
    main()
