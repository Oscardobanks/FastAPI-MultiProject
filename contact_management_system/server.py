from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Contact(BaseModel):
    name: str
    phone: str
    email: str


contacts: Contact = {}


@app.post("/contacts/", status_code=201)
def add_contact(contact: Contact):
    key = contact.name.lower()
    if key in contacts:
        raise HTTPException(
            status_code=409, detail=f"Contact '{contact.name}' already exists.")
    contacts[key] = contact
    return {"message": "Contact added successfully", "contact": contact}


@app.get("/contact/")
def search_contact(name: str = Query(..., min_length=1)):
    key = name.lower()
    if key not in contacts:
        raise HTTPException(
            status_code=404, detail=f"Contact not found: {name}")
    return {"message": "Contact found", "contact": contacts[key]}


@app.put("/contact/{name}")
def update_contact(name: str = Path(..., min_length=1), contact: Contact = None):
    key = name.lower()
    if key not in contacts:
        raise HTTPException(
            status_code=404, detail=f"Contact not found: {name}")
    contacts[key] = contact
    return {"message": "Contact updated successfully", "contact": contact}


@app.delete("/contact/{name}")
def delete_contact(name: str = Path(..., min_length=1)):
    key = name.lower()
    if key not in contacts:
        raise HTTPException(
            status_code=404, detail=f"Contact not found: {name}")
    deleted_contact = contacts.pop(key)
    return {"message": "Contact deleted successfully", "contact": deleted_contact}
