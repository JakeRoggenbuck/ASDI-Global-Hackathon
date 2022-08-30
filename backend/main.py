from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime, timedelta
import pandas as pd
import boto3
import uvicorn
import yaml
import gzip

with open("./config.yml") as file:
    config = yaml.safe_load(file)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

session = boto3.Session(
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
)

s3_resource = session.resource('s3')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "crops": str,   16 def plant_request(pl_req: PlantRequest):


    }
    """

    crops: list[int]
    soil_ph: float
    conf_lvl: float


def plant_request(pl_req: PlantRequest):
    rains = []

    time = pl_req.start

    file = f"2020/{str(time.month).zfill(2)}/{2020}{str(time.month).zfill(2)}{str(time.day).zfill(2)}.csv.gz"

    buck = s3_resource.Bucket("rainfall-normalized")
    a = buck.download_file(file, "tmp/file.csv.gz")

    with gzip.open("tmp/file.csv.gz", 'rb') as f:
        with open("tmp/file.csv", "wb") as file:
            file.write(f.read())

    df = pd.read_csv("tmp/file.csv")

    rain = df.iloc[int(pl_req.latitude)].iloc[int(pl_req.longitude)]

    rains.append(
        {
            "text": f"The rain at lat={pl_req.latitude}, lon={pl_req.longitude} is {rain} on {time}",
            "plants": ["corn", "soybean", "moringa"],
        }
    )

    return rains


@app.get("/")
def read_root():
    return {"Hello": "Plant Here!"}


@app.get("/timeframe")
def read_timeframe():
    """Get the timeframe of the data that we have."""
    return {
        "start": datetime(2020, 1, 1),
        "end": datetime(2022, 1, 1),
    }


@app.post("/plant-request")
def read_plant_request(pl_req: PlantRequest):
    return plant_request(pl_req)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
