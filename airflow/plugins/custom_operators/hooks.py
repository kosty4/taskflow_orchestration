from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine
import json
from google.cloud import storage

class CustomSQLHook(BaseHook):
    def __init__(self, conn_id: str):
        super().__init__()
        self.conn_id = conn_id
        self.engine = self.get_engine()
    
    def get_connection(self):
        """
        Get connection for the hook
        """

        return self.engine.connect()

    def get_engine(self):
        """
        Get a SQLAlchemy engine using an Airflow connection ID.

        :param conn_id: The Airflow connection ID.
        :return: A SQLAlchemy engine.
        """

        self.log.info("Getting SQL connection using connection ID: %s", self.conn_id)

        # Retrieve the connection object using BaseHook
        connection = BaseHook.get_connection(self.conn_id)
        
        # Construct the SQLAlchemy connection string
        conn_type = connection.conn_type
        host = connection.host
        schema = connection.schema
        login = connection.login
        password = connection.password
        port = connection.port

        # WTF?
        if conn_type == 'postgres':
            conn_type = 'postgresql'

        # Create the connection string (example for PostgreSQL)
        connection_string = f"{conn_type}://{login}:{password}@{host}:{port}/{schema}"
        
        # Create and return the SQLAlchemy engine
        engine = create_engine(connection_string)
        return engine
    
class ObjectStorageHook(BaseHook):

    def __init__(self, conn_id):
        self.conn_id = conn_id

    
    def upload(self, bucket_name, object_name, filename):
        """Uploads a file to the Google Cloud Storage bucket"""

        # Initialize the Google Cloud Storage client
        storage_client = storage.Client.from_service_account_json('./config/gcp-sva-file.json') #BIG TODO

        # Get the bucket object
        bucket = storage_client.get_bucket(bucket_name)

        # Create a blob (object) in the bucket with the destination name
        blob = bucket.blob(object_name)

        print(f'Uploading {object_name}  from {filename}.')

        # Upload the file to the bucket
        blob.upload_from_filename(filename)

        print(f'File {object_name} uploaded to {filename}.')

