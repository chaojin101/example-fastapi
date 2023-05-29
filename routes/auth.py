from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from database import DB
import models
import schemas
import utils
import oauth2

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
    *, user_credentials: OAuth2PasswordRequestForm = Depends(), db: DB
) -> schemas.TokenResponse:
    stmt = select(models.User).where(models.User.email == user_credentials.username)
    user_model = db.execute(stmt).scalar_one_or_none()
    if user_model is None:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user_model.password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    token_payload = schemas.TokenPayload(user_id=user_model.id).dict()
    access_token = oauth2.create_access_token(data=token_payload)
    return schemas.TokenResponse(access_token=access_token, token_type="bearer")
