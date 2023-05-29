from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from datetime import datetime, timedelta
from typing import Annotated

from database import DB
from config import settings
import schemas
import models

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return schemas.TokenPayload(**payload)
    except:
        return None


async def get_current_user(db: DB, token: str = Depends(oauth2_scheme)):
    token_payload = verify_access_token(token)
    if token_payload is None:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    stmt = select(models.User).where(models.User.id == token_payload.user_id)
    user_model = db.execute(stmt).scalar_one_or_none()
    if user_model is None:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return user_model


User = Annotated[models.User, Depends(get_current_user)]
