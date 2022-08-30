import pandas as pd
from tqdm import tqdm
import numpy as np
import os

with open("all_data.csv", "w") as file:

    for l in os.listdir("../data/csvs/"):
        df = pd.read_csv("../data/csvs/" + l)

        df = df.fillna(0)

        lon, lat = df.shape
        for x in tqdm(range(lon)):
            content = ""
            for y in range(lat):
                rain = df.iloc[x].iloc[y]
                date = l.split(".")[0]
                content += f"{x},{y},{rain},{date}\n"

            file.write(content)
