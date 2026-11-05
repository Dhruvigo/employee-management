from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Literal
from app.schemas.department import EmployeeDepartmentResponse
from pydantic import BaseModel, ConfigDict, Field ,EmailStr

class UserBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=150)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=150)
    password: str = Field(..., min_length=8, max_length=255)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"