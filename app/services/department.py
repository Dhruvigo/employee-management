
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate
)


# 1. CREATE DEPARTMENT
def create_department(
    db: Session,
    department_data: DepartmentCreate
):

    new_department = Department(
        **department_data.model_dump()
    )

    try:
        db.add(new_department)
        db.commit()
        db.refresh(new_department)

        return new_department

    except IntegrityError:
        db.rollback()
        raise ValueError("Department name already exists")


# 2. GET ALL DEPARTMENTS
def get_all_departments(
    db: Session,
    search: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10
):

    query = db.query(Department)

    if search:
        query = query.filter(
            Department.name.ilike(f"%{search}%")
        )

    if status:
        query = query.filter(
            Department.status == status
        )

    offset = (page - 1) * limit

    return (
        query.order_by(Department.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


# 3. GET DEPARTMENT BY ID
def get_department_by_id(
    db: Session,
    department_id: int
):

    return db.query(Department).filter(
        Department.id == department_id
    ).first()


# 4. UPDATE DEPARTMENT
def update_department(
    db: Session,
    department_id: int,
    department_data: DepartmentUpdate
):

    department = get_department_by_id(
        db,
        department_id
    )

    if not department:
        return None

    update_data = department_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(department, key, value)

    try:
        db.commit()
        db.refresh(department)

        return department

    except IntegrityError:
        db.rollback()
        raise ValueError("Department name already exists")


# 5. DELETE DEPARTMENT
def delete_department(db, department_id):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    if department.employees:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete department with assigned employees"
        )

    db.delete(department)
    db.commit()

    return {"message": "Department deleted successfully"}
