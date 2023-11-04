"""
This module has the controllers used from drivers' app
"""
import os
from datetime import datetime
from app.models.model import Driver
from app.database import SessionLocal
from app.controllers.auth_controller import get_current_user
from app.dto.driver import Location
from app.dto.trip import Trip, TripStatus
from app.controllers.producers import location_monitoring, payment_processing
from fastapi import HTTPException, Depends
from fastapi import APIRouter
import redis

router = APIRouter()
redis_client = redis.Redis(host=os.getenv("REDIS_HOST"),
                           port=os.getenv("REDIS_PORT"), decode_responses=True)
session = SessionLocal()


@router.get("/driver_requests")
async def get_driver_requests(user: dict = Depends(get_current_user)):
    """ drivers call this to get their requests """
    driver_id = user["id"]
    reqs = redis_client.get(str(driver_id))
    if reqs is None:
        reqs = []
    return reqs


@router.post("/accept_booking/{booking_id}")
async def accept_booking(booking_id: str,
                      user: dict = Depends(get_current_user)):
    """ drivers call this to accept a booking """
    booking = redis_client.get(booking_id)
    trip: Trip = Trip.model_validate(booking)
    trip.status = TripStatus.Accepted
    redis_client.set(booking_id, os.getenv("REDIS_EXPIRY"), booking)
    session.query(Driver).\
        filter(Driver.id == trip.driver_id).\
        update({'status': TripStatus.Accepted})
    session.commit()


@router.post("/reject_booking/{booking_id}")
async def reject_booking(booking_id: str,
                      user: dict = Depends(get_current_user)):
    """ drivers call this to reject a booking """
    driver_id = user["id"]
    reqs = redis_client.get(str(driver_id))
    reqs = [req for req in reqs if req["booking_id"] != booking_id]
    redis_client.set(booking_id, os.getenv("REDIS_EXPIRY"), reqs)


@router.patch("/pickedup/{driver_id}")
async def pickedup(driver_id: int,
                      user: dict = Depends(get_current_user)):
    """
    update booking status on redis
    update driver status in db
    trigger payment processing
    """

    # update the cache:
    booking_id = None
    driver_reqs = redis_client.get(str(driver_id))
    if driver_reqs is not None:
        booking_id = None
        for req in driver_reqs:
            req = Trip.model_validate(req)
            if req.status == TripStatus.Accepted:
                booking_id = req.booking_id
                break

    if booking_id is None:
        raise HTTPException(status_code=401, detail="???")

    booking = redis_client.get(booking_id)
    if booking is None:
        raise HTTPException(status_code=401, detail="???")

    trip = Trip.model_validate(booking)
    trip.status = TripStatus.Accepted
    redis_client.set(booking_id, os.getenv("REDIS_EXPIRY"), trip.model_dump(mode="json"))

    driver_amount = trip.amount * (1.0 - os.getenv("SERVICE_CHARGE"))
    payment_processing.send_driver_earning(driver_id, driver_amount, datetime.now())
    payment_processing.send_rider_payment(trip.rider_id, trip.id, datetime.now())

@router.patch("/driver/{driver_id}")
async def update_driver_location(driver_id: int,
                                 location: Location,
                                 user: dict = Depends(get_current_user)):
    """ drivers continuously send their location here """
    location_monitoring.update_location(driver_id, location)
