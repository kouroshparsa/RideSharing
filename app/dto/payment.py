from pydantic import BaseModel
from datetime import datetime

class RiderPayment(BaseModel):
    rider_id: int
    amount: float
    payment_date: datetime

class DriverEarning(BaseModel):
    driver_id: int
    amount: float
    earning_date: datetime