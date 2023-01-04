from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import csv
from time import sleep


def load_avro_schema_from_file(main_path='./schema') -> tuple:
    key_schema = avro.load(
        f"{main_path}/btc_price_key.avsc"
    )
    value_schema = avro.load(
        f"{main_path}/btc_price_value.avsc"
    )
    return key_schema, value_schema

def push_record(producer, file, topic='teamai.btc_price_training') -> None:
    csvreader = csv.reader(file)
    header = next(csvreader) # skip first row

    for row in csvreader:
        key = {"Date": str(row[0])}
        value = {
            "Date": str(row[0]), 
            "Open": float(row[1]), 
            "High": float(row[2]), 
            "Low": float(row[3]), 
            "Close": float(row[4]),
            "Volume": str(row[5]),
            "Market_Cap": str(row[6])
            }

        try:
            producer.produce(topic=topic, key=key, value=value)
        except Exception as e:
            print(f"Exception while producing record value - {value}: {e}")
        else:
            print(f"Successfully producing record value - {value}")

        producer.flush()
        sleep(1)

if __name__ == "__main__":
    key_schema, value_schema = load_avro_schema_from_file()

    producer_config = {
        "bootstrap.servers": "broker:29092",
        "schema.registry.url": "http://schema-registry:8081",
        "acks": "1"
    }

    ####### Kafka Avro Producer #######
    producer = AvroProducer(producer_config,
    default_key_schema=key_schema, default_value_schema=value_schema)
    ###################################
    file = open('./data/bitcoin_price_training.csv')

    push_record(producer, file)