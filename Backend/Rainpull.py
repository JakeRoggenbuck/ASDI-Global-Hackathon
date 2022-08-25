import netCDF4 as nc
import pandas as pd
import boto3
from io import BytesIO
import gzip
import numpy as np



from botocore.handlers import disable_signing


s3_resource = boto3.resource('s3')
s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)



# def collect_data():
#     year = "2020"
#     month = "01"

#     for i in range(1,32):
#         day = str(i)

#         if (i < 10):
#             day = "0" + day

#         date_file=f"2020{month}{day}"
#         date_path=f"2020/{month}/{day}"

#         key=f"rain_rate/{date_path}/NPR.GEO.GHE.v1.S{date_file}0000.nc.gz"

#         zip_obj = s3_resource.Object(bucket_name="noaa-ghe-pds", key=key)
#         buffer = BytesIO(zip_obj.get()["Body"].read())

#         dataset_new = nc.Dataset('none.nc', 'w')

#         with gzip.open(buffer, 'rb') as f:
#             file_content = f.read()
#             dataset_new = nc.Dataset('TEMP', memory=file_content)

#         rainfall_array = dataset_new['rain']

#         dataframe = pd.DataFrame(rainfall_array[923:3876, 4453:6541])
#         dataframe.to_csv(f'africa-rainfall/{date_file}.csv')

#         print(key)



# collect_data()

# Requested coordinates
lat_requested = -0.6229166667
long_requested = -18.32335329

def read_data():
    month = "01"
    year = "2020"

    for i in range(1,2): #still downloads all?
        day = str(i)

        if (i < 10):
            day = "0" + day

        date_file=f"2020{month}{day}"
        path = f"africa-rainfall/{date_file}.csv"

        temp_dataframe = pd.read_csv(path)
        retrieve_data(temp_dataframe, lat_requested, long_requested)


def retrieve_data(df, latitude, longitude):
    # Both are now validated! Next, correct lat. and long. to begin at zero
    lat_corrected = 65 - latitude
    long_corrected = longitude + 180

    # Convert coordinates into indexes (reminder - latitude is y, longitude is x)
    # TODO - Look into proper rounding (up/down)

    lat_index = round((4800.0 / 130) * lat_corrected - 923) - 2
    long_index = round((10020.0 / 360) * long_corrected - 4453) +1

    print("LAT INDEX = " + str(round(lat_index)))
    print("LONG INDEX = " + str(round(long_index)))

    print(df.iloc[lat_index].iloc[long_index])

#in the dataframe, the labels are not included so we need to subtract one from horz and two from vert
#might need to account for the csv printing the headers label when comparing to the actual 2d array. Or maybe because csv start at 1 and array start at 0.
# TODO , check this against the actual array and see if we are printing the right thing.
# TODO, check the conversion of the index to distance, between every margin of +- 0.5 of that index, refer to it - wait, don't need to worry about this because 'round' does it for us. Probably just something interesting to write about.
# TODO, take average of rainfall after verifying this is true.

read_data()
