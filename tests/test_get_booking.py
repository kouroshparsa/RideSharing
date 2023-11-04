import httpx
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import create_app
from app.dto.trip import TripStatus
from app.controllers.auth_controller import get_current_user
app = create_app()

async def override_dependency(q: str | None = None):
    return {}

@patch('app.controllers.rider_controller.redis_client.get')  # Mock the Redis client
def test_get_booking_request_status_unauthorized(mock_get):
    # Configure the mock to return the expected data
    mock_get.return_value = {"status": TripStatus.Accepted}

    # Create a test client using your FastAPI app
    client = TestClient(app)

    # Define the booking_id you want to test
    booking_id = "12345"

    # Make a GET request to the endpoint
    response = client.get(f"/booking/{booking_id}")

    # Assert unauthorized response:
    assert response.status_code == 401


@patch('app.controllers.rider_controller.redis_client.get')  # Mock the Redis client
def test_get_booking_request_status(mock_get):
    # Configure the mock to return the expected data
    mock_get.return_value = {"status": TripStatus.Accepted}

    # Create a test client using your FastAPI app
    client = TestClient(app)
    app.dependency_overrides[get_current_user] = override_dependency # ignore dependency check

    # Define the booking_id you want to test
    booking_id = "12345"

    # Make a GET request to the endpoint
    response = client.get(f"/booking/{booking_id}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response content matches the expected data
    assert response.json() == {"status": TripStatus.Accepted.name}
