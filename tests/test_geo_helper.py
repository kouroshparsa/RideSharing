import json
from unittest.mock import patch
from requests.models import Response
from app.utils.geo_helper import get_coord_from_address, get_driving_distance

def mocked_requests_get(*args, **kwargs):
    response_content = None
    request_url = args[0]
    if request_url == "https://maps.googleapis.com/maps/api/geocode/json":
        response_content = {"status": "OK",
                            "results": [
                                    {
                                        "geometry": {
                                            "location": {"lng": 1.1, "lat": 2.2}
                                        }
                                    }
                                ]
                            }
    elif request_url == "https://maps.googleapis.com/maps/api/distancematrix/json":
        response_content = {"status": "OK",
                            "rows": [
                                    {"elements": [
                                        {"distance": {"value": 100}}
                                    ]}
                                ]
                            }

    response = Response()
    response.status_code = 200
    response._content = str.encode(json.dumps(response_content))
    return response


@patch('app.utils.geo_helper.requests.get', side_effect=mocked_requests_get)
def test_get_coord_from_address(mock_get):
    res = get_coord_from_address("address")
    assert res == {"longitude": 1.1, "latitude": 2.2}


@patch('app.utils.geo_helper.requests.get', side_effect=mocked_requests_get)
def test_get_driving_distance(mock_get):
    res = get_driving_distance("origin", "destination")
    assert res == 100