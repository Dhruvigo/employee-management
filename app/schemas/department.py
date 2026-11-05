
from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    status: Literal["active", "inactive"] = "active"


class DepartmentUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    status: Optional[Literal["active", "inactive"]] = None


class DepartmentResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    status: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class EmployeeDepartmentResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)