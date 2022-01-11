from kafka import KafkaConsumer

kafka_consumer = KafkaConsumer(
    bootstrap_servers=["kafka_server:9092"],
    group_id="test")
kafka_consumer.subscribe(topics=["user-task"])
