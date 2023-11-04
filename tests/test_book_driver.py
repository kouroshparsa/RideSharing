import httpx
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import create_app
from app.dto.trip import TripStatus, Trip
from app.controllers.auth_controller import get_current_user
app = create_app()

async def override_dependency(q: str | None = None):
    return {}

@patch('app.controllers.rider_controller.redis_client.get')  # Mock the Redis client
def test_book_driver_unauthorized(mock_get):
    # Configure the mock to return the expected data
    mock_get.return_value = {"status": TripStatus.Accepted}

    # Create a test client using your FastAPI app
    client = TestClient(app)

    # Define the booking_id you want to test
    booking_id = "12345"
    response = client.patch(f"/book/{booking_id}")

    # Assert unauthorized response:
    assert response.status_code == 401


@patch('app.controllers.rider_controller.redis_client.get')  # Mock the Redis client
def test_book_driver_invalid_booking_id(mock_get):
    # Configure the mock to return the expected data
    mock_get.return_value = None # the booking id is not in redis

    # Create a test client using your FastAPI app
    client = TestClient(app)
    app.dependency_overrides[get_current_user] = override_dependency # ignore dependency check

    # Define the booking_id you want to test
    booking_id = "12345"
    response = client.patch(f"/book/{booking_id}")

    # Assert invalid input response:
    assert response.status_code == 404


@patch('app.controllers.rider_controller.redis_client.get')  # Mock the Redis client
def test_book_driver(mock_get):
    # Configure the mock to return the expected data
    booking_id = "12345"
    trip = Trip(origin={"longitude": 1, "latitude": 1},
                destination={"longitude": 1, "latitude": 1},
                origin_address="",
                destination_address="",
                price=20.0, status=TripStatus.Pending, booking_id=booking_id)
    mock_get.return_value = [trip.model_dump(mode="json")]

    # Create a test client using your FastAPI app
    client = TestClient(app)
    app.dependency_overrides[get_current_user] = override_dependency # ignore dependency check

    response = client.patch(f"/book/{booking_id}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200