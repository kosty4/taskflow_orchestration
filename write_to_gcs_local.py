from google.cloud import storage

# Initialize the client
client = storage.Client.from_service_account_json('./gcp-sva-file.json')

# List buckets
# buckets = list(client.list_buckets())
# print("Buckets accessible:", buckets)

# Upload a file to the target bucket
bucket_name = 'ksmi-airflow'
bucket = client.bucket(bucket_name)
blob = bucket.blob('sample_file_to_write.txt')

blob.upload_from_string('This is a test file')
print("File uploaded successfully.")

