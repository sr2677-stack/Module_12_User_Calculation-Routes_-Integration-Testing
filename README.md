## Module 12 - User and Calculation Routes Integration Testing

FastAPI backend with:
- User registration and login endpoints
- Calculation BREAD endpoints (Browse, Read, Edit, Add, Delete)
- Integration tests with `pytest`
- GitHub Actions CI with PostgreSQL
- Docker image build and push to Docker Hub after tests pass

## API Endpoints

### User routes
- `POST /users/register`
- `POST /users/login`

### Calculation routes
- `GET /calculations/` (Browse)
- `GET /calculations/{id}` (Read)
- `POST /calculations/` (Add)
- `PATCH /calculations/{id}` (Edit)
- `DELETE /calculations/{id}` (Delete)

## Run Locally (Without Docker)

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Open:
- Swagger docs: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`
- Health: `http://127.0.0.1:8001/health`

## Run Integration Tests Locally

Default (SQLite-based test DB):

```bash
pytest -v
```

Run tests against PostgreSQL (optional):

```bash
# Example:
# $env:TEST_DATABASE_URL="postgresql://postgres:password@localhost:5444/calcdb_test"
pytest -v
```

## Run with Docker Compose

```bash
docker compose up --build
```

API will be available at:
- `http://localhost:8001/docs`

Stop containers:

```bash
docker compose down
```

## CI/CD (GitHub Actions)

Workflow file: `.github/workflows/ci.yml`

Pipeline behavior:
1. Starts PostgreSQL service
2. Installs Python dependencies
3. Runs `pytest -v`
4. If tests pass on `main` push, builds and pushes Docker image to Docker Hub

### Required GitHub Secrets

Set these in `Settings -> Secrets and variables -> Actions`:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Docker Hub Repository

Image name configured in workflow:
- `DOCKERHUB_USERNAME/module12-fastapi-app`

Repository link (replace username with yours):
- `https://hub.docker.com/r/sr2677stack/module12-fastapi-app`

## Submission Checklist

- GitHub repo link
- Screenshot of successful GitHub Actions run
- Screenshot of running app endpoints (`/docs` with working calls)
- Reflection document (`REFLECTION.md`)
- Docker Hub repository link
