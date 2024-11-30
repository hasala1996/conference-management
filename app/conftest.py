import atexit
import os
import subprocess
from datetime import datetime, timedelta

import jwt
import pytest
from adapters.api.dependencies import get_db
from config import settings
from fast_api.fast_api_app import create_app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

app = create_app()
TEST_DB_NAME = f"test_db_{os.urandom(8).hex()}"
TEST_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{TEST_DB_NAME}"
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def cleanup_database():
    if database_exists(TEST_DATABASE_URL):
        drop_database(TEST_DATABASE_URL)
        print(f"Test database {TEST_DB_NAME} dropped.")


atexit.register(cleanup_database)


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    """
    Creates a new database engine for tests, ensuring UTF-8 encoding.
    The database engine is created only once before the tests are run.
    """
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL, encoding="utf8")

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"options": "-c client_encoding=utf8"},
    )

    SessionLocal.configure(bind=engine)

    execute_alembic_migrations()

    yield engine

    engine.dispose()
    drop_database(TEST_DATABASE_URL)


def execute_alembic_migrations():
    print("Executing Alembic migrations...")
    project_root = os.path.dirname(os.path.abspath(__file__))

    os.environ["DATABASE_URL"] = TEST_DATABASE_URL

    command = ["alembic", "-c", "alembic.ini", "upgrade", "heads"]
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, cwd=project_root)
        print("Alembic migrations executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing Alembic migrations:")
        print(e.output)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Creates a new database session for a test.
    This fixture is executed before each test function.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def setup_override_get_db(db_session):
    app.dependency_overrides[get_db] = lambda: db_session


@pytest.fixture
def client():
    """
    Creates a test client for the FastAPI application.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def initialize_seed_data(db_engine):
    """
    Seeds the database with initial data for tests.
    """
    from seed_data import seed_data

    with SessionLocal(bind=db_engine) as session:
        seed_data(session)
    print("Seed data loaded for tests.")


@pytest.fixture(scope="function")
def admin_token(db_session):
    """
    Generates a JWT token for the seeded admin user.
    """
    from adapters.database.models.user_model import User

    admin_user = (
        db_session.query(User).filter(User.email == "admin@example.com").first()
    )
    if not admin_user:
        raise ValueError("Admin user not found in the database.")

    expire = datetime.utcnow() + timedelta(
        minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"user_id": str(admin_user.id), "email": admin_user.email, "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token
