from datetime import datetime
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

#
# @app.get("/students/me")
# def read_user_me():
#     return {"student": 'me'}


# @app.get("/students/me")
# def item():
#     return {"student": 'you'}


class Student(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    is_present: bool = False
    last_modified: datetime | None = None


@app.get("/students/{student_id}")
def read_student(student_id: int, q: str | None = None) -> Student:
    if student_id == 1:
        student_name = "karl"
    else:
        student_name = "brian"
    student_x =  Student(id = student_id, first_name = student_name, last_name = "real last name", is_present = False )
    return student_x


@app.get('/students')
def read_students() -> list[Student]:
    student_list = [
        Student(id=10, first_name='Kevin', is_present=True, last_modified=datetime.now()),
        Student(id=9, first_name='Carol', last_name= 'Gutierrez', is_present=False, last_modified=datetime.now()),
        Student(id=8, first_name='Felipe', last_name= 'Mina', is_present=True, last_modified=datetime(year=2020, month=1, day=31, hour=13, minute=14, second=31)),
        Student(id=7, first_name='Sofia', last_name= 'Smith', is_present=True, last_modified=datetime(year=2020, month=1, day=31, hour=13, minute=14, second=31)),
    ]
    return student_list


@app.get('/classroom')
def view_classroom() -> list[Student]:
    student_list = [
        Student(id=10, first_name='Kevin', is_present=True, last_modified=datetime.now()),
        Student(id=9, first_name='Carol', last_name='Gutierrez', is_present=False, last_modified=datetime.now()),
        Student(id=8, first_name='Felipe', last_name='Mina', is_present=True,
                last_modified=datetime(year=2020, month=1, day=31, hour=13, minute=14, second=31)),
        Student(id=7, first_name='Sofia', last_name='Smith', is_present=True,
                last_modified=datetime(year=2020, month=1, day=31, hour=13, minute=14, second=31)),
    ]
    return student_list


# create a function that takes an integer (number of timestamps) and returns a boolean (is_present) based on the number of timestamps
# e.g. 1 timestamp ->  student entered -> return True
# e.g. 0 timestamps -> return False
def find_student(number_of_timestamps: int) -> bool:
    pass

def print_name(student: Student):
    #print student name from student object
    pass

if __name__ == "__main__":
    bob = Student(id=4,first_name="bob", last_name="jones", is_present=False)
    print_name(bob)
class Color(str, Enum):
    red = 'red'
    blue = 'blue'
    yellow = 'yellow'


@app.get('/colors/{color_name}')
def get_colors_numbers(color_name: Color):
    # return color_name + " is " +  str(len(color_name)) + " letters long"
    return f"{color_name} is {str(len(color_name))} letters long"


