from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    points = Column(Integer)

    scans = relationship("CodeScan", back_populates="scanned_student")


class CodeScan(Base):
    __tablename__ = "code_scans"
    id = Column(Integer, primary_key=True, index=True)
    student = Column(Integer, ForeignKey("students.id"))
    timestamp = Column(DateTime)
    date = Column(Date, index=True)

    scanned_student = relationship("Student", back_populates="scans")
