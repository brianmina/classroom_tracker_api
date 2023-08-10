import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import  load_dotenv

load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SQLALCHEMY_DATABASE_URL = f'cockroachdb+psycopg2://{DB_USER}:{DB_PASS}@spark-clam-4749.g8z.cockroachlabs.cloud:26257/classroom_tracker' \
                          # f'?sslmode=verify-full&sslrootcert='$HOME'/.postgresql/root.crt'

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL,
    connect_args={"application_name":"docs_simplecrud_sqlalchemy"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
