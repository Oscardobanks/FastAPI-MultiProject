import json
import os
from fastapi import FastAPI

DATA_FILE = "students.json"

app = FastAPI()


class Student:
    def __init__(self, name, subject_scores):
        self.name = name
        self.subject_scores = subject_scores
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self):
        if not self.subject_scores:
            return 0
        return sum(self.subject_scores) / len(self.subject_scores)

    def calculate_grade(self):
        avg = self.average
        if avg >= 80:
            return "A"
        elif avg >= 70:
            return "B+"
        elif avg >= 60:
            return "B"
        elif avg >= 55:
            return "C+"
        elif avg >= 50:
            return "C"
        elif avg >= 45:
            return "D+"
        elif avg >= 40:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "name": self.name,
            "subjects": self.subjects,
            "scores": self.scores,
            "average": self.average,
            "grade": self.grade,
        }


def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump([s.to_dict() for s in students], f)


def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Student.from_dict(d) for d in data]
    return []


@app.post("/students")
def add_student():
    students = load_students()
    name = input("Enter the student name: ")
    subjects = input(f"Enter {name}'s subjects (comma separated): ").split(",")
    subjects = [s.strip() for s in subjects]
    scores = []
    for subject in subjects:
        while True:
            try:
                score = float(input(f"Score for {subject}: "))
                break
            except:
                print("Invalid score.")
        scores.append(score)
    student = Student(name, subjects, scores)
    students.append(student)
    print("Student added.")


@app.get("/students/{name}")
def view_student(name):
    students = load_students()
    if not students:
        print("There are no students yet.")
    for s in students:
        if s.name.lower() == name.lower():
            print(f"\nStudent Name is {s.name}")
            for subj, score in zip(s.subjects, s.scores):
                print(f"\n{subj}: {score}")
            print(f"\nAverage: {s.average:.2f}, Grade: {s.grade}")
            return
    print("The student is not found.")


@app.get("/students")
def view_students():
    students = load_students()
    if not students:
        print("There are no students yet.")
    for s in students:
        print(f"\nStudent Name is {s.name}")
        for subj, score in zip(s.subjects, s.scores):
            print(f"\n{subj}: {score}")
        print(f"\nAverage: {s.average:.2f}, Grade: {s.grade}")
