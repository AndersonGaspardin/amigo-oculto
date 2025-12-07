from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/sortear", response_class=HTMLResponse)
async def sortear(
    request: Request,
    participants: str = Form(...),
    gift_suggestion: str = Form(""),
    price: str = Form(""),
    time: str = Form(""),
    place: str = Form("")
):
    names = [p.strip() for p in participants.split("\n") if p.strip()]
    shuffled = names[:]
    random.shuffle(shuffled)

    # se alguém tirar ele mesmo, embaralha novamente
    while any(a == b for a, b in zip(names, shuffled)):
        random.shuffle(shuffled)

    pairs = list(zip(names, shuffled))

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "pairs": pairs,
            "gift_suggestion": gift_suggestion,
            "price": price,
            "time": time,
            "place": place
        }
    )
