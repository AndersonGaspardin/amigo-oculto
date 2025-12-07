from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# armazenamento temporário dos pares sorteados
results_cache = {}


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

    # evitar auto-sorteio
    while any(a == b for a, b in zip(names, shuffled)):
        random.shuffle(shuffled)

    pairs = dict(zip(names, shuffled))

    # armazenar cache temporário
    global results_cache
    results_cache = {
        "pairs": pairs,
        "gift_suggestion": gift_suggestion,
        "price": price,
        "time": time,
        "place": place,
    }

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "names": names,
        }
    )


@app.get("/reveal/{person}", response_class=HTMLResponse)
async def reveal(request: Request, person: str):
    global results_cache

    giver = person
    receiver = results_cache["pairs"].get(person)
    gift = results_cache["gift_suggestion"]
    price = results_cache["price"]
    time = results_cache["time"]
    place = results_cache["place"]

    return templates.TemplateResponse(
        "reveal.html",
        {
            "request": request,
            "giver": giver,
            "receiver": receiver,
            "gift": gift,
            "price": price,
            "time": time,
            "place": place,
        }
    )
