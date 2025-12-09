from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.core.config import templates
from app.database import Base, engine, get_db
from app.init_db import init_db
from app.models import Group
from app.routers import groups, participants, draws

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(
    participants.router, prefix="/participants", tags=["participants"]
)
app.include_router(draws.router, prefix="/draws", tags=["draws"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    groups = db.query(Group).all()

    return templates.TemplateResponse(
        "index.html", {"request": request, "groups": groups}
    )
