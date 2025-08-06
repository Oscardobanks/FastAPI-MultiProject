from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict

from file_handler import Application, load_applications, load_jobs, save_application, calculate_application_status

app = FastAPI()

# Apply for a job


@app.post("/applications/", response_model=Application)
def apply(job_id: Dict[str, int]):
    applications = load_applications()
    jobs = load_jobs()
    job = next((j for j in jobs if j.job_id == job_id["job_id"]), None)
    if not job:
        raise HTTPException(
            status_code=404, detail="The Job doesn't exist.")

    # Check if you have already applied for the job
    job_application = next(
        (app for app in applications if app.id == job_id["job_id"]), None)
    if job_application:
        raise HTTPException(
            status_code=400, detail="You have already applied for this job.")
    else:
        job_application = Application.from_application(job)
        applications.append(job_application)
    save_application(applications)
    return job_application


# Get all applications
@app.get("/applications/", response_model=List[Application])
def view_applications():
    loaded_applications = load_applications()
    if not loaded_applications:
        raise HTTPException(
            status_code=404, detail="There are no applications")
    # Update status for each application
    for application in loaded_applications:
        application.status = calculate_application_status(application)
    save_application(loaded_applications)
    return loaded_applications

# Search for applications by status


@app.get("/applications/search", response_model=List[Application])
def search_application(status: str):
    applications = load_applications()
    if not applications:
        raise HTTPException(
            status_code=404, detail=(f"There are no applications with status {status}"))
    # Update status for each application before searching
    for application in applications:
        application.status = calculate_application_status(application)
    save_application(applications)
    matched = [app for app in applications if app.status.lower() ==
               status.lower()]
    if not matched:
        raise HTTPException(
            status_code=404, detail=f"No applications found with status {status}")
    return matched
