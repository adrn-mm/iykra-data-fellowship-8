from confluent_kafka.avro import AvroConsumer
from google.cloud import bigquery
from google.oauth2 import service_account

def bq_api(cred_file='/root/.credentials/creds.json') -> None:
    # PROJECT_ID = 'YOUR_GCP_PROJECT_ID'
    DATASET_NAME = 'btc_price'
    TABLE_NAME = 'stream_btc_train'

    creds = service_account.Credentials.from_service_account_file(cred_file)
    client_bq = bigquery.Client(credentials=creds)
    client_bq.create_dataset(DATASET_NAME, exists_ok=True)
    dataset_bq = client_bq.dataset(DATASET_NAME)
    schema_bq = [
        bigquery.SchemaField('Date', 'STRING'),
        bigquery.SchemaField('Open', 'FLOAT'),
        bigquery.SchemaField('High', 'FLOAT'),
        bigquery.SchemaField('Low', 'FLOAT'),
        bigquery.SchemaField('Close', 'FLOAT'),
        bigquery.SchemaField('Volume', 'STRING'),
        bigquery.SchemaField('Market_Cap', 'STRING')
    ]

    table_ref = bigquery.TableReference(dataset_bq, TABLE_NAME)
    table = bigquery.Table(table_ref, schema=schema_bq)
    client_bq.create_table(table, exists_ok=True)
    table_id = f'{DATASET_NAME}.{TABLE_NAME}'
    return client_bq, table_id

def pull_messages(consumer, topic='teamai.btc_price_training') -> None:
    tmp_cnt = 0
    msg_list = []
    consumer.subscribe([topic])
    client_bq, table_id = bq_api()

    while True:
        try:
            message = consumer.poll(5)
        except Exception as e:
            print(f"Exception while trying to poll messages - {e}")
        else:
            if tmp_cnt % 2 == 0 and tmp_cnt > 0:
                msg_list.append(message.value())
            if message:
                msg_prnt = f'''
                    Successfully poll a record from
                    Kafka topic: {message.topic()}, partition: {message.partition()}, offset: {message.offset()}
                    message key: {message.key()} || message value: {message.value()}
                '''
                print(msg_prnt)
                consumer.commit()

                ####### BigQuery Sink #######
                msg_sink = msg_list.copy()
                if tmp_cnt % 2 == 0 and tmp_cnt > 0:
                    sink_request = client_bq.insert_rows_json(table_id, msg_sink)

                    if sink_request == []:
                        print('Rows Pushed to Bigquery v')
                    else:
                        print(f'Error while Pushing: {sink_request}')
                msg_list.clear()
                #############################
                tmp_cnt += 1
            else:
                print("No new messages at this point. Try again later.")
    else:
        consumer.close()


if __name__ == "__main__":
    consumer_config = {
        "bootstrap.servers": "broker:29092",
        "schema.registry.url": "http://schema-registry:8081",
        "group.id": "teamai.btcprice.avro.consumer.1712",
        "auto.offset.reset": "earliest"
    }

    ####### Kafka Avro Consumer #######
    consumer = AvroConsumer(consumer_config)
    ###################################

    pull_messages(consumer)
