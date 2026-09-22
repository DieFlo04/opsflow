# OpsFlow — IT Operations & Automation Platform

OpsFlow is a web-based IT operations platform designed to centralize incident management, automate operational analysis, and provide useful metrics for IT teams.

The project was developed as a portfolio project focused on backend development, REST APIs, database management, authentication, role-based access control, automated testing, and data-driven operational analysis.

---

## 🚀 Features

### 🔐 Authentication & Security

* User authentication with JWT.
* Password hashing using Argon2.
* Protected API endpoints.
* Role-Based Access Control (RBAC).
* User roles:

  * Admin
  * Technician
  * Employee
* Current authenticated user endpoint.
* Protected incident operations.

### 🛠️ Incident Management

OpsFlow provides complete incident management functionality:

* Create incidents.
* View incident details.
* Update incidents.
* Delete incidents according to user permissions.
* Assign incidents.
* Change incident status.
* Define incident priority.
* Associate incidents with systems and categories.
* Search incidents.
* Filter incidents.
* Paginate results.
* Sort incidents.
* Track incident creation and resolution times.

### 🔄 Incident Status Workflow

Incidents support the following statuses:

```text
OPEN
   ↓
IN_PROGRESS
   ↓
RESOLVED
   ↓
CLOSED
```

The backend validates allowed status transitions to prevent invalid workflow changes.

### 📊 Operational Metrics

OpsFlow provides several metrics through REST endpoints:

* Total incidents.
* Open incidents.
* In-progress incidents.
* Resolved incidents.
* Closed incidents.
* Incidents by priority.
* Incidents by status.
* Incidents by system.
* Incidents by category.
* Critical incidents.
* Old incidents.
* Incident age.
* Resolution times.
* Average resolution time.

### 🤖 Operational Analysis

The platform analyzes incidents and generates operational alerts based on conditions such as:

* Critical incidents.
* Incidents that have remained open for an extended period.

Example analysis:

```json
{
  "total_open_incidents": 2,
  "critical_incidents": 1,
  "old_incidents": 2,
  "alerts": []
}
```

### 📈 Dashboard

The frontend provides a dashboard with:

* General incident metrics.
* Priority analysis.
* Status analysis.
* Interactive charts.
* Operational analysis.
* Operational alerts.
* Resolution-time analysis.
* Average resolution time.
* Incidents by system.

Charts are implemented using Chart.js.

### 🌐 Frontend

The project includes a lightweight frontend built with:

* HTML
* CSS
* JavaScript
* Chart.js

Available pages:

```text
Login
Dashboard
Incidents
Incident Detail
Create Incident
```

The frontend communicates with the FastAPI backend through REST APIs and uses JWT authentication.

---

## 🏗️ Architecture

The application follows a layered architecture:

```text
┌──────────────────────────┐
│        Frontend          │
│ HTML / CSS / JavaScript  │
└────────────┬─────────────┘
             │ HTTP / JSON
             ▼
┌──────────────────────────┐
│        FastAPI           │
│       REST API           │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       Services           │
│ Business Logic           │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       SQLAlchemy         │
│          ORM             │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       PostgreSQL         │
│        Database          │
└──────────────────────────┘
```

Authentication and authorization are handled through JWT tokens and role-based dependencies.

---

## 📁 Project Structure

```text
opsflow/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── categories.py
│   │   │   ├── comment.py
│   │   │   ├── incidents.py
│   │   │   ├── metrics.py
│   │   │   ├── systems.py
│   │   │   └── users.py
│   │   │
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   ├── category.py
│   │   │   ├── comment.py
│   │   │   ├── incident.py
│   │   │   ├── system.py
│   │   │   └── user.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── category.py
│   │   │   ├── comment.py
│   │   │   ├── incident.py
│   │   │   ├── system.py
│   │   │   └── user.py
│   │   │
│   │   ├── services/
│   │   │   ├── category_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── incident_service.py
│   │   │   ├── metrics_service.py
│   │   │   ├── system_service.py
│   │   │   └── user_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_incidents.py
│   │   ├── test_metrics.py
│   │   └── test_rbac.py
│   │
│   └── alembic/
│
├── frontend/
│   ├── css/
│   │   └── styles.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── create-incident.js
│   │   ├── dashboard.js
│   │   ├── incident-detail.js
│   │   └── incidents.js
│   │
│   ├── pages/
│   │   ├── create-incident.html
│   │   ├── dashboard.html
│   │   ├── incident-detail.html
│   │   └── incidents.html
│   │
│   └── index.html
│
├── .gitignore
└── README.md
```

