'''

NOTES
- Way too slow! Takes around 40 seconds per file, and there are 96 files per day
- Way too many database inserts! Between 90 and 100k per file

THOUGHTS
- Forget the database idea, find better way to store 2D arrays in small files and upload to AWS cloud storage

'''

import netCDF4 as nc
import pandas as pd
import boto3 as boto
import numpy as np
import mysql.connector

from botocore.handlers import disable_signing
from io import BytesIO
import datetime
import time
import gzip

# Set up the local MySQL connection
connection = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='rainfall')
cursor = connection.cursor()

# Create command execution method to catch errors
def execute(command):
	try:
		cursor.execute(command)
	except mysql.connector.Error as error:
		print("An error occured - " + error)

# Disable signing to access S3 bucket without credentials
s3_resource = boto.resource('s3')
s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

# Collect bucket
bucket = s3_resource.Bucket("noaa-ghe-pds")

# Collect all data from S3 and insert nonzero values into MySQL database
def collect_data():
	insert_count = 0
	total_inserts = 0

	year = "2020"
	months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

	for month in months:
		for i in range(1,32):
			day = str(i)

			if (i < 10):
				day = "0" + day

			print("------")
			print(f"COLLECTING FOR {month}/{day}")

			for file in bucket.objects.filter(Prefix=f"rain_rate/2020/{month}/{day}"):
				time_start = time.perf_counter()

				# This stores the date and time to be used in the database
				timestamp = file.last_modified

				buffer = BytesIO(file.get()["Body"].read())
				dataset_new = nc.Dataset('none.nc', 'w')

				with gzip.open(buffer, 'rb') as f:
					file_content = f.read()
					dataset_new = nc.Dataset('TEMP', memory=file_content)

				# Create Pandas dataframe to store only the region corresponding to Africa
				rainfall_array = dataset_new['rain']
				dataframe = pd.DataFrame(rainfall_array[923:3876, 4453:6541])

				dataframe.to_csv(f'data/2020/{timestamp}.csv')

				time_end = time.perf_counter()
				print(f"LAST FILE TOOK {time_end - time_start:0.4f} SECONDS.")
				print(f"INSERTS - {total_inserts}")

collect_data()

# Commit pending inserts
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()
