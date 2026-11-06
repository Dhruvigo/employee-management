from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_admin, require_employee
from app.schemas.leave import (
    LeaveCreate,
    LeaveStatusUpdate,
    LeaveResponse
)

from app.services import leave as leave_service


router = APIRouter(
    prefix="/api/leaves",
    tags=["Leave Management"]
)


# 1. ADMIN: CREATE LEAVE
@router.post(
    "/",
    response_model=LeaveResponse,
    status_code=201,
    dependencies=[Depends(require_admin)]
)
def create_leave(
    data: LeaveCreate,
    db: Session = Depends(get_db)
):
    try:
        return leave_service.create_leave(db, data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 2. ADMIN: GET ALL LEAVES
@router.get("/",response_model=list[LeaveResponse],dependencies=[Depends(require_admin)])
def get_leaves(employee_id: int = None,status: str = None,db: Session = Depends(get_db)):
    
    return leave_service.get_leaves(
        db,
        employee_id=employee_id,
        status=status
    )


# 3. ADMIN: APPROVE OR REJECT LEAVE
@router.put(
    "/{leave_id}/status",
    response_model=LeaveResponse
)
def update_leave_status(
    leave_id: int,
    data: LeaveStatusUpdate,
    current_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        leave = leave_service.update_leave_status(
            db,
            leave_id,
            data.status,
            admin_id=current_user.id
        )

        if not leave:
            raise HTTPException(
                status_code=404,
                detail="Leave request not found"
            )

        return leave

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 4. EMPLOYEE: APPLY FOR LEAVE
@router.post("/my-leaves",response_model=LeaveResponse,status_code=201)

def apply_my_leave(
    data: LeaveCreate,
    current_user=Depends(require_employee),
    db: Session = Depends(get_db)
):
    data = data.model_copy(
        update={"employee_id": current_user.employee_id}
    )

    try:
        return leave_service.create_leave(db, data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 5. EMPLOYEE: GET MY LEAVES
@router.get(
    "/my-leaves",
    response_model=list[LeaveResponse]
)
def my_leaves(
    current_user=Depends(require_employee),
    db: Session = Depends(get_db)
):
    return leave_service.get_leaves(
        db,
        employee_id=current_user.employee_id
    )