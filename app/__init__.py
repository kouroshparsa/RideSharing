"""
Do not load view at the top because they pull controllers which need db to be set up
"""
from dotenv import load_dotenv
from fastapi import FastAPI
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger()
load_dotenv()
from app import database # import after loading environment variable

def create_app():
    """ initializes the app and registers routes """
    print('create_app...')
    app = FastAPI()
    from app.controllers import rider_controller, driver_controller, auth_controller
    app.include_router(rider_controller.router)
    app.include_router(driver_controller.router)
    app.include_router(auth_controller.router)
    return app
