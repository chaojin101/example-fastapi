from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


class PostBase(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool = True


class PostCreate(PostBase):
    title: str
    content: str


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    title: str
    content: str
    published: bool

    id: int
    created_at: float = Field(description="Unix Timestamp: 1685246631.588908")

    @validator("created_at", pre=True)
    def convert_datetime_to_timestamp(cls, v: datetime):
        return v.timestamp()

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserResponse(UserBase):
    email: EmailStr

    id: int
    created_at: float = Field(description="Unix Timestamp: 1685246631.588908")

    @validator("created_at", pre=True)
    def convert_datetime_to_timestamp(cls, v: datetime):
        return v.timestamp()

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int
