
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.dependencies import require_admin
from app.database import get_db

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)

from app.services import department as department_service


router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"],
    dependencies=[Depends(require_admin)]
)


# 1. CREATE DEPARTMENT
@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=201
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):

    try:
        return department_service.create_department(
            db,
            department
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


# 2. GET ALL DEPARTMENTS
@router.get(
    "/",
    response_model=list[DepartmentResponse]
)
def get_departments(
    search: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):

    return department_service.get_all_departments(
        db=db,
        search=search,
        status=status,
        page=page,
        limit=limit
    )


# 3. GET DEPARTMENT BY ID
@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    department = department_service.get_department_by_id(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# 4. UPDATE DEPARTMENT
@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db)
):

    try:
        department = department_service.update_department(
            db,
            department_id,
            department_data
        )

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        return department

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


# 5. DELETE DEPARTMENT
@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    try:
        deleted = department_service.delete_department(
            db,
            department_id
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        return {
            "success": True,
            "message": "Department deleted successfully"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )
