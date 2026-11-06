
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.employee import Employee
from app.models.department import Department
from app.models.user import User

from app.schemas.employee import EmployeeCreate, EmployeeUpdate

from app.core.security import hash_password


# 1. CREATE EMPLOYEE + USER
def create_employee(db: Session, employee_data: EmployeeCreate):

    validate_department(db, employee_data.department_id)

    data = employee_data.model_dump()
    password = data.pop("password")

    try:
        # Create employee
        new_employee = Employee(**data)

        db.add(new_employee)
        db.flush()

        # Automatically create login user
        new_user = User(
            name=f"{new_employee.first_name} {new_employee.last_name}",
            email=new_employee.email,
            hashed_password=hash_password(password),
            employee_id=new_employee.id,
            role="employee",
            is_active=True
        )

        db.add(new_user)

        db.commit()
        db.refresh(new_employee)

        return new_employee

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Employee code or email already exists"
        )


# 2. GET ALL EMPLOYEES WITH SEARCH, FILTER, SORT AND PAGINATION
def get_all_employees(
    db: Session,
    search: str = None,
    department_id: int = None,
    status: str = None,
    sort_by: str = "id",
    order: str = "asc",
    page: int = 1,
    limit: int = 10
):

    query = db.query(Employee).options(
        joinedload(Employee.department_record)
    )

    # Search
    if search:
        query = query.filter(
            or_(
                Employee.first_name.ilike(f"%{search}%"),
                Employee.last_name.ilike(f"%{search}%"),
                Employee.email.ilike(f"%{search}%"),
                Employee.employee_code.ilike(f"%{search}%")
            )
        )

    # Department filter
    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    # Status filter
    if status:
        query = query.filter(
            Employee.status == status
        )

    # Sorting
    sort_columns = {
        "id": Employee.id,
        "name": Employee.first_name,
        "salary": Employee.salary,
        "joining_date": Employee.joining_date
    }

    if sort_by not in sort_columns:
        raise ValueError("Invalid sort field")

    if order not in ["asc", "desc"]:
        raise ValueError("Invalid sort order")

    column = sort_columns[sort_by]

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    # Pagination
    total = query.count()

    employees = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "employees": employees
    }


# 3. GET EMPLOYEE BY ID
def get_employee_by_id(db: Session, employee_id: int):

    return (
        db.query(Employee)
        .options(joinedload(Employee.department_record))
        .filter(Employee.id == employee_id)
        .first()
    )


# 4. UPDATE EMPLOYEE + SYNCHRONIZE USER EMAIL
def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):

    employee = get_employee_by_id(db, employee_id)

    if not employee:
        return None

    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    # Validate department
    if "department_id" in update_data:
        validate_department(
            db,
            update_data["department_id"]
        )

    try:
        # Update employee fields
        for key, value in update_data.items():
            setattr(employee, key, value)

        # Update linked login account email
        if "email" in update_data:
            user = db.query(User).filter(
                User.employee_id == employee_id
            ).first()

            if user:
                user.email = update_data["email"]

        db.commit()
        db.refresh(employee)

        return employee

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Employee code or email already exists"
        )


# 5. DELETE EMPLOYEE + LINKED USER
def delete_employee(db: Session, employee_id: int):

    employee = get_employee_by_id(db, employee_id)

    if not employee:
        return False

    try:
        # Find linked user
        user = db.query(User).filter(
            User.employee_id == employee_id
        ).first()

        # Delete user first
        if user:
            db.delete(user)

        # Delete employee
        db.delete(employee)

        db.commit()

        return True

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Unable to delete employee"
        )


# 6. VALIDATE DEPARTMENT
def validate_department(db: Session, department_id: int):

    if department_id is None:
        return

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )
