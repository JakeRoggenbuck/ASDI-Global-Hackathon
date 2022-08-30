# Backend

## API Routes

`/` -> Return `{ "Hello" : "World" }`

`/timeframe` -> Return the time frame for which we have data

`/plant-request` -> Request will include latitude, longitude, starting date, and ending date, and response will include the best crops to plant as IDs, soil pH, rainfall, and confidence level.

### Request
Step 1. By clicking on a map, users can select the place with which they live/are able to plant their crops. 

Step 2. Next, they can select the time frame. <br/>
		The system will find the total rainfall in the period, then match it with the required rainfall for the crops and return the ones that fulfill this requirement.
. 

Step 3. OPTIONAL: Finally, the user can choose to filter. Food insecurity comes in many forms, whether that be a deprivation of necessary caloric intake, protein deficiency, lack of healthy fats etc. Therefore, our application allows users to filter the crops to return the ones that best suites their nutritional needs. 
		
		If they do: the system will return a SORTED LIST of crops that are highest in the requested category (e.g Protein) that meet the requirements for soil PH and Rainfall.

		Else : they system will return ALL the crops that meet the requirements for soil PH and Rainfall. 

```
{
	"latitude": float,
	"longitude": float,
	"start_date": string,
	"end_date": string,
	"filter" : string
}
```

### Response
```
{
	"crops": [int, ..., int],
	"soil_ph": float,
	"confidence": float,
}
```