---

## 🧰 Technologies

### Backend

* Python 3.12
* FastAPI
* Uvicorn
* SQLAlchemy
* Psycopg
* Pydantic
* PyJWT
* pwdlib
* Argon2

### Database

* PostgreSQL 17

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

### Testing

* pytest
* FastAPI TestClient
* HTTPX

### Development Tools

* Git
* GitHub
* Visual Studio Code
* PowerShell
* Alembic
* Docker

---

## 🔑 API

The API is organized into several areas:

```text
/api/auth
/api/users
/api/incidents
/api/systems
/api/categories
/api/comments
/api/metrics
```

### Authentication

```text
POST /api/auth/login
GET  /api/auth/me
```

### Incident Management

```text
GET    /api/incidents
GET    /api/incidents/{id}
POST   /api/incidents
PUT    /api/incidents/{id}
DELETE /api/incidents/{id}
```

### Metrics

```text
GET /api/metrics/incidents
GET /api/metrics/incidents/by-priority
GET /api/metrics/incidents/by-status
GET /api/metrics/incidents/by-system
GET /api/metrics/incidents/by-category
GET /api/metrics/incidents/critical
GET /api/metrics/incidents/open
GET /api/metrics/incidents/age
GET /api/metrics/analysis
GET /api/metrics/incidents/resolution-times
GET /api/metrics/incidents/average-resolution-time
```

---

## 🧪 Testing

The project includes automated tests covering:

* Authentication.
* JWT authorization.
* Role-based access control.
* Incident creation.
* Incident retrieval.
* Incident updates.
* Incident deletion.
* Incident filtering.
* Incident pagination.
* Incident status transitions.
* Metrics.
* Operational analysis.
* Resolution analytics.

Current test result:

```text
73 passed
```

Run the complete test suite with:

```powershell
python -m pytest -v
```

---

## ▶️ Running the Project

### 1. Clone the repository

```powershell
git clone https://github.com/DieFlo04/opsflow.git
cd opsflow
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/opsflow_db
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
```

Do not commit `.env` to GitHub.

### 5. Run database migrations

```powershell
alembic upgrade head
```

### 6. Start the backend

From the project root:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 7. Open Swagger

FastAPI automatically provides interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 8. Start the frontend

Open another terminal:

```powershell
python -m http.server 5500 --directory frontend
```

Then open:

```text
http://127.0.0.1:5500
```

---

## 🔐 Security Considerations

The project implements several security mechanisms:

* Password hashing with Argon2.
* JWT authentication.
* Protected API routes.
* Role-based authorization.
* Environment variables for sensitive configuration.
* `.env` excluded through `.gitignore`.
* Backend validation of incident operations.

For a production deployment, additional hardening would be recommended, including:

* Strong production secrets.
* HTTPS.
* Secure HTTP-only cookies or another secure token storage strategy.
* Restricted CORS origins.
* Production database credentials and permissions.
* Rate limiting.
* Centralized logging and monitoring.

---

## 🎯 Project Objectives

OpsFlow was created to demonstrate practical experience in:

* Backend development with Python.
* REST API design.
* Database modeling.
* PostgreSQL.
* Authentication and authorization.
* RBAC.
* Automated testing.
* Business logic implementation.
* Operational metrics.
* Data analysis.
* Frontend/API integration.
* Git and GitHub workflows.

The project combines software development and IT operations concepts into a single application.

---

## 📌 Current Status

```text
Backend              ✅ Complete
REST API             ✅ Complete
Authentication       ✅ Complete
RBAC                 ✅ Complete
Incident Management  ✅ Complete
Metrics              ✅ Complete
Operational Analysis ✅ Complete
Resolution Analysis  ✅ Complete
System Analysis      ✅ Complete
Frontend             ✅ Complete
Dashboard            ✅ Complete
Automated Tests      ✅ 73 passed
Documentation        ✅ Complete
```

OpsFlow is currently considered a completed portfolio MVP.

---

## 👨‍💻 Author

**Diego Acosta**

Computer Systems Engineering Student

GitHub:

https://github.com/DieFlo04
