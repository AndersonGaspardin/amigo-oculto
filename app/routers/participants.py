import secrets

from fastapi import APIRouter, Depends, Form,Request
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Participant,Group
from app.core.config import templates  # assume que templates foi movido para core.config


router = APIRouter()


@router.post("/add/{group_id}", response_class=HTMLResponse)
def add_participant(
    group_id: int,
    request: Request,
    name: str = Form(...),
    suggestion: str = Form(None),
    db: Session = Depends(get_db)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Grupo não encontrado"}
        )

    token = secrets.token_urlsafe(32)

    participant = Participant(
        name=name,
        suggestion=suggestion,
        secret_token=token,
        group_id=group_id
    )

    db.add(participant)
    db.commit()
    db.refresh(participant)

    return templates.TemplateResponse(
        "participant_added.html",
        {
            "request": request,
            "participant": participant,
            "group": group
        }
    )
