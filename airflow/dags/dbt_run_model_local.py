from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    'dbt_run_dag',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    run_dbt = DockerOperator(
        task_id='run_dbt_models_local',
        image='dbt-runner:latest',
        container_name='dbt_container',
        api_version='auto',
        auto_remove=True,
        command="run --target staging",
        network_mode="airflow_default",  # Same network as docker-compose
        docker_url="unix://var/run/docker.sock",
        mount_tmp_dir=True
    )

    run_dbt
