
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

from sqlalchemy.exc import IntegrityError
from app.models.employee import Employee



def register_user(user_data, db: Session):

    if db.query(User).filter(User.email == user_data.email).first():
        raise ValueError("Email already exists")

    try:
        # Create employee record
        new_employee = Employee(
            employee_code="EMP-" + str(db.query(Employee).count() + 1).zfill(4),
            first_name=user_data.name.split(" ")[0],
            last_name=" ".join(user_data.name.split(" ")[1:]) or "-",
            email=user_data.email,
            status="active"
        )

        db.add(new_employee)
        db.flush()

        # Create user account
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            employee_id=new_employee.id,
            role="employee",
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()
        raise ValueError("Employee or User already exists")


# Login User
def authenticate_user(email: str, password: str, db: Session):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    return user
