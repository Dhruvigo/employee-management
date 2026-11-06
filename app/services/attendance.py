
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.attendance import Attendance
from app.models.employee import Employee
from sqlalchemy import func

TIMEZONE = ZoneInfo("Asia/Kolkata")


# 1. CHECK IN
def check_in(db: Session, employee_id: int):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise ValueError("Employee not found")

    now = datetime.now(TIMEZONE)

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=now.date(),
        check_in=now,
        status="present"
    )

    try:
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance

    except IntegrityError:
        db.rollback()
        raise ValueError("Employee already checked in today")


# 2. CHECK OUT
def check_out(db: Session, employee_id: int):

    today = datetime.now(TIMEZONE).date()

    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance:
        raise ValueError("Please check in first")

    if attendance.check_out:
        raise ValueError("Already checked out")

    now = datetime.now(TIMEZONE)

    attendance.check_out = now

    hours = (
        now - attendance.check_in
    ).total_seconds() / 3600

    attendance.total_hours = round(hours, 2)

    # Example attendance policy
    if hours < 4:
        attendance.status = "half_day"
    else:
        attendance.status = "present"

    db.commit()
    db.refresh(attendance)

    return attendance


# 3. GET ATTENDANCE RECORDS
def get_attendance_records(
    db: Session,
    employee_id: int = None,
    attendance_date=None
):

    query = db.query(Attendance)

    if employee_id is not None:
        query = query.filter(
            Attendance.employee_id == employee_id
        )

    if attendance_date is not None:
        query = query.filter(
            Attendance.attendance_date == attendance_date
        )

    return query.order_by(
        Attendance.attendance_date.desc()
    ).all()

def get_monthly_report(db: Session, year: int, month: int):

    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")

    records = db.query(
        Attendance.employee_id,
        Attendance.status,
        func.count(Attendance.id).label("total_days"),
        func.sum(Attendance.total_hours).label("total_hours")
    ).filter(
        func.extract("year", Attendance.attendance_date) == year,
        func.extract("month", Attendance.attendance_date) == month
    ).group_by(
        Attendance.employee_id,
        Attendance.status
    ).all()

    return [
        {
            "employee_id": record.employee_id,
            "status": record.status,
            "total_days": record.total_days,
            "total_hours": float(record.total_hours or 0)
        }
        for record in records
    ]