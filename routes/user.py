from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.responses import RedirectResponse
from psycopg2.extras import RealDictCursor
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
import psycopg2

from typing import Annotated, Sequence
import time

from database import DB
import models
import schemas
import utils


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", status_code=201)
async def create_user(user: schemas.UserCreate, db: DB) -> schemas.UserResponse:
    user_create_dict = user.dict()
    user_create_dict["password"] = utils.hash_password(user_create_dict["password"])
    stmt = insert(models.User).values(**user_create_dict).returning(models.User)
    user_model = db.execute(stmt).scalar_one()
    db.commit()
    return user_model


@router.get("/{id}")
async def get_user(id: int, db: DB) -> schemas.UserResponse:
    stmt = select(models.User).where(models.User.id == id)
    user_model = db.execute(stmt).scalar_one_or_none()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_model


@router.get("")
async def get_users(db: DB) -> Sequence[schemas.UserResponse]:
    user_models = db.execute(select(models.User)).scalars().all()
    return user_models
