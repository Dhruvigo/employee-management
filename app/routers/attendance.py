
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_admin
from fastapi import Query

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse
)

from app.services import attendance as attendance_service


router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance"],
    dependencies=[Depends(require_admin)]
)


# 1. CHECK IN
@router.post("/check-in", response_model=AttendanceResponse)
def check_in(
    data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    try:
        return attendance_service.check_in(
            db, data.employee_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 2. CHECK OUT
@router.post("/check-out", response_model=AttendanceResponse)
def check_out(
    data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    try:
        return attendance_service.check_out(
            db, data.employee_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 3. ATTENDANCE RECORDS
@router.get("/", response_model=list[AttendanceResponse])
def get_attendance(
    employee_id: int = None,
    attendance_date: date = None,
    db: Session = Depends(get_db)
):
    return attendance_service.get_attendance_records(
        db,
        employee_id=employee_id,
        attendance_date=attendance_date
    )


@router.get("/monthly-report")
def monthly_report(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db)
):
    return attendance_service.get_monthly_report(
        db,
        year,
        month
    )