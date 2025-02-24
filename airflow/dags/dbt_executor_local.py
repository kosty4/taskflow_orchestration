
# Example usage in an Airflow DAG
from airflow import DAG
from airflow.utils.dates import days_ago
from custom_operators.docker_exec_operator import DockerContainerExecutorOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

with DAG(
    'docker_command_execution_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
    ) as dag:

    execute_task = DockerContainerExecutorOperator(
        task_id='execute_command_in_container',
        container_name='sharp_jones',
        command='dbt run --target staging',
        min_memory=200,  # 200MB
        min_cpu=0.2,  # 0.2 CPU units
    )

    execute_task
