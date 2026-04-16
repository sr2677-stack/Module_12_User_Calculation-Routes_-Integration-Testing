import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Default to SQLite for frictionless local testing.
# Set TEST_DATABASE_URL to use Postgres when needed.
TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_calc.db")

engine_kwargs = {}
if TEST_DB_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine_test = create_engine(TEST_DB_URL, **engine_kwargs)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)
    engine_test.dispose()
    if TEST_DB_URL.startswith("sqlite:///./"):
        sqlite_file = TEST_DB_URL.replace("sqlite:///./", "", 1)
        if os.path.exists(sqlite_file):
            os.remove(sqlite_file)


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()
