
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.leave import Leave
from app.models.employee import Employee
from app.schemas.leave import LeaveCreate


# 1. CREATE LEAVE REQUEST
def create_leave(db: Session, data: LeaveCreate):

    employee = db.query(Employee).filter(
        Employee.id == data.employee_id
    ).first()

    if not employee:
        raise ValueError("Employee not found")

    leave = Leave(**data.model_dump())

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave


# 2. GET LEAVE REQUESTS
def get_leaves(db: Session, employee_id=None, status=None):

    query = db.query(Leave)

    if employee_id is not None:
        query = query.filter(Leave.employee_id == employee_id)

    if status:
        query = query.filter(Leave.status == status)

    return query.order_by(Leave.id.desc()).all()


# 3. APPROVE OR REJECT LEAVE
def update_leave_status(db: Session, leave_id, status, admin_id):

    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()

    if not leave:
        return None

    if leave.status != "pending":
        raise ValueError("Leave request already reviewed")

    leave.status = status
    leave.reviewed_by = admin_id
    leave.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(leave)

    return leave
