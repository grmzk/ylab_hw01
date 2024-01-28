import pytest
from config import (POSTGRES_DB_TEST, POSTGRES_HOST_TEST,
                    POSTGRES_PASSWORD_TEST, POSTGRES_PORT_TEST,
                    POSTGRES_USER_TEST)
from database import Base as Base_menus
from database import get_session
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

DATABASE_URL_TEST = (
    f"postgresql://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}"
    f"@{POSTGRES_HOST_TEST}:{POSTGRES_PORT_TEST}/{POSTGRES_DB_TEST}"
)

engine_test = create_engine(DATABASE_URL_TEST)
SessionTest = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)


def override_get_session():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base_menus.metadata.create_all(bind=engine_test)
    yield
    Base_menus.metadata.drop_all(bind=engine_test)


client = TestClient(app=app, base_url="http://localhost:8000/api/v1")
