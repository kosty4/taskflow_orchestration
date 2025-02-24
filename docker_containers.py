import docker
client = client = docker.DockerClient(base_url='unix:///Users/ksdev/.docker/run/docker.sock')


container_name = "postgres"

# Get the container
try:
    container = client.containers.get(container_name)
except docker.errors.NotFound:
    print(f"Container '{container_name}' not found.")
    raise

# Get container stats
stats = container.stats(stream=False)
memory_usage = stats['memory_stats']['usage']
cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
num_cpus = len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
cpu_usage = (cpu_delta / system_delta) * num_cpus if system_delta > 0 else 0

print(f"Container '{container_name}' Memory Usage: {memory_usage / 1024 / 1024} MB")
print(f"Container '{container_name}' CPU Usage: {cpu_usage} CPUs")