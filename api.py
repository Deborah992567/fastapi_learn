from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Creating our first API
students = {
    1: {
        "name": "felix",
        "age": 35,
        "gender": "male",
        "profession": "banker"
    }
}

class Student(BaseModel):
    name: str
    age: int
    gender: str
    profession: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    profession: Optional[str] = None

@app.get("/")
def read_name():
    return {"name": "first name"}

# Endpoint parameter is used to return data relating to an endpoint
@app.get("/get-student/{student_id}")
def get_student_by_id(student_id: int = Path(..., description="the ID of the student you are looking for", gt=0, lt=5)):
    if student_id not in students:
        return {"error": "Student not found"}
    return students[student_id]

# Query parameters
@app.get("/get-by-name")
def get_student_by_name(name: str):
    for student in students.values():
        if student["name"] == name:
            return student
    return {"message": "student not found"}
# for get student details using age 
@app.get("/get-by-age")
def get_student_by_age(age: int):
    for student in students.values():
        if student["age"] == age:
            return student
    return {"message": "not found"}

# Request body and POST method
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"error": "student_id already exists"}
    students[student_id] = student.dict()
    return students[student_id]

# PUT method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"error": "student_id not found"}
    
    # Update only the fields that are provided (not None)
    existing_student = students[student_id]
    update_data = student.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        existing_student[field] = value
    
    return students[student_id]

# delete method 
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return {"message":" student does not exist"}
    
    del students[student_id]
    return{"message":"students_id and details deleted successfully!"}
     