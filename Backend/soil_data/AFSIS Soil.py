import pandas as pd

lat_requested = -0.6229166667
long_requested = -18.32335329

def retrieve_data(df, latitude, longitude): #closest distance algorithm

    lat_dict = {}
    long_dict = {}
    print(df.iloc[1842].iloc[2]) #arrays start at zero lol, csv's don't.
    for i in range(1843):
        lat = df.iloc[i].iloc[2]
        long = df.iloc[i].iloc[3]
        diff_lat = abs(lat - latitude)
        diff_long = abs(long-longitude)
        lat_dict[lat] = diff_lat
        long_dict[long] = diff_long

    closest_lat= min(lat_dict.values())
    closest_long = min(long_dict.values())

    lat = list(lat_dict.keys())[list(lat_dict.values()).index(closest_lat)]
    long = list(long_dict.keys())[list(long_dict.values()).index(closest_long)]

    print(lat,long)

path = "georeferences.csv"

temp_dataframe = pd.read_csv(path)
retrieve_data(temp_dataframe, lat_requested, long_requested)
