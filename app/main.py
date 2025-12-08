from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import templates
from app.routers import groups, participants, draws
from app.database import Base, engine
from app.models import Group
from app.database import get_db

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(participants.router, prefix="/participants", tags=["participants"])
app.include_router(draws.router, prefix="/draws", tags=["draws"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    groups = db.query(Group).all()

    return templates.TemplateResponse("index.html", {"request": request, "groups": groups})
