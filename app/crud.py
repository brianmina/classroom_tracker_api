from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, lazyload

from . import models, schemas
from .exception import ClassroomTrackerException


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
    try:
        db.commit()
    except IntegrityError as e:
        raise ClassroomTrackerException(f"Student QR code {student_id} not found", 404)

    db.refresh(db_scan)
    return db_scan.scanned_student

