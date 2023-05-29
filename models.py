from datetime import datetime
from database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.sql import text
from sqlalchemy.orm import Mapped


class Post(Base):
    __tablename__ = "posts"

    id: Mapped["int"] = Column(Integer, primary_key=True, index=True)  # type: ignore
    title: Mapped["str"] = Column(String, nullable=False)  # type: ignore
    content: Mapped["str"] = Column(String)  # type: ignore
    published: Mapped["bool"] = Column(Boolean, server_default=text("false"))  # type: ignore
    created_at: Mapped["datetime"] = Column(TIMESTAMP(timezone=True), server_default=text("now()"))  # type: ignore


class User(Base):
    __tablename__ = "users"

    id: Mapped["int"] = Column(Integer, primary_key=True, index=True)  # type: ignore
    email: Mapped["str"] = Column(String, nullable=False, unique=True)  # type: ignore
    password: Mapped["str"] = Column(String)  # type: ignore
    created_at: Mapped["datetime"] = Column(TIMESTAMP(timezone=True), server_default=text("now()"))  # type: ignore
