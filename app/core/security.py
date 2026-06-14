#sab authentication aur authorization se related functions yaha aayo
from datetime import datetime , timedelta
from jose import JWTError , jwt 
from passlib.context import CryptContext
from app.core.config import settings
from typing import Optional

pw_context = CryptContext(schemes =["bcrypt"], deprecated= "auto")

def hash_password(password:str) ->str:
    return pw_context.hash(password[:72])

def verify_password(plain:str , hashed:str)->bool:
    return pw_context.verify(plain[:72] , hashed)

def create_access_token(data:dict, expires_delta :Optional[timedelta] = None ) ->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire })
    if "type" not in to_encode :
        to_encode["type"] = "access"
    return jwt.encode(to_encode , settings.SECRET_KEY , algorithm = settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token:str) -> dict:
    try:
        return jwt.decode(token , settings.SECRET_KEY , algorithms = [settings.ALGORITHM])
    except JWTError:
        return None
