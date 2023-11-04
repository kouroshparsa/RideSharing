from pydantic import BaseModel


class UpdateCustomer(BaseModel):
    email: str
    active: bool
