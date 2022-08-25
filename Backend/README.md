# Backend

# API Layout

- `/`
	- {"Hello": "World"}

- `/timeframe`
	- Get the timeframe of the data that we have.

- `/plant-request`
	- Lat
	- Lon
	- Time start
	- Time end

	{
		"latitude": float,
		"longitude": float,
		"start": string,
		"end": string,
	}

	Return
	- Best crops (as many) in IDs
	- Some specific data
		- Soil pH
		- Rain in some unit
		- Confidence Level

	{
		"crops": [int, int],
		"soil_ph": float,
		"conf_lvl": float,
	}
