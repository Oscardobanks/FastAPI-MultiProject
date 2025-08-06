import os
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse

app = FastAPI()

NOTES_DIR = "notes"

# Ensure the notes directory exists
os.makedirs(NOTES_DIR, exist_ok=True)


def get_note_path(title: str) -> str:
    # Sanitize title to prevent directory traversal
    safe_title = "".join(c for c in title if c.isalnum()
                         or c in (' ', '_', '-')).rstrip()
    filename = f"{safe_title}.txt"
    return os.path.join(NOTES_DIR, filename)


@app.post("/notes/", status_code=status.HTTP_201_CREATED)
def add_note(title: str, content: str):
    path = get_note_path(title)
    if os.path.exists(path):
        raise HTTPException(
            status_code=409, detail="Note with this title already exists.")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"message": "Note added successfully!", "title": title, "content": content}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save note: {e}")


@app.get("/notes/{title}", response_class=PlainTextResponse)
def view_note(title: str):
    path = get_note_path(title)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Note not found.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to read note: {e}")


@app.put("/notes/{title}")
def update_note(title: str, content: str):
    path = get_note_path(title)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Note not found.")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"message": "Note updated successfully!", "title": title, "content": content}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update note: {e}")


@app.delete("/notes/{title}")
def delete_note(title: str):
    path = get_note_path(title)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Note not found.")
    try:
        os.remove(path)
        return {"message": "Note deleted successfully!", "title": title}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete note: {e}")
