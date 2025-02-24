import tempfile
import json
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
from custom_operators.hooks import CustomSQLHook, ObjectStorageHook

class SQLToGCSCustomOperator(BaseOperator):
    """
    Custom operator to export data from a SQL table to a Parquet file and upload it to GCS.
    """

    @apply_defaults
    def __init__(
        self,
        sql_query: str,
        gcs_bucket: str,
        gcs_filename: str,
        object_storage_hook: ObjectStorageHook,
        sql_hook: CustomSQLHook,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.sql_query = sql_query
        self.gcs_bucket = gcs_bucket
        self.gcs_filename = gcs_filename
        self.object_storage_hook = object_storage_hook
        self.sql_hook = sql_hook


    def execute(self, context):

        with self.sql_hook.get_connection() as connection:
            self.log.info("Executing SQL query and saving results to Parquet file: %s", self.sql_query)
            df = pd.read_sql(self.sql_query, connection) # Watch out with memory size here !

        # Create a temporary file for the Parquet file
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=True) as temp_file:
            self.log.info("Fetched data from SQL query. Preparing Parquet file...")
            temp_file_path = temp_file.name
            
            # pd.write_to_dataset ?
            # Q: Why arrow?
            df.to_parquet(temp_file_path, engine='pyarrow', index=False) 

            self.log.info("Parquet file saved to temporary path: %s", temp_file_path)

            # Upload Parquet file to GCS
            self.log.info("Uploading Parquet file to GCS: bucket=%s, filename=%s", self.gcs_bucket, self.gcs_filename)

            self.object_storage_hook.upload(
                bucket_name=self.gcs_bucket,
                object_name=self.gcs_filename,
                filename=temp_file_path
            )

            self.log.info("File successfully uploaded to GCS.")
