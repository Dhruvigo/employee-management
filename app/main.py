import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine
from app.routers.employee import router as employee_router
from app.routers.department import router as department_router
from app.routers.auth import router as auth_router

load_dotenv()

app = FastAPI(
    title=os.getenv(
        "APP_NAME",
        "Employee Management System"
    ),
    version="1.0.0"
)

# Register API routers
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(auth_router)

@app.get("/")
def home():

    return {
        "success": True,
        "message": "Employee Management System API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "OK",
        "message": "Python FastAPI application is working"
    }


@app.get("/health/database")
def database_health():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "success": True,
            "database": "PostgreSQL",
            "message": "Database connected successfully"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )