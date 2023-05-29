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
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.post("", status_code=201)
async def create_post(
    post: schemas.PostCreate,
    db: DB,
    user_model: Annotated[models.User, Depends(oauth2.get_current_user)],
) -> schemas.PostResponse:
    stmt = insert(models.Post).values(**post.dict()).returning(models.Post)
    post_model = db.execute(stmt).scalar_one()
    return post_model


@router.get("/{id}")
async def get_post(id: int, db: DB) -> schemas.PostResponse:
    stmt = select(models.Post).where(models.Post.id == id)
    post_model = db.execute(stmt).scalar_one_or_none()
    if post_model is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_model


@router.get("")
async def get(db: DB) -> Sequence[schemas.PostResponse]:
    post_models = db.execute(select(models.Post)).scalars().all()
    return post_models


@router.put("/{id}", status_code=200)
async def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: DB,
    user_model: Annotated[models.User, Depends(oauth2.get_current_user)],
) -> schemas.PostResponse:
    stmt = (
        update(models.Post)
        .where(models.Post.id == id)
        .values(**post.dict())
        .returning(models.Post)
    )
    post_model = db.execute(stmt).scalar_one_or_none()
    if post_model is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.commit()
    return post_model


@router.delete("/{id}", status_code=204)
async def delete_post(
    id: int,
    db: DB,
    user_model: Annotated[models.User, Depends(oauth2.get_current_user)],
):
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return None
