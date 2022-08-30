import requests
import json
from time import sleep
import pandas as pd

def script_for_nutrients(food):
   
    api_key="api_key=2Ma3nUPBcSGR8K7S6mzSjffqKZagXbSGu8ejFvDD"
    url = "https://api.nal.usda.gov/fdc/v1/foods/search?"
    params = f"&query={food}"
    results = requests.get(url+ api_key+params)
    try:
        while results.status_code != 200:
            sleep(15)
            results = requests.get(url+api_key+params)
        results_json = results.json()
        print(results_json["foods"][0]["description"])
        food_nutrients = results_json["foods"][0]["foodNutrients"]
        sought_out_nutrients = ["Protein", "Energy", "Carbohydrate, by difference", "Fiber, total dietary", "Fatty acids, total trans"]
        nutrient_values = []
        for nutrients in food_nutrients:
            for sought_nutrients in sought_out_nutrients:
                if sought_nutrients == nutrients["nutrientName"]:
                    nutrient_values.append([nutrients["nutrientName"], nutrients["value"], nutrients['unitName'] ])
    
    #JSONDecodeError happens when request response is empty: this is the case if the database cannot find the requested nutrient. Therefore we must catch it.  
    #IndexError occurs when we call the 
    except json.JSONDecodeError and IndexError:
        nutrient_values = []
    return nutrient_values


def add_nutrients_to_spreadsheet():
    path ="plant-ph.csv"
    temp_dataframe = pd.read_csv(path)
    
    for x in range(5):
        dataframe = []
        nutrients = ["Protein", "Energy", "Carbohydrate, by difference", "Fiber, total dietary", "Fatty acids, total trans"]
        for i in range(43):
            nutrient_values = script_for_nutrients(temp_dataframe.iloc[i].iloc[0])

            #making sure it exists. 
            try:
                dataframe.append(str(nutrient_values[x][1])+ nutrient_values[x][2])
            except IndexError:
                dataframe.append('')

        if nutrients[x] == "Protein":
            temp_dataframe["protein"] = dataframe
        elif nutrients[x] == "Energy":
            temp_dataframe["energy"] = dataframe
        elif nutrients[x] == "Carbohydrate, by difference":
            temp_dataframe["carbohydrates"] = dataframe
        elif nutrients[x] == "Fiber, total dietary":
            temp_dataframe["fibre"] = dataframe
        elif nutrients[x] == "Fatty acids, total trans":
            temp_dataframe["fattyacids"] = dataframe

        temp_dataframe.to_csv("plants.csv")
add_nutrients_to_spreadsheet()
