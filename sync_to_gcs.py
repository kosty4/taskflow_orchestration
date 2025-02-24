from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

def extract_data_from_postgres(**kwargs):
    """Extract data from PostgreSQL database."""
    print('starting!!!')

    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
    sql = """SELECT * FROM event LIMIT 10;"""
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    connection.close()

    # Convert to Pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Save the DataFrame to a temporary Parquet file
    output_path = '/tmp/simulator_event.parquet'
    df.to_parquet(output_path, index=False)

    print(df.head())

    # Push the file path to XCom for the next task
    kwargs['ti'].xcom_push(key='parquet_file_path', value=output_path)

def upload_to_gcs(**kwargs):
    """Upload the Parquet file to GCS."""
    gcs_hook = GCSHook(gcp_conn_id='your_gcs_connection')
    bucket_name = 'your_gcs_bucket'
    destination_path = 'simulator_event/simulator_event.parquet'

    # Retrieve the file path from XCom
    parquet_file_path = kwargs['ti'].xcom_pull(task_ids='extract_data', key='parquet_file_path')

    # Upload to GCS
    gcs_hook.upload(
        bucket_name=bucket_name,
        object_name=destination_path,
        filename=parquet_file_path
    )

    # Clean up the local file
    os.remove(parquet_file_path)

# Define the DAG
dag = DAG(
    'postgres_to_gcs',
    default_args=default_args,
    description='Extract data from PostgreSQL and save it to GCS as Parquet.',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define tasks
extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_from_postgres,
    provide_context=True,
    dag=dag,
)

# upload_data = PythonOperator(
#     task_id='upload_to_gcs',
#     python_callable=upload_to_gcs,
#     provide_context=True,
#     dag=dag,
# )

# Task dependencies
# extract_data >> upload_data
extract_data
