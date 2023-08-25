from datetime import date, time, datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, select, func, and_, FetchedValue
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped, column_property, object_session

from .database import Base


class CodeScan(Base):
    __tablename__ = "code_scans"
    id = Column(Integer, primary_key=True, index=True)
    student = Column(Integer, ForeignKey("students.id"))
    timestamp = Column(DateTime, server_default=FetchedValue())
    date = Column(Date, index=True, server_default=FetchedValue())

    scanned_student = relationship("Student")
    # scanned_student = relationship("Student", back_populates="scans")


end_times = {
    1: time(11, 0),
    2: time(11, 0),
    3: time(12, 35),
    4: time(12, 35),
    5: time(14, 45),
    6: time(14, 45),
    7: time(16, 20),
    8: time(16, 20),

}


def check_is_period(period: int):
    return datetime.now().time() < end_times.get(period)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    points = Column(Integer)
    student_number = Column(String, unique=True)
    period = Column(Integer)

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
        return self.scan_count_today % 2 == 1 and check_is_period(self.period)


class StudentDetail(Student):
    scans = relationship("CodeScan", back_populates="scanned_student", lazy="joined")
