from time import sleep
import csv 
from kafka import KafkaProducer
import json

print("Starting Kafka Producer...")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda x: 
                        json.dumps(x).encode('utf-8'))

print("Opening CSV...")

with open('twitter_validation.csv', encoding='utf-8') as file_obj:
    reader_obj = csv.reader(file_obj)
    for i, data in enumerate(reader_obj): 
        print(f"[{i}] Sending: {data}")
        producer.send('numtest', value=data)
        sleep(3)

print("Finished sending data.")
