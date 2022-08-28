# Rainfall Data Collection
One challenge we faced during this project was the large quantity of rainfall data stored on the original AWS S3 bucket, with around ninety 200 MB files for every day of the year. Our solution was to download this data automatically using a Python script, normalizing the rainfall measurements over the course of every day, and reuploading the normalized data for every day as a relatively small .csv file on our own S3 bucket.

## Data Description
Every day on the NOAA Global Hydration Estimator bucket is represented by around ninety .nc files, each reporting estimates fifteen minutes apart. An .nc dataset is essentially a large 2D array, with rows representing latitude degrees and columns representing longitude degrees.

According to the navigation files provided on the NOAA GHE bucket, we know that latitude is measured from +65 to -65 degrees, and that longitude is measured from -180 to +180 degrees. Using some basic math, we found approximately how many degrees every row (of which there are around 4800) and column (of which there are around 10020) represents.

Using this math, we found what row/column indices represented the region containing Africa, and isolated only that data from the file.

## Script Description
The included script downloads every file for every day, adds them all together, and divides by the total number of files for that day to find the day's rainfall average. This is saved to a CSV file. These files were uploaded manually to our personal AWS S3 bucket, and are retrieved by the server in a similar fashion.

Because the code employs concurrency, the data download and processing is much faster than if files were retrieved one at a time - in fact, it's seven times as fast because the script creates seven threads!

This script was run overnight on two computers to collect all of the data.

## Running Instructions
Before running the script, make sure to create a directory called `normalized_data`. Then, you can run the script using `python -m multithreaded_download`.