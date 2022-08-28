from datetime import date, timedelta
from queue import Queue
from threading import Thread
from dataclasses import dataclass

import boto3 as boto
import netCDF4 as nc
import pandas as pd
import numpy as np
import time
import gzip

from botocore.handlers import disable_signing
from io import BytesIO

# Disable signing to access S3 bucket without credentials
s3_resource = boto.resource('s3')
s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

# Establish bucket
bucket = s3_resource.Bucket("noaa-ghe-pds")

def producer(queue):
    # Change these depending on which years and months you would like to collect
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    year = "2020"

    for month in months:
        minimum_days = 19
        maximum_days = 32

        for i in range(minimum_days, maximum_days):
            day = str(i)

            if (i < 10):
                day = "0" + day

            path_data = {
                "month": month,
                "day": day
            }

            queue.put(path_data)

def consumer(queue):
    while True:
        if queue.empty():
            break

        path_data = queue.get()

        try:
            sum_dataframe = pd.DataFrame()
            sum_count = 0

            print(f"--- PROCESSING FOR 2020/{path_data['month']}/{path_data['day']} ---")
            dataset_new = "TEMP"

            for file in bucket.objects.filter(Prefix=f"rain_rate/2020/{path_data['month']}/{path_data['day']}"):
                timestamp = file.last_modified
                print("File timestamp - " + str(timestamp))

                buffer = BytesIO(file.get()["Body"].read())
                
                with gzip.open(buffer, 'rb') as f:
                    file_content = f.read()
                    dataset_new = nc.Dataset('TEMP', memory=file_content)

                # Create Pandas DataFrame to store only the region corresponding to Africa
                rainfall_array = dataset_new['rain']
                temp_dataframe = pd.DataFrame(rainfall_array[923:3876, 4453:6541])

                # Either initialize sum_dataframe or add the newest collected data to it
                if (sum_dataframe.shape[0] == 0):
                    sum_dataframe = temp_dataframe
                else:
                    sum_dataframe = sum_dataframe.add(temp_dataframe, fill_value=0)

                sum_count += 1

            # Divide by the number of files collected to find the day's rainfall averages
            sum_dataframe = sum_dataframe.div(sum_count)

            # Remove measurements less than 0.05 mm and round all values to four decimal points
            sum_dataframe[sum_dataframe < 0.05] = np.nan
            sum_dataframe = sum_dataframe.round(decimals = 4)

            # Export to CSV
            sum_dataframe.to_csv(f"normalized_data/2020{path_data['month']}{path_data['day']}.csv")

        except Exception as exception:
            if "Could not connect to the endpoint URL" in str(exception):
                print("--- AWS S3 THROTTLING - WAIT ONE MINUTE ---")
                time.sleep(60)
            else:
                print(exception) 

def main():
    print("--- MAIN STARTED ---")

    queue = Queue()
    producer(queue)

    threads = []

    for _ in range(8):
        consumer_thread = Thread(
            target=consumer,
            args=(queue,),
            daemon=True,
        )

        threads.append(consumer_thread)
        consumer_thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    time_start = time.perf_counter()

    main()

    time_end = time.perf_counter()
    print(f"SCRIPT TOOK {time_end - time_start:0.4f} SECONDS TO COMPLETE.")
