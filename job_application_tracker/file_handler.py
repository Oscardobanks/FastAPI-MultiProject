import json
import os
from pydantic import BaseModel
from typing import List
from datetime import datetime, date

APPLICATION_FILE = "applications.json"
JOB_FILE = "jobs.json"


class Job(BaseModel):
    job_id: int
    name: str
    company: str
    position: str
    posted_date: str


class Application(BaseModel):
    id: int
    name: str
    company: str
    position: str
    status: str
    posted_date: str
    application_date: str

    @classmethod
    def from_application(cls, job: Job):
        return cls(
            id=job.job_id,
            name=job.name,
            company=job.company,
            position=job.position,
            status="Applied",
            posted_date=job.posted_date,
            application_date=f"{date.today()}"
        )

# Calculate job status by date


def calculate_application_status(application: Application):
    app_date = datetime.strptime(
        application.application_date, "%Y-%m-%d").date()
    today = date.today()
    days_since = (today - app_date).days
    if days_since == 0:
        return "Applied"
    elif 0 < days_since <= 3:
        return "Pending"
    else:
        return "Rejected"

# Save application data to JSON file


def save_application(application: List[Application]):
    with open(APPLICATION_FILE, "w") as file:
        json.dump([job_app.model_dump()
                  for job_app in application], file, indent=2)

# Load jobs & applications data from JSON


def load_jobs() -> List[Job]:
    if os.path.exists(JOB_FILE):
        with open(JOB_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            try:
                data = json.loads(content)
                return [Job(**d) for d in data]
            except json.JSONDecodeError:
                return []
    return []


def load_applications() -> List[Application]:
    if os.path.exists(APPLICATION_FILE):
        with open(APPLICATION_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            try:
                data = json.loads(content)
                return [Application(**d) for d in data]
            except json.JSONDecodeError:
                return []
    return []
