# Secret Santa - Full Project

This project is a complete Secret Santa app with:
- FastAPI backend
- SQLite persistence via SQLAlchemy
- Templates (Jinja2) and static CSS with a Christmas theme
- Multi-group support, per-participant suggestion, secret token links, and draws saved in DB

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000
