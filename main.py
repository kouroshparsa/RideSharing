import uvicorn
# from app.controllers import rider_controller, driver_controller, auth_controller

from app import create_app
app = create_app()

# app.include_router(rider_controller.router)
# app.include_router(driver_controller.router)
# app.include_router(auth_controller.router)
# @app.get("/api/payment/{id}")
# def get_payment(id: int):
#     return driver_controller.get_payment(id)


# class CustomerStatus(BaseModel):
#     email: str
#     active: bool

# @app.post("/api/customer")
# def set_customer_status(data: CustomerStatus):
#     return driver_controller.set_customer_status(data.email, data.active)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)