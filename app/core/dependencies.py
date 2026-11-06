from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import verify_access_token
from fastapi import Depends, HTTPException

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(credentials.credentials)

    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return user

def require_admin(current_user: User = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required"
        )

    return current_user

def require_employee_or_admin(
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["employee", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user


def require_employee(
    current_user = Depends(get_current_user)
):
    if current_user.role != "employee":
        raise HTTPException(
            status_code=403,
            detail="Employee access required"
        )

    if not current_user.employee_id:
        raise HTTPException(
            status_code=403,
            detail="No employee record linked to this account"
        )

    return current_user