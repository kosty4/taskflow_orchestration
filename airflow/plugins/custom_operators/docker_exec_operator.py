import docker
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from random import sample

class DockerContainerExecutorOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        container_name: str,
        command: str,
        min_memory: int = 100,  # MB
        min_cpu: float = 0.1,  # CPU units
        docker_url: str = "unix://var/run/docker.sock",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.container_name = container_name
        self.command = command
        self.min_memory = min_memory * 1024 * 1024  # Convert MB to Bytes
        self.min_cpu = min_cpu
        self.docker_url = docker_url

    def execute(self, context):
        client = docker.DockerClient(base_url=self.docker_url)
        
        # Get the container
        try:
            container = client.containers.get(self.container_name)
        except docker.errors.NotFound:
            self.log.error(f"Container '{self.container_name}' not found.")
            raise



        available_containers = client.containers.list(filters={'status':'running','ancestor':'dbt-custom-runner'})

        print(available_containers)

        # sample randomly
        selected_container = sample(available_containers,1)[0]

        # TODO
        exec_result = selected_container.exec_run(self.command)
        
        self.log.info(f"Command output: {exec_result.output.decode()}")
        return exec_result.output.decode()
