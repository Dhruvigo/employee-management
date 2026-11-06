from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_admin, require_employee
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.services import attendance as attendance_service


router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance"]
)


# 1. ADMIN CHECK IN
@router.post("/check-in", response_model=AttendanceResponse,
             dependencies=[Depends(require_admin)])
def check_in(
    data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    try:
        return attendance_service.check_in(db, data.employee_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 2. ADMIN CHECK OUT
@router.post("/check-out", response_model=AttendanceResponse,
             dependencies=[Depends(require_admin)])
def check_out(
    data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    try:
        return attendance_service.check_out(db, data.employee_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 3. ADMIN ATTENDANCE RECORDS
@router.get("/", response_model=list[AttendanceResponse],
            dependencies=[Depends(require_admin)])
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


# 4. ADMIN MONTHLY REPORT
@router.get("/monthly-report",
            dependencies=[Depends(require_admin)])
def monthly_report(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db)
):
    return attendance_service.get_monthly_report(db, year, month)


# 5. EMPLOYEE SELF CHECK IN
@router.post("/my-check-in", response_model=AttendanceResponse)
def my_check_in(
    current_user=Depends(require_employee),
    db: Session = Depends(get_db)
):
    try:
        return attendance_service.check_in(
            db, current_user.employee_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 6. EMPLOYEE SELF CHECK OUT
@router.post("/my-check-out", response_model=AttendanceResponse)
def my_check_out(
    current_user=Depends(require_employee),
    db: Session = Depends(get_db)
):
    try:
        return attendance_service.check_out(
            db, current_user.employee_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 7. EMPLOYEE OWN ATTENDANCE RECORDS
@router.get("/my-records", response_model=list[AttendanceResponse])
def my_attendance_records(
    current_user=Depends(require_employee),
    db: Session = Depends(get_db)
):
    return attendance_service.get_attendance_records(
        db,
        employee_id=current_user.employee_id
    )