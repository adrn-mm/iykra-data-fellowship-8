import os
import logging

import requests
import json
import csv
import pandas as pd

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateExternalTableOperator,
)
import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
# PROJECT_ID = "data-fellowship-8-adrian"
# BUCKET = "dummy-bucket-adrian"

dataset_file = "population.csv"
dataset_url = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
# path_to_local_home = "/opt/airflow/"
parquet_file = dataset_file.replace(".csv", ".parquet")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "population")


def call_dataset_task(dataset_url, ti):
    """
    get the dataset from url
    """
    res = requests.get(dataset_url)
    parse_json = json.loads(res.text)
    data_json = parse_json["data"]
    ti.xcom_push(key="data_json", value=data_json)


def save_as_csv(path_to_local_home, dataset_file, ti):
    """
    save the data to csv
    """
    data_file = open("{}/{}".format(path_to_local_home, dataset_file), "w")
    csv_writer = csv.writer(data_file)
    count = 0
    data_json = ti.xcom_pull(key="data_json", task_ids="call_dataset_task")
    for emp in data_json:
        if count == 0:  # Writing headers of CSV file
            header = emp.keys()
            csv_writer.writerow(header)
            count += 1  # Writing data of CSV file
        csv_writer.writerow(emp.values())
    data_file.close()


def format_to_parquet(src_file):
    if not src_file.endswith(".csv"):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace(".csv", ".parquet"))


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["dtc-de"],
) as dag:

    call_dataset_task = PythonOperator(
        task_id="call_dataset_task",
        python_callable=call_dataset_task,
        op_kwargs={"dataset_url": dataset_url},
    )

    save_as_csv = PythonOperator(
        task_id="save_as_csv",
        python_callable=save_as_csv,
        op_kwargs={
            "path_to_local_home": path_to_local_home,
            "dataset_file": dataset_file,
        },
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{parquet_file}"],
            },
        },
    )

    (
        call_dataset_task
        >> save_as_csv
        >> format_to_parquet_task
        >> local_to_gcs_task
        >> bigquery_external_table_task
    )
