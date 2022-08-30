from datetime import datetime, timedelta
import pandas as pd
import boto3
import yaml
import gzip


with open("./config.yml") as file:
    config = yaml.safe_load(file)

session = boto3.Session(
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
)

s3_resource = session.resource('s3')

time = datetime(2020, 12, 27)

file = f"{time.year}/{str(time.month).zfill(2)}/{time.year}{str(time.month).zfill(2)}{str(time.day).zfill(2)}.csv.gz"
print(file)
buck = s3_resource.Bucket("rainfall-normalized")
a = buck.download_file("2020/12/20201227.csv.gz", "tmp/file.csv.gz")

with gzip.open("tmp/file.csv.gz", 'rb') as f:
    with open("tmp/file.csv", "wb") as file:
        file.write(f.read())

df = pd.read_csv("tmp/file.csv")
