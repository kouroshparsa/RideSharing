import os
from app.models.model import Rider, Driver
from app.database import SessionLocal
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from fastapi import APIRouter

router = APIRouter()

session = SessionLocal()

SECRET_KEY = os.getenv("SECRET_KEY")
# use secrets.token_hex(16)
if SECRET_KEY is None:
    raise Exception("Missing SECRET_KEY. It must be present in the environment variables.")

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email,
                "name": "{} {}".format(payload.get("first_name", ""), payload.get("last_name", "")),
                "id": payload.get("id")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")



@router.post("/token/{user_type}")
async def login_for_access_token(user_type: str, form_data: OAuth2PasswordRequestForm = Depends()):
    userClass = Rider
    if user_type.lower() == "driver":
        userClass = Driver
        
    user = session.query(userClass).filter_by(email=form_data.username).first()
    if user is None or not verify_password(form_data.password, user.pass_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "id": user.id}
    access_token = create_access_token(
        data=data, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
