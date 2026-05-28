FastAPI User Management API
REST API for user management built with FastAPI and deployed on Google Cloud Run.
API in production:
https://fastapi-user-management-api-sqrl33cllq-tl.a.run.app
Interactive Documentation (Swagger):
https://fastapi-user-management-api-sqrl33cllq-tl.a.run.app/docs
Technologies
FastAPI: Web framework for building the API
SQLAlchemy 2: ORM for database interaction
Pydantic v2: Data validation and schemas
Uvicorn: ASGI server for running FastAPI
PostgreSQL: Production database (Cloud SQL)
SQLite: Local development and testing database
pytest + httpx: Integration tests
Docker: Application container
Google Cloud Run: Serverless API hosting
Google Cloud SQL: Managed PostgreSQL database
Google Cloud Build: CI/CD pipeline (build → test → deploy)
Google Artifact Registry: Docker image registry
Google Secret Manager: Secure credentials storage
Run Locally
Prerequisites

Python 3.11+
Git

Steps

Clone the repository
git clone https://github.com/gseguel/fastapi-user-management-api.git
Create virtual environment

Mac/Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Configure environment variables

Create .env at the project root:
DATABASE_URL=sqlite:///./data/users.db
APP_TITLE=User Management API
APP_VERSION=1.0.0

Start the API
uvicorn app.main:app --reload
Open in browser
API: http://localhost:8000
Swagger UI: http://localhost:8000/docs
Health check: http://localhost:8000/health

Run Tests
pytest tests/ -v
GCP Deployment
Deployment is automatic via Cloud Build on every push to main