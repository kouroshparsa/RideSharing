from pydantic import BaseModel
from enum import IntEnum

class DriverStatus(IntEnum):
    Offline = 0
    Available = 1
    Accepted = 2
    InTransit = 3

class Location(BaseModel):
    longitude: float
    latitude: float
