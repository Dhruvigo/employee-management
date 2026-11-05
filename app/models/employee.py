
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime
from sqlalchemy.sql import func

from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    employee_code = Column(String(20), unique=True, nullable=False)

    first_name = Column(String(100), nullable=False)

    last_name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    phone = Column(String(20), nullable=True)

    department = Column(String(100), nullable=True)

    designation = Column(String(100), nullable=True)

    salary = Column(Numeric(10, 2), nullable=True)

    joining_date = Column(Date, nullable=True)

    status = Column(String(20), default="active")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )

    department_record = relationship(
        "Department",
        back_populates="employees"
    )