from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str  # On peut se connecter avec username ou email
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    java_level: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pour SQLAlchemy


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None