from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.utils.dates import days_ago
from airflow import DAG

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': days_ago(1)
}

class DagTemplate:
    
    def __init__(self, postgres_conn_id: str, gcs_bucket_name: str):
        self.postgres_conn_id = postgres_conn_id
        self.gcs_bucket_name = gcs_bucket_name

    def generate(self, table_name: str, dag_id: str) -> DAG:

        with DAG(
            default_args=default_args,
            catchup=False,
            dag_id=dag_id
        ) as dag:
            # Task: Transfer data from PostgreSQL to GCS
            transfer_postgres_to_gcs = PostgresToGCSOperator(
                task_id=f"export_{table_name}_to_gcs",
                postgres_conn_id='my_postgres_connection',  # Connection ID for Postgres
                sql=f'SELECT * FROM {table_name}',          # SQL query to extract data     
                bucket=self.gcs_bucket_name,     # GCS bucket name
                filename=f"{table_name}.json",     # GCS object name (path in bucket)
                export_format='json',    # Format: 'json', 'csv', or 'parquet'
                gzip=False               # Set to True if you want gzip compression
            )

            transfer_postgres_to_gcs
        
        return dag

postgres_config = {
    "tables": ["category", "orders", "events"],
    "config": {
        "postgres_conn_id": "my_postgres_connection",
        "gcs_bucket_name": "ksmi-airflow"
    }
}

dag_factory = DagTemplate(**postgres_config['config'])


for table in postgres_config["tables"]:

    dag_id = f"export_table_{table}_to_gcs_dag"

    globals()[dag_id] = dag_factory.generate(table_name=table, dag_id=dag_id)