import pandas as pd
from math import sqrt, pow

lat_requested = -6.85
long_requested = 34.24

def closest_distance(df, latitude, longitude): #closest distance algorithm
    
    dictionary_for_points = {}
    #arrays start at zero lol, csv's don't. -> 0-1842, and 0-14
    for i in range(1843):
        lat = df.iloc[i].iloc[2]
        long = df.iloc[i].iloc[3]
        diff_lat = abs(lat - latitude)
        diff_long = abs(long- longitude)
        dictionary_for_points[i] = diff_lat + diff_long

    closest_point = min(dictionary_for_points.values())
    point_key = list(dictionary_for_points.keys())[list(dictionary_for_points.values()).index(closest_point)]
    lat = df.iloc[point_key].iloc[2]
    long = df.iloc[point_key].iloc[3]
    ssn = df.iloc[point_key].iloc[0]

    #find distance. 
    vertical_distance = abs(lat-latitude) * 69 #convert to miles
    horizontal_distance = abs(long-longitude) * 53
    total_distance = sqrt(pow(vertical_distance,2) + pow(horizontal_distance,2))
    if total_distance > 100:# 100 miles arbitrary distance for good and bad. 
        indicator= "bad" 
    else:
        indicator = "good"

    return [ssn,lat,long, indicator ]

def find_soil_ph(lat, long):
    path = "georeferences.csv"
    temp_dataframe = pd.read_csv(path)
    closest_distance_array = closest_distance(temp_dataframe, lat,long)
    ssn = closest_distance_array[0]

    path_to_ph = "Wet_Chemistry_CROPNUTS.csv"
    ph_dataframe = pd.read_csv(path_to_ph)
    for i in range(1908):
        found_ssn = ph_dataframe.iloc[i].iloc[0]
        if ssn == found_ssn:
            return ph_dataframe.iloc[i].iloc[17]
    return 

