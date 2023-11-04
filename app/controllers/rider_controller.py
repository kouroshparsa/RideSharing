"""
This module has the controllers used from riders' app
"""
import os
from fastapi import APIRouter
from fastapi import HTTPException, Depends
import redis
from app.models.model import Driver
from app.database import SessionLocal
from app.controllers import cost_calculator
from app.controllers.auth_controller import get_current_user
from app.utils import geo_helper
from app.dto.driver import DriverStatus
from app.dto.trip import TripCandidate, Trip, VehicleType, TripStatus

router = APIRouter()

session = SessionLocal()

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"),
                           port=os.getenv("REDIS_PORT"), decode_responses=True)

@router.get("/trip_candidates")
async def get_trip_candidates(trip: Trip,
               user: dict = Depends(get_current_user)):

    drivers = session.query(Driver).filter(
        Driver.location.ST_Distance(
            f"SRID=4326;POINT({trip.origin.longitude} {trip.origin.latitude})"
            ) <= 10000  # 10 kilometers in meters
        ).order_by(
            Driver.location.ST_Distance(
                f"SRID=4326;POINT({trip.origin.longitude} {trip.origin.latitude})"
            )
        ).all() # by default is is ascending (smallest first)

    candidates = []
    uuid = uuid.uuid4().hex
    for driver in drivers:
        price = cost_calculator.get_cost(trip.origin, trip.destination, driver.vehicle_type)
        vtype = VehicleType(driver.vehicle_type).name
        booking_id = f'{driver.id}_{user["id"]}_{uuid}'
        candidates.append(TripCandidate(driver.id, price, vtype, driver.rating, booking_id=booking_id))
        trip.booking_id = booking_id
        trip.price = price
        trip.status = TripStatus.Pending
        redis_client.set(booking_id, os.getenv("REDIS_EXPIRY"), trip.model_dump(mode="json"))
    return candidates


@router.get("/address_to_geolocation/{address}")
async def get_geo_location(address: str,
               user: dict = Depends(get_current_user)):
    return geo_helper.get_coord_from_address(address)

@router.get("/driver/{driver_id}")
async def get_driver(driver_id: int,
               user: dict = Depends(get_current_user)):
    res = session.query(Driver).filter(Driver.id == driver_id).first()
    return {"status": res.status, "status_name": DriverStatus(res.status).name, "location": res.location}


def update_dirver_requests(driver_id: int, trip: Trip):
    driver_reqs = redis_client.get(str(driver_id))
    if driver_reqs is None:
        driver_reqs = [trip]
    else:
        driver_reqs.append(trip)
    redis_client.set(str(driver_id), os.getenv("REDIS_EXPIRY"), driver_reqs)


@router.patch("/book/{booking_id}")
async def book_driver(booking_id: str,
               user: dict = Depends(get_current_user)):

    trip_dict = redis_client.get(booking_id)
    if trip_dict is None:
        raise HTTPException(status_code=404, detail="The booking request is not found.")

    trip_dict['booking_id'] = booking_id
    trip: Trip = Trip.model_validate(trip_dict)
    update_dirver_requests(trip.driver_id, trip)


@router.get("/booking/{booking_id}")
async def get_booking_request_status(booking_id: str,
                      user: dict = Depends(get_current_user)):

    booking = redis_client.get(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="The booking request is not found.")
    return {"status": TripStatus(booking['status']).name}
