
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from fastapi import HTTPException
from app.models.department import Department
from sqlalchemy.orm import joinedload

# 1. CREATE EMPLOYEE
# 1. CREATE EMPLOYEE
def create_employee(db: Session, employee_data: EmployeeCreate):

    # Validate department before creating employee
    validate_department(db, employee_data.department_id)

    new_employee = Employee(**employee_data.model_dump())

    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return new_employee

    except IntegrityError:
        db.rollback()
        raise ValueError("Employee code or email already exists")


# 2. GET ALL EMPLOYEES WITH SEARCH AND PAGINATION
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
        query = query.filter(Employee.status == status)

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
def get_employee_by_id(db, employee_id):

    employee = (
        db.query(Employee)
        .options(joinedload(Employee.department_record))
        .filter(Employee.id == employee_id)
        .first()
    )

    return employee


# 4. UPDATE EMPLOYEE
def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):

    employee = get_employee_by_id(db, employee_id)

    if not employee:
        return None

    update_data = employee_data.model_dump(exclude_unset=True)

    # Validate department only when department_id is supplied
    if "department_id" in update_data:
        validate_department(db, update_data["department_id"])

    for key, value in update_data.items():
        setattr(employee, key, value)

    try:
        db.commit()
        db.refresh(employee)

        return employee

    except IntegrityError:
        db.rollback()
        raise ValueError("Employee code or email already exists")


# 5. DELETE EMPLOYEE
def delete_employee(db: Session, employee_id: int):

    employee = get_employee_by_id(db, employee_id)

    if not employee:
        return False

    db.delete(employee)
    db.commit()

    return True


def validate_department(db, department_id):
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