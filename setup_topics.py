import os
import kafka
from kafka.admin import KafkaAdminClient, NewTopic
from dotenv import load_dotenv
load_dotenv()

#TOPICS_NAMES = ['fair_calculator', 'payment_processing', 'refund', 'driver_status', 'rating', 'payment_receipt']
TOPICS_NAMES = ['location_monitoring', 'payment_processing']
KAFKA_SERVER = os.getenv("KAFKA_SERVER")

def create_topic_with_partitions():
    consumer = kafka.KafkaConsumer(bootstrap_servers=[KAFKA_SERVER])
    consumer.topics()
    admin_client = KafkaAdminClient(bootstrap_servers=[KAFKA_SERVER])
    topics = []
    for topic in TOPICS_NAMES:
        topics.append(NewTopic(name=topic,
                               num_partitions=2,
                               replication_factor=1))
    admin_client.create_topics(new_topics=topics,
                                validate_only=False)
    admin_client.close()

if __name__ == "__main__":
    create_topic_with_partitions()