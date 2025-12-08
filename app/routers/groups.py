# app/routers/groups.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Group, Participant, Draw
from app.core.config import templates  # assume que templates foi movido para core.config

router = APIRouter()

# LISTAR GRUPOS (GET /groups/)
@router.get("/", response_class=HTMLResponse)
def list_groups(request: Request, db: Session = Depends(get_db)):
    groups = db.query(Group).order_by(Group.created_at.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "groups": groups})

# CRIAR GRUPO via form (POST /groups/)
@router.post("/", response_class=RedirectResponse)
def create_group(
    request: Request,
    name: str = Form(...),
    price: str = Form(None),
    time: str = Form(None),
    place: str = Form(None),
    db: Session = Depends(get_db),
):
    g = Group(name=name.strip() or "Sem nome", price=price or "", time=time or "", place=place or "")
    db.add(g)
    db.commit()
    db.refresh(g)
    # redireciona para a página do grupo criado
    return RedirectResponse(url=f"/groups/{g.id}", status_code=303)

# VER PÁGINA DO GRUPO (GET /groups/{group_id})
@router.get("/{group_id}", response_class=HTMLResponse)
def group_page(group_id: int, request: Request, db: Session = Depends(get_db)):
    g = db.query(Group).filter(Group.id == group_id).first()
    if not g:
        return templates.TemplateResponse("not_found.html", {"request": request, "message": "Grupo não encontrado."})
    participants = db.query(Participant).filter(Participant.group_id == group_id).order_by(Participant.created_at).all()
    draws_exist = db.query(Draw).filter(Draw.group_id == group_id).first() is not None
    return templates.TemplateResponse("group.html", {"request": request, "group": g, "participants": participants, "draws_exist": draws_exist})
