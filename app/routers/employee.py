
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.dependencies import require_admin
from app.database import get_db

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)

from app.services import employee as employee_service


router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"],
    dependencies=[Depends(require_admin)]
)


# 1. CREATE EMPLOYEE
@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    try:
        return employee_service.create_employee(db, employee)

    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


# 2. GET ALL EMPLOYEES
@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
    search: str | None = None,
    department: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return employee_service.get_all_employees(
        db=db,
        search=search,
        department=department,
        status=status,
        page=page,
        limit=limit
    )


# 3. GET EMPLOYEE BY ID
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = employee_service.get_employee_by_id(db, employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# 4. UPDATE EMPLOYEE
@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated_employee = employee_service.update_employee(
            db, employee_id, employee
        )

        if not updated_employee:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return updated_employee

    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


# 5. DELETE EMPLOYEE
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    deleted = employee_service.delete_employee(db, employee_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "success": True,
        "message": "Employee deleted successfully"
    }
