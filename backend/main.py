from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
import uvicorn

from main_file import main

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
        "crops": str,
        
    }
    """
    crops: list[str]
    


def plant_request(pl_req: PlantRequest):
    response = main([pl_req.latitude, pl_req.longitude,pl_req.start, pl_req.end ])
    return response

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
