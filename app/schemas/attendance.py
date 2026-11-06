
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AttendanceCreate(BaseModel):
    employee_id: int


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    check_in: datetime | None = None
    check_out: datetime | None = None
    total_hours: Decimal | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)
