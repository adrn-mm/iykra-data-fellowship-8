# IYKRA DF 8 Program Assignment 2 - Adrian Maulana Muhammad
## Assignment Objective
Silahkan buat DAG yang mengekstrak data dari API ini : https://datausa.io/api/data?drilldowns=Nation&measures=Population  Kemudian diakhir pipeline akan di load ke external table bigquery seperti pada pertemuan sebelumnya.
## Project Description
The project modifies the datasource and DAGS of the given project in session 2.
### Download the Datasource
The data in this task is in the form of JSON API. First, we will make a request and parse it, this process is the contents of the `call_dataset_task` function. Second, the data that has been called and parsed will be downloaded locally in CSV form, this process is the contents of the `save_as_csv` function. To be able to interact between the two tasks, I use the help of Xcom from Airflow.
## Modify the DAGS
i changed the DAGS order to be as follows:
`call_dataset_task` -> `save_as_csv` -> `format_to_parquet_task` -> `local_to_gcs_task` -> `bigquery_external_table_task`