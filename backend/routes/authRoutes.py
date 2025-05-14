from datetime import datetime, timedelta, timezone
from http.client import HTTPException

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from database.dbHelper import get_db_connection
from helpers.returnResult import return_result
from models.auth import Token
from typing import Optional
from bson.objectid import ObjectId
import jwt
import os

router = APIRouter(prefix="/auth")

client = get_db_connection()
db = client.Shorklights.Users
roles_db = client.Shorklights.Roles

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "OwO")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"}
    )

permissions_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"}
    )

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

async def get_admin_user(current_user: tuple = Depends(get_current_user)):
    role_id=ObjectId(current_user["role_id"])
    role = roles_db.find_one({"_id": role_id})
    if role["name"] != "shork":
        raise permissions_exception
    return current_user

async def get_authentificated_user(current_user: tuple = Depends(get_current_user)):
    role_id=ObjectId(current_user["role_id"])
    role = roles_db.find_one({"_id": role_id})
    if role["name"] not in ["shork", "member"]:
        raise permissions_exception
    return current_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        return return_result(False, message="Incorrect username or password", status_code=401)

    role_id = user["role_id"]
    if not isinstance(role_id, ObjectId):
        role_id = ObjectId(role_id)
    role = roles_db.find_one({"_id": role_id})

    role_name = role["name"]

    access_token = create_access_token(
        data={"sub": user["username"], "role": role_name})

    response = {"access_token": access_token, "token_type": "bearer"}
    return return_result(True, data=response, message="Authentifcation successful")
