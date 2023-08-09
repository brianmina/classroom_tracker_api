from datetime import datetime

from pydantic import BaseModel

class StudentBase(BaseModel):
    first_name: str
    last_name: str | None = None
    is_present: bool = False
    last_modified: datetime | None = None

class StudentBaseCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True

class CodeScanBase(BaseModel):
    timestamp: datetime
    date: datetime

class CodeScanCreate(CodeScanBase):
    pass

class CodeScan(CodeScanBase):
    id: int

    class Config:
        orm_mode = True

