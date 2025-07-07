
import json, random, time, datetime, uuid, argparse, sys
from faker import Faker
fake = Faker()

def gen_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": random.randint(1, 10000),
        "event_type": random.choice(["login","view_item","add_to_cart","checkout"]),
        "device": random.choice(["web","ios","android"]),
        "ts": datetime.datetime.utcnow().isoformat()
    }

def to_kafka(event, producer, topic):
    producer.produce(topic, json.dumps(event).encode())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka", action="store_true", help="send to kafka, otherwise stdout")
    args = parser.parse_args()
    if args.kafka:
        from confluent_kafka import Producer
        producer = Producer({"bootstrap.servers":"localhost:9092"})
    else:
        producer = None
    topic = "events"
    while True:
        ev = gen_event()
        if producer:
            to_kafka(ev, producer, topic)
        else:
            print(json.dumps(ev))
        time.sleep(0.1)

if __name__ == "__main__":
    main()
