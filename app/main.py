import sys
from datetime import datetime
from enum import Enum
from logging import DEBUG
from pathlib import Path
from pprint import pformat
from sys import stdout

from fastapi import FastAPI, Depends, Request
from google.auth import default
from loguru._defaults import LOGURU_FORMAT
from sqlalchemy.orm import Session
from starlette.routing import Match

from app import crud
from app.database import SessionLocal
from app.schemas import Student
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import secure

from app.security.dependencies import validate_token
from app.security.config import settings


# import logging

from app.server_logging import init_logging

config_path = Path(__file__).with_name("logging_config.json")

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)





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
        version="0.3.0",
        # docs_url="/docs"
    )
    # logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger
    return app

app = create_app()

# @app.middleware("http")
# async def set_secure_headers(request, call_next):
#     response = await call_next(request)
#     secure_headers.framework.fastapi(response)
#     return response
#
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[settings.client_origin_url],
#     allow_methods=["GET"],
#     allow_headers=["Authorization", "Content-Type"],
#     max_age=86400,
# )



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    #
    # response = await call_next(request)
    # return response

@app.get("/students/{student_id}")
async def read_student(student_id: int, db: Session = Depends(get_db)) -> Student:
    return crud.get_student(db, student_id)


@app.get("/protected_students/{student_id}", dependencies=[Depends(validate_token)])
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
async def scan_student(student_id: int, db: Session = Depends(get_db)) -> Student:
    return crud.create_scan(db,student_id)

# create a function that takes an integer (number of timestamps) and returns a boolean (is_present)
# based on the number of timestamps
# e.g. 1 timestamp ->  student entered -> return True
# e.g. 0 timestamps -> return False
# def find_student(number_of_timestamps: int) -> bool:
#     pass


# def print_name(student: Student):
#     #print student name from student object
#     pass

# if __name__ == "__main__":
#     bob = Student(id=4, first_name="bob", last_name="jones", is_present=False)
#     print_name(bob)
class Color(str, Enum):
    red = 'red'
    blue = 'blue'
    yellow = 'yellow'


@app.get('/colors/{color_name}')
def get_colors_numbers(color_name: Color):
    # return color_name + " is " +  str(len(color_name)) + " letters long"
    return f"{color_name} is {str(len(color_name))} letters long"
