from airflow import DAG
from datetime import datetime
from custom_operators.sql_to_gcs_operator import SQLToGCSCustomOperator
from custom_operators.hooks import CustomSQLHook, ObjectStorageHook

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG('sql_to_gcs_custom',
         default_args=default_args,
         description='DAG to export SQL data to GCS as Parquet',
         schedule_interval=None,
         start_date=datetime(2023, 1, 1),
         catchup=False) as dag:

    export_task = SQLToGCSCustomOperator(
        task_id='export_sql_to_gcs_custom',
        sql_query='SELECT * FROM event',
        gcs_bucket='ksmi-airflow',
        gcs_filename='event_table_file.parquet',
        sql_hook=CustomSQLHook(conn_id='my_postgres_connection'),
        object_storage_hook=ObjectStorageHook(conn_id='google_cloud_default')
    )

    export_task
