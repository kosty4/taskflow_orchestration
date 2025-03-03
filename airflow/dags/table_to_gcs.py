from airflow import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.utils.dates import days_ago

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='example_postgres_table_to_gcs',
    default_args=default_args,
    description='A simple example to transfer data from Postgres table to GCS',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task: Transfer data from PostgreSQL to GCS
    transfer_postgres_to_gcs = PostgresToGCSOperator(
        task_id='transfer_postgres_table_to_gcs',
        postgres_conn_id='my_postgres_connection',  # Connection ID for Postgres
        sql='SELECT * FROM event',      # SQL query to extract data
        bucket='ksmi-airflow',          # GCS bucket name
        filename='synced_data.json',    # GCS object name (path in bucket)
        export_format='json',           # Format: 'json', 'csv', or 'parquet'
        gzip=False                      # Set to True if you want gzip compression
    )

    # Add more tasks as needed
    transfer_postgres_to_gcs
