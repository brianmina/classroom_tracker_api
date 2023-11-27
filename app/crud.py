from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, lazyload

from . import models, schemas
from .exception import ClassroomTrackerException
from . import models, schemas


def get_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    return student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def get_student_detail(db: Session, student_id: int):
    return db.query(models.StudentDetail).filter(models.StudentDetail.id == student_id).first()


def create_scan(db: Session, student_id: int):
    db_scan = models.CodeScan(student=student_id)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan.scanned_student


def create_student(db: Session, new_student: schemas.StudentBaseCreate) -> models.Student:
    db_student = models.Student(**new_student.model_dump(), points=0)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    # TODO: implement
    pass

