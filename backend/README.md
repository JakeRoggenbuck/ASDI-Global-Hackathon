# Backend

## API Routes

`/` -> Return `{ "Hello" : "World" }`

`/timeframe` -> Return the time frame for which we have data

`/plant-request` -> Request will include latitude, longitude, starting date, and ending date, and response will include the best crops to plant as IDs, soil pH, rainfall, and confidence level.

### Request
```
{
	"latitude": float,
	"longitude": float,
	"start_dtae": string,
	"end_date": string,
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
