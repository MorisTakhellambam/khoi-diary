from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import models, database
from app.database import Base, engine
from app.models import Note  # your Note model

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

models.Base.metadata.create_all(bind=database.engine)


@app.get("/", response_class=HTMLResponse)
def read_notes(request: Request):
    db = database.SessionLocal()
    notes = db.query(models.Note).order_by(models.Note.id.desc()).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})


@app.post("/add", response_class=RedirectResponse)
def add_note(request: Request, title: str = Form(...), content: str = Form(...)):
    db = database.SessionLocal()
    note = models.Note(title=title, content=content)
    db.add(note)
    db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{note_id}", response_class=RedirectResponse)
def delete_note(note_id: int):
    db = database.SessionLocal()
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)
