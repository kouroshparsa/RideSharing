import os
import requests
from math import radians, sin, cos, sqrt, atan2
from app import logger


API_KEY = os.getenv("GOOGLE_API_KEY")

def get_coord_from_address(address: str):
    """
    returns a dict with longitude and latitude in degrees
    """
    API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': API_KEY
    }

    # Sending a request to Google Geocoding API
    response = requests.get(API_URL, params=params, timeout=2)# timeout is in seconds
    data = response.json()

    # Extracting latitude and longitude if the request was successful
    if data['status'] == 'OK':
        loc = data['results'][0]['geometry']['location']
        return {"longitude": loc["lng"], "latitude": loc["lat"]}

    if 'error_message' in data:
        logger.error(data['error_message'])
    return None


def get_driving_distance(origin: str, destination: str):
    """
    Latitude,Longitude
    returns driving distance in meters
    """
    API_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": API_KEY
    }

    # Sending a request to Google Geocoding API
    response = requests.get(API_URL, params=params, timeout=2)# timeout is in seconds
    data = response.json()

    if data['status'] == 'OK':
        if len(data['rows']) > 0 and \
            len(data['rows'][0]['elements']) > 0 and \
            'distance' in data['rows'][0]['elements'][0]:
            return data['rows'][0]['elements'][0]['distance']['value']
    
    if 'error_message' in data:
        logger.error(data['error_message'])
    return None

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    returns the distance in Km
    """
    # Radius of the Earth in kilometers
    R = 6371.0 # Km

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calculate the change in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance
