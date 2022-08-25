from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI()


class PlantRequest(BaseModel):
    """
    {
        "latitude": float,
        "longitude": float,
        "start": string,
        "end": string,
    }
    """

    latitude: float
    longitude: float
    start: datetime
    end: datetime


class PlantReturn(BaseModel):
    """
    {
        "crops": [int, int],
        "soil_ph": float,
        "conf_lvl": float,
    }
    """
    crops: list[int]
    soil_ph: float
    conf_lvl: float


def plant_request(pl_req: PlantRequest):
    return f"{pl_req.latitude=} {pl_req.longitude=}"


@app.get("/")
def read_root():
    return {"Hello": "Plant Here!"}


@app.get("/timeframe")
def read_timeframe():
    """Get the timeframe of the data that we have."""
    return {
        "start": datetime(2021, 1, 1),
        "end": datetime(2050, 1, 1),
    }


@app.post("/plant-request")
def read_plant_request(pl_req: PlantRequest):
    return plant_request(pl_req)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
