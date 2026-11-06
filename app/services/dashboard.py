
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.department import Department
from app.models.attendance import Attendance


TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_dashboard_summary(db: Session):

    today = datetime.now(TIMEZONE).date()

    total_employees = db.query(Employee).count()

    active_employees = db.query(Employee).filter(
        Employee.status == "active"
    ).count()

    total_departments = db.query(Department).count()

    present = db.query(Attendance).filter(
        Attendance.attendance_date == today,
        Attendance.status == "present"
    ).count()

    half_day = db.query(Attendance).filter(
        Attendance.attendance_date == today,
        Attendance.status == "half_day"
    ).count()

    checked_in = db.query(Attendance).filter(
        Attendance.attendance_date == today,
        Attendance.check_in.isnot(None),
        Attendance.check_out.is_(None)
    ).count()

    absent = max(
        active_employees - present - half_day,
        0
    )

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "total_departments": total_departments,
        "present_today": present,
        "half_day_today": half_day,
        "absent_today": absent,
        "currently_checked_in": checked_in
    }
