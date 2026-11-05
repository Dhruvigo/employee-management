# Employee Management System

A RESTful Employee Management System built using **Python, FastAPI, PostgreSQL, and SQLAlchemy**. The application provides employee and department management, database migrations, user management, and JWT-based authentication.

## 🚀 Technologies Used

- **Backend:** Python 3, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Database Migrations:** Alembic
- **Data Validation:** Pydantic
- **Authentication:** JWT (JSON Web Token)
- **Password Security:** Argon2 password hashing
- **API Documentation:** Swagger UI
- **Development Tools:** VS Code, Postman, pgAdmin

## ✨ Features

### 1. Employee Management
- Create new employees.
- View employee details.
- Update employee information.
- Delete employees.
- Search and filter employees.
- Manage employee status.
- Assign employees to departments.

### 2. Department Management
- Create departments.
- View department details.
- Update department information.
- Delete departments.
- Manage department status.
- View employees associated with departments.

### 3. User Management
- Create user accounts.
- Store user information securely.
- Hash passwords before saving them.
- Manage user records.

### 4. JWT Authentication
- User registration.
- User login.
- Password verification.
- Generate JWT access tokens.
- Verify JWT tokens.
- Set token expiration.
- Retrieve logged-in user details.

## 📁 Project Structure

```text
employee-management/
│
├── app/
│   ├── core/
│   │   ├── dependencies.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── employee.py
│   │   ├── department.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── employee.py
│   │   ├── department.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── employee.py
│   │   ├── department.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── employee.py
│   │   ├── department.py
│   │   └── auth.py
│   │
│   ├── database.py
│   └── main.py
│
├── migrations/
│   └── versions/
│
├── .env
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Dhruvigo/employee-management.git
```

### 2. Navigate to the Project

```bash
cd employee-management
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/employee_management

SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the database password and secret key with your own values.

### 7. Create PostgreSQL Database

Create a database named:

```text
employee_management
```

### 8. Run Database Migrations

```bash
python -m alembic upgrade head
```

### 9. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.

**Swagger UI:**

http://127.0.0.1:8000/docs

**ReDoc:**

http://127.0.0.1:8000/redoc

## 🔐 Authentication

The application uses JWT-based authentication.

### Register User

```http
POST /api/auth/register
```

Example request:

```json
{
  "name": "Rahul Patel",
  "email": "rahul@example.com",
  "password": "Rahul@123"
}
```

### Login User

```http
POST /api/auth/login
```

Example request:

```json
{
  "email": "rahul@example.com",
  "password": "Rahul@123"
}
```

The login endpoint returns an access token.

Use the token in the Authorization header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Get Logged-in User

```http
GET /api/auth/me
```

## 🗄️ Database Migrations

This project uses Alembic to manage database schema changes.

Create a migration:

```bash
python -m alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
python -m alembic upgrade head
```

Check current migration:

```bash
python -m alembic current
```

View migration history:

```bash
python -m alembic history
```

## 🧪 Testing

Use Swagger UI or Postman to test the API endpoints.

Test the following operations:

- Employee CRUD
- Department CRUD
- Employee-Department relationship
- User registration
- User login
- JWT token generation
- Authenticated user details

## 🔒 Security Notes

- Passwords are stored as hashes, not plain text.
- JWT tokens have an expiration time.
- Database credentials must be stored in `.env`.
- Never commit `.env` or your secret key to GitHub.
- Use `.gitignore` to exclude virtual environments and sensitive files.

## 👨‍💻 Developer

**GitHub:** [Dhruvigo](https://github.com/Dhruvigo)

**Repository:** [Employee Management System](https://github.com/Dhruvigo/employee-management)

## 📄 License

This project is developed for learning and development purposes.
