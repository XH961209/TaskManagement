import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

while True:
    time.sleep(1)
    try:
        kafka_consumer = KafkaConsumer(
            bootstrap_servers=["kafka_server:9092"],
            group_id="test")
        kafka_consumer.subscribe(topics=["user-task"])
        break
    except NoBrokersAvailable as e:
        print(e)
