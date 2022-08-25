from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()


class PlantRequest(BaseModel):
    latitude: float
    longitude: float


def plant_request(pl_req: PlantRequest):
    return f"{pl_req.latitude=} {pl_req.longitude=}"


@app.get("/")
def read_root():
    return {"Hello": "Plant Here!"}


@app.post("/plant-request")
def read_plant_request(pl_req: PlantRequest):
    return plant_request(pl_req)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
