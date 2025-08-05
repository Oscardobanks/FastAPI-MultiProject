import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

DATA_FILE = "students.json"

app = FastAPI()


class StudentResult(BaseModel):
    name: str
    scores: Dict[str, float]


class Student(BaseModel):
    name: str
    scores: Dict[str, float]
    average: float
    grade: str

    @staticmethod
    def calculate_average(scores: Dict[str, float]) -> float:
        if not scores:
            return 0.0
        return sum(scores.values()) / len(scores)

    @staticmethod
    def calculate_grade(average: float) -> str:
        if average >= 80:
            return "A"
        elif average >= 70:
            return "B+"
        elif average >= 60:
            return "B"
        elif average >= 55:
            return "C+"
        elif average >= 50:
            return "C"
        elif average >= 45:
            return "D+"
        elif average >= 40:
            return "D"
        else:
            return "F"

    @classmethod
    def from_result(cls, result: StudentResult):
        avg = cls.calculate_average(result.scores)
        grade = cls.calculate_grade(avg)
        return cls(name=result.name, scores=result.scores, average=avg, grade=grade)


# Save student data to JSON file
def save_students(students: List[Student]):
    with open(DATA_FILE, "w") as file:
        json.dump([student.dict() for student in students], file, indent=2)

# Load student data from JSON


def load_students() -> List[Student]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            try:
                data = json.loads(content)
                return [Student(**d) for d in data]
            except json.JSONDecodeError:
                # Optionally, log or handle the error
                return []
    return []


@app.post("/students/", response_model=Student)
def add_student(stud: StudentResult):
    students = load_students()
    for s in students:
        if s.name.lower() == stud.name.lower():
            raise HTTPException(
                status_code=400, detail="Student already exists"
            )
    student = Student.from_result(stud)
    students.append(student)
    save_students(students)
    return student

# Get specific student data


@app.get("/students/{name}", response_model=Student)
def view_student(name: str):
    students = load_students()
    for s in students:
        if s.name.lower() == name.lower():
            return s
    raise HTTPException(status_code=404, detail="Student not found")

# Get all Students


@app.get("/students", response_model=List[Student])
def view_students():
    students = load_students()
    if not students:
        raise HTTPException(status_code=404, detail="There are no students")
    return students
