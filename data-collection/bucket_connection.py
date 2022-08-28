import pandas as pd
import boto3

import io
import time
import gzip

# NOTE - Never share your actual key ID or key! If you replace these values with the actual keys during testing, don't forget to remove them before committing changes
session = boto3.Session(
    aws_access_key_id='ACCESS KEY ID',
    aws_secret_access_key='ACCESS KEY',
)

s3_resource = session.resource('s3')
bucket = s3_resource.Bucket("rainfall-normalized")

for file in bucket.objects.all():
    time_start = time.perf_counter()

    # Stores date and time that the file was created
    timestamp = file.last_modified
    content = ""

    with gzip.GzipFile(fileobj=file.get()["Body"]) as gzipfile:
        content = gzipfile.read()
        
    dataframe = pd.read_csv(io.BytesIO(content))

    time_end = time.perf_counter()
    print(f"LAST FILE TOOK {time_end - time_start:0.4f} SECONDS TO DOWNLOAD.")