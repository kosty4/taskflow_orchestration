# 📌 Taskflow Orchestration with Airflow

![Project Banner](stack.png)

> This is a project I worked on while learning about Airflow and task orchestration.
The goal of this project was to learn airflow and build a simple data backup application.

## 🚀 Features

- ✨ Use Airflow-provided PostgresToGCSOperator on a single table or set of tables to back up data to a GCS blob.
- 🔥 Created custom SQL Operator and GCS Hook to learn how to build custom extracting/loading functionality, inheriting from Airflow base classes.
- ⚡ Running DBT models using Airflow-provided DockerOperator
- 🎯 Running DBT models using custom-made DockerExecutorOperator that submits jobs to provisioned (hot) containers.


## 📖 Requirements

- You will need to setup your GCP project and Service Account yourself.
In short, this is how to do it:
1. Create your Service account in GCP Console
2. Add the admin storage role in IAM panel to the service account.
3. Download the Service Accouint JSON file. Place it here:
```sh
airflow/config/gcp-sva-file.json
```

## 📦 Installation

```sh
# Clone the repository
git clone https://github.com/kosty4/taskflow_orchestration.git
cd taskflow_orchestration

# Pull / Build images and Run the project
docker-compose up

```
This will build and start all the containers that are needed for this project.
The DB will also be seeded with some toy data. 


## 🔧 Airflow Configuration

- Once containers are up and running and service account file is placed, we need to add connections to airflow so they are indexed in the DAGS, allowing us read/write to Postgres and GCS

```sh
# 1. Get the ID of the Airflow Scheduler Contaniner and exec into it:
docker ps 
# We see 6bb6d8a90e58 runs as the scheduler
docker exec -it 6bb6d8a90e58 /bin/bash

# 2. Add Postgres connection
airflow connections add 'my_postgres_connection' --conn-type 'postgres' --conn-host 'postgres-data' --conn-schema 'simulator' --conn-login 'admin' --conn-password 'admin' --conn-port 5432

# 3. Add GCS connection 
airflow connections add 'google_cloud_default' --conn-type 'google_cloud_platform' --conn-extra '{"key_path": "./config/gcp-sva-file.json"}'

```

## 🛠 Tech Stack

- 🖥️ GCP
- 📚 Airflow
- 🏗️ DBT
- 🚀 Docker

## 🙌 Acknowledgments

- Thanks to [Gary Clark and Xccelerated team for provided training](https://github.com/gclarkjr5) (https://www.xccelerated.io)

---

⭐ **Don't forget to give this repo a star if you found it useful!** ⭐
