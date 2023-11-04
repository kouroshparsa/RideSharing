from app.dto.trip import Location, VehicleType
from app.utils import geo_helper

def get_tax(loc: Location) -> float:
    """ returns the tax rate in decimal (%5 would be 0.05)
    """
    return 0.05 # TODO fetch from cache, if not in cache then from database

def get_price_per_meter(vehicleType: VehicleType)-> float:
    """ returns the cost of the ride excluding taxes per meter
    """
    return 0.2220 # TODO fetch from cache, if not in cache then from database

def get_cost(origin: Location, destination: Location, vehicleType: VehicleType) -> float:
    distance = geo_helper.get_driving_distance(origin, destination)
    if distance is None:
        return None
    price_per_meter = get_price_per_meter(vehicleType)
    price = distance * price_per_meter
    price = price * (1 + get_tax(origin))
    return price