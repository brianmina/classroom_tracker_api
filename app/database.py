from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = ""
DB_PASS = ""

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@spark-clam-4749.g8z.cockroachlabs.cloud:26257/defaultdb' \
                          f'?sslmode=verify-full'

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
