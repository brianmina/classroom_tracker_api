from datetime import datetime
from enum import Enum
from logging import DEBUG
from pathlib import Path
from sys import stdout
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Depends, Request
from google.auth import default
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from app import crud, schemas
from app.database import SessionLocal
from app.exception import ClassroomTrackerException
from app.schemas import Student
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from loguru import logger
# import logging

config_path = Path(__file__).with_name("logging_config.json")

"""
GCP logging
"""


def setup_logger(
        name: str = "my_logger",
        level: int = DEBUG,
        project_id: str = "avian-serenity-393711",
):
    logger.remove()

    # Local Logging (GKE, GCE, ...):
    logger.add(stdout, level=level)

    # Cloud Logging:
    credentials, _ = default(
        quota_project_id=project_id,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = google.cloud.logging.Client(project=project_id, credentials=credentials)
    handler = CloudLoggingHandler(client, name=name)
    handler.setLevel(level=level)
    logger.add(handler)


def create_app() -> FastAPI:
    app = FastAPI(
        name="ClassroomTracker",
        version="0.2.0"
    )
    # logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger
    return app


app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:6060",
        "http://localhost",
        "https://classroom-tracker-gu6t24lssq-uk.a.run.app",
        "http://localhost:6060",
        "https://brianmina.github.io",
        "*"

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    #
    # response = await call_next(request)
    # return response


@app.exception_handler(ClassroomTrackerException)
async def unicorn_exception_handler(request: Request, exc: ClassroomTrackerException):
    return JSONResponse(
        status_code=exc.response_code,
        content={"message": exc.message},
    )


@app.get("/students/{student_id}")
async def read_student(student_id: int, db: Session = Depends(get_db)) -> Student:
    return crud.get_student(db, student_id)


@app.get("/students/{student_id}/detail")
async def read_student_detail(student_id: int, db: Session = Depends(get_db)) -> Student:
    return crud.get_student_detail(db, student_id)


@app.get('/students')
async def read_students(db: Session = Depends(get_db)) -> list[Student]:
    student_list = crud.get_students(db)
    return student_list


@app.get('/classroom')
async def view_classroom(db: Session = Depends(get_db)) -> list[Student]:
    pass


@app.post("/students/{student_id}")
async def scan_student(student_id: int, response: Response, db: Session = Depends(get_db)) -> Student:
    found_student = crud.create_scan(db, student_id)
    # server_time = datetime.now(tz=ZoneInfo("America/New_York")).time()
    # response.headers["X-server-time"] = server_time
    response.headers["X-server-time"] = str(datetime.now(tz=ZoneInfo("America/New_York")).time())
    return found_student


@app.post("/students", response_model=schemas.Student)
async def create_students(new_student: schemas.StudentBaseCreate, db: Session = Depends(get_db)):
    created_student = crud.create_student(db, new_student)
    return created_student


@app.get("/readiness")
def is_ready() :
    return Response('', status_code=200)


class Color(str, Enum):
    red = 'red'
    blue = 'blue'
    yellow = 'yellow'


@app.get('/colors/{color_name}')
def get_colors_numbers(color_name: Color):
    # return color_name + " is " +  str(len(color_name)) + " letters long"
    return f"{color_name} is {str(len(color_name))} letters long"
