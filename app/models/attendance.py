
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "attendance_date",
            name="unique_employee_attendance"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    attendance_date = Column(Date, nullable=False)

    check_in = Column(DateTime(timezone=True), nullable=True)

    check_out = Column(DateTime(timezone=True), nullable=True)

    total_hours = Column(Numeric(5, 2), default=0)

    status = Column(String(20), default="present", nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
