from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                    POSTGRES_PORT, POSTGRES_USER)

DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
                f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()
