from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Student(BaseModel):
    matricule: str
    filiere: str
    nom: str
    age: int


students = []

@app.get("/students/", response_model=List[Student])
async def read_students(skip: int = 0, limit: int = 10):
    return students[skip : skip + limit]

@app.get("/students/{matricule}", response_model=Student)
async def read_student(matricule: str):
    for student in students:
        if student.matricule == matricule:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students/", response_model=Student)
async def create_student(student: Student):
    students.append(student)
    return student

@app.put("/students/{matricule}", response_model=Student)
async def update_student(matricule: str, student: Student):
    for s in students:
        if s.matricule == matricule:
            index = students.index(s)
            students[index].nom = student.nom
            students[index].filiere = student.filiere
            students[index].age = student.age
            return students[index]
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{matricule}")
async def delete_student(matricule: str):
    for i, s in enumerate(students):
        if s.matricule == matricule:
            del students[i]
            return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")
