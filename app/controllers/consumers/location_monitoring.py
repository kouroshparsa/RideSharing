"""
The purpose of this module is to fetch driver locations and save them to the database
If it fails to write to the db, it will lose the information and will not try it again
"""
import os
from kafka import KafkaConsumer
import json
from app import logger
from app.models.model import Driver
from app.database import SessionLocal
from sqlalchemy import update

TOPIC_NAME = os.getenv("LOCATION_MONITORING_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")
session = SessionLocal()

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER],
                         value_deserializer = lambda v: json.loads(v.decode('ascii')),
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         consumer_timeout_ms=1000,
                         group_id='g1')


try:
    consumer.subscribe(topics=[TOPIC_NAME])
    while True:
        msg = consumer.poll(60000) # this is in milliseconds

        if msg is None or msg == {}:
            continue

        locations = []
        for _,records in msg.items():
            for rec in records:
                print(rec.value)
                locations.append(rec.value)
        
        logger.info("Received {} driver locations from Kafka".format(len(locations)))
        for rec in locations:
            stmt = update(Driver).where(Driver.id == rec["driver_id"]).values(location=f'POINT({rec["longitude"]} {rec["latitude"]})')
            session.execute(stmt)
            session.commit()

except KeyboardInterrupt:
    logger.info('Caught KeyboardInterrupt, stopping.')
finally:
    if consumer is not None:
        consumer.close() # autocommit=True by default so it will update the offset