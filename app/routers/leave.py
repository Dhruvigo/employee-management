
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_admin

from app.schemas.leave import (
    LeaveCreate,
    LeaveStatusUpdate,
    LeaveResponse
)

from app.services import leave as leave_service


router = APIRouter(
    prefix="/api/leaves",
    tags=["Leave Management"],
    dependencies=[Depends(require_admin)]
)


# 1. CREATE LEAVE
@router.post("/", response_model=LeaveResponse, status_code=201)
def create_leave(
    data: LeaveCreate,
    db: Session = Depends(get_db)
):
    try:
        return leave_service.create_leave(db, data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# 2. GET LEAVES
@router.get("/", response_model=list[LeaveResponse])
def get_leaves(
    employee_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    return leave_service.get_leaves(
        db,
        employee_id=employee_id,
        status=status
    )


# 3. APPROVE OR REJECT LEAVE
@router.put("/{leave_id}/status", response_model=LeaveResponse)
def update_leave_status(
    leave_id: int,
    data: LeaveStatusUpdate,
    db: Session = Depends(get_db)
):
    try:
        leave = leave_service.update_leave_status(
            db,
            leave_id,
            data.status,
            admin_id=1
        )

        if not leave:
            raise HTTPException(
                status_code=404,
                detail="Leave request not found"
            )

        return leave

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
