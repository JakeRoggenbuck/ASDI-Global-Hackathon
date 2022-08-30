'''

NOTES
The idea behind this method is to
(1) Add up all of the rates over the course of the day
(2) Normalize (find the average) over the course of the day
(3) Remove all zeroes from the table (replace with NaN)
(4) Export CSV file for each day, and upload to some other cloud service

The result is that
- The CSV size unzipped is reduced from 200 MB full to 20 MB Africa to 10-15 MB w/o zeroes to 2 MB as a gzip
- Then, files can THEORETICALLY be retrieved and processed faster from some online source

PROBLEMS
- Where to store files
- It'll still take around two seconds per file, which means the user would still have to wait around 
  fifteen minutes for the data to be collected and analyzed with the statistical model

POTENTIAL SOLUTION
- Lambda / Amazon Elastic File System (EFS) could possibly be used to perform the data collection
  through the cloud and store the processed files on EFS, and then read locally when procesing
  data for the statistical model to use (should be way faster for clients)

'''

import netCDF4 as nc
import pandas as pd
import boto3 as boto
import numpy as np

from botocore.handlers import disable_signing
from io import BytesIO
import time
import gzip

# Disable signing to access S3 bucket without credentials
s3_resource = boto.resource('s3')
s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

# Collect bucket
bucket = s3_resource.Bucket("noaa-ghe-pds")

def collect_data():
	insert_count = 0
	total_inserts = 0

	year = "2020"
	months = ["01"]

	for month in months:
		for i in range(12,32):
			day = str(i)

			if (i < 10):
				day = "0" + day

			print("------")
			print(f"COLLECTING FOR {month}/{day}")

			# Initialize empty DataFrame
			sum_dataframe = pd.DataFrame()
			sum_count = 0

			for file in bucket.objects.filter(Prefix=f"rain_rate/2020/{month}/{day}"):
				time_start = time.perf_counter()

				# Stores date and time that the file was created
				timestamp = file.last_modified

				buffer = BytesIO(file.get()["Body"].read())
				dataset_new = nc.Dataset('none.nc', 'w')

				with gzip.open(buffer, 'rb') as f:
					file_content = f.read()
					dataset_new = nc.Dataset('TEMP', memory=file_content)

				# Create Pandas dataframe to store only the region corresponding to Africa
				rainfall_array = dataset_new['rain']
				temp_dataframe = pd.DataFrame(rainfall_array[923:3876, 4453:6541])

				if (sum_dataframe.shape[0] == 0):
					sum_dataframe = temp_dataframe
				else:
					sum_dataframe = sum_dataframe.add(temp_dataframe, fill_value=0)

				sum_count += 1

				time_end = time.perf_counter()
				print(f"LAST FILE TOOK {time_end - time_start:0.4f} SECONDS.")
			
			sum_dataframe = sum_dataframe.div(sum_count)
			sum_dataframe.to_csv(f'data/2020/2020{month}{day}_norm.csv')

collect_data()
