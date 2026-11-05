
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Literal
from app.schemas.department import EmployeeDepartmentResponse
from pydantic import BaseModel, ConfigDict, Field ,EmailStr
#schema for employee data validation and serialization using Pydantic
#schemas are used to define the structure and validation rules for the data that is sent and received by the API endpoints.

class EmployeeCreate(BaseModel):

    employee_code: str = Field(min_length=2, max_length=20)

    first_name: str = Field(min_length=2, max_length=100)

    last_name: str = Field(min_length=2, max_length=100)

    email: EmailStr = Field(max_length=150)

    phone: Optional[str] = Field(default=None, max_length=20)

    department: Optional[str] = Field(default=None, max_length=100)

    designation: Optional[str] = Field(default=None, max_length=100)

    salary: Optional[Decimal] = Field(default=None, ge=0)

    joining_date: Optional[date] = None

    status: Literal["active", "inactive"] = "active"
    department_id: Optional[int] = None


class EmployeeUpdate(BaseModel):

    employee_code: Optional[str] = Field(default=None, min_length=2, max_length=20)

    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)

    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)

    email: Optional[str] = Field(default=None, max_length=150)

    phone: Optional[str] = Field(default=None, max_length=20)

    department: Optional[str] = Field(default=None, max_length=100)

    designation: Optional[str] = Field(default=None, max_length=100)

    salary: Optional[Decimal] = Field(default=None, ge=0)

    joining_date: Optional[date] = None

    status: Optional[Literal["active", "inactive"]] = None
    department_id: Optional[int] = None


class EmployeeResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_code: str
    first_name: str
    last_name: str
    email: str

    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[Decimal] = None
    joining_date: Optional[date] = None

    status: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    department_id: Optional[int] = None
    department_record: Optional[EmployeeDepartmentResponse] = None