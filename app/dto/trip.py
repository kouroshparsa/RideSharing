from pydantic import BaseModel
from typing import Optional
from dataclasses import dataclass
from enum import IntEnum

class VehicleType(IntEnum):
    EcoRide = 0
    ComfortRide = 1
    GreenRide = 2
    ExtraLargeRide = 3
    SharedRide = 4


class Location(BaseModel):
    longitude: float
    latitude: float

class TripStatus(IntEnum):
    Pending = 0
    Accepted = 1
    PickedUp = 2

class Trip(BaseModel):
    origin: Location
    destination: Location
    origin_address: str
    destination_address: str
    price: Optional[float] = None
    status: Optional[TripStatus] = TripStatus.Pending
    driver_id: Optional[int] = None
    rider_id: Optional[int] = None
    booking_id: Optional[int] = None

@dataclass
class TripCandidate:
    driver_id: int
    price: float
    vehicle_type: VehicleType
    rating: float
    booking_id: str
