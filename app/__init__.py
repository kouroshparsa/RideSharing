"""
Do not load view at the top because they pull controllers which need db to be set up
"""
from fastapi import FastAPI
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger()
from dotenv import load_dotenv
load_dotenv()

def create_app():
    print('create_app...')
    app = FastAPI()
    from app import database
    print('db is set up')
    from app.controllers import rider_controller, driver_controller, auth_controller
    app.include_router(rider_controller.router)
    app.include_router(driver_controller.router)
    app.include_router(auth_controller.router)
    return app
