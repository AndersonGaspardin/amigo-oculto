# app/routers/draw.py

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.services.draw_service import perform_draw
from app.models import Participant, Draw, Group
from app.core.config import templates
from app.database import get_db

router = APIRouter()


# ---------- EXECUTAR O SORTEIO ----------
@router.get("/run/{group_id}")
def run_draw(group_id: int,    request: Request,
 db: Session = Depends(get_db)):
    perform_draw(group_id, db)
    return templates.TemplateResponse("draw_done.html", {"request": request, "group": Group(id=group_id)})


# ---------- RESULTADO POR ID (APENAS PARA ADM) ----------
@router.get("/participant/{participant_id}", response_class=HTMLResponse)
def show_result_by_id(
    participant_id: int, request: Request, db: Session = Depends(get_db)
):
    participant = db.query(Participant).filter_by(id=participant_id).first()
    if not participant:
        return HTMLResponse("Participante não encontrado", status_code=404)

    draw = db.query(Draw).filter_by(giver_id=participant.id).first()
    if not draw:
        return HTMLResponse("Sorteio ainda não realizado.", status_code=404)

    assigned = db.query(Participant).filter_by(id=draw.receiver_id).first()

    return templates.TemplateResponse(
        "participant_result.html",
        {
            "request": request,
            "participant": participant,
            "assigned": assigned,
        },
    )


# ---------- RESULTADO VIA TOKEN (PÚBLICO) ----------
@router.get("/result/{token}", response_class=HTMLResponse)
def show_result_by_token(
    token: str, request: Request, db: Session = Depends(get_db)
):
    participant = db.query(Participant).filter_by(secret_token=token).first()

    if not participant:
        return HTMLResponse("Token inválido.", status_code=404)

    draw = db.query(Draw).filter_by(giver_id=participant.id).first()
    if not draw:
        return HTMLResponse("Nenhum sorteio encontrado.", status_code=404)

    receiver = db.query(Participant).filter_by(id=draw.receiver_id).first()

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "giver": participant,
            "receiver": receiver,
            "group": participant.group,
        },
    )
