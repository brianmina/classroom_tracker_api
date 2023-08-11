from datetime import date
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, select, func, and_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped, column_property, object_session

from .database import Base




    # @hybrid_property
    # def is_present(self):
    #     return sum(v.value == 1 for v in self.votes)
    #
    # @likes.expression
    # def likes(cls):
    #     return select(func.count(1).filter(PostVote.value == 1)). \
    #         where(PostVote.problem_id == cls.id). \
    #         label('likes')

class CodeScan(Base):
    __tablename__ = "code_scans"
    id = Column(Integer, primary_key=True, index=True)
    student = Column(Integer, ForeignKey("students.id"))
    timestamp = Column(DateTime)
    date = Column(Date, index=True)

    scanned_student = relationship("Student")
    # scanned_student = relationship("Student", back_populates="scans")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    points = Column(Integer)

    # scans = relationship("CodeScan", back_populates="scanned_student", lazy="joined")
    # scans = Mapped[List["CodeScan"]] = relationship()

    scan_count_today = column_property(
        select(func.count(CodeScan.id))
        .where(
            and_(
                CodeScan.student == id,
                CodeScan.date == date.today()
            )
        )
        .scalar_subquery()
    )

    last_modified = column_property(
        select(CodeScan.timestamp)
        .where(
            and_(
                CodeScan.student == id
            )
        )
        .order_by(CodeScan.id.desc())
        .limit(1)
        .scalar_subquery()
    )

    @hybrid_property
    def is_present(self):
        return self.scan_count_today % 2 == 1


class StudentDetail(Student):
    scans = relationship("CodeScan", back_populates="scanned_student", lazy="joined")