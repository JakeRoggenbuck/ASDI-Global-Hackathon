
import pandas as pd
from analysis import entry
import datetime

sample_input = [11, 8.2, "2021-05-21 11:22:03", "2021-09-21 11:22:03"]
def main(input):
    lat, long, start, stop = input[0], input[1], input[2], input[3]
    #rainfall function with start and stop and long for total rainfall. 
    soil_ph = entry(lat,long).find_soil_ph()
    predicted_rainfall = 500 #replace with rain_fall_function(datetime_object, datetime_object)
    path = "plants.csv"
    dataframe = pd.read_csv(path)
    valid_ph = []
    valid = {}

    #loop through and find the PH that are within the range. 
    for i in range(43):
        ph_bot,ph_up = dataframe.iloc[i].iloc[2].split('-')
        if float(ph_bot) < soil_ph and float(ph_up) > soil_ph:
            print(ph_bot, ph_up, soil_ph)
            valid_ph.append(i)

    #loop through and match the valid PH with valid rainfall too
    for i in valid_ph:
        rain_bot,rain_up = dataframe.iloc[i].iloc[3].split('-')
        if int(rain_bot)< predicted_rainfall and int(rain_up) > predicted_rainfall:
            valid[i]= dataframe.iloc[i].iloc[1]
    
    # return the names of crops
    return list(valid.values())

#trial delete this when actually putting it in. 
main(sample_input)