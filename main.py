from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/students/{student_id}")
def read_students(student_id: int, q: Union[str, None] = None):
    if student_id == 1 :
        student_name = "karl"
    else:
        student_name = "brian"
    return {
        "student_id": student_id,
        "name": student_name,
        "q": q,
    }