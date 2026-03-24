from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TU API KEY
API_KEY = "ad1319c3fa2f328a63fb60550d70c05b"

@app.get("/")
def home():
    return {"mensaje": "IA funcionando"}

# Función de análisis tipo tipster
def analizar_partidos(matches, team_id):
    goles_favor = 0
    goles_contra = 0
    victorias = 0
    tarjetas = 0
    partidos = 0

    for m in matches["response"]:
        goals_home = m["goals"]["home"]
        goals_away = m["goals"]["away"]

        if goals_home is None or goals_away is None:
            continue

        partidos += 1

        if m["teams"]["home"]["id"] == team_id:
            gf = goals_home
            gc = goals_away
        else:
            gf = goals_away
            gc = goals_home

        goles_favor += gf
        goles_contra += gc

        if gf > gc:
            victorias += 1

        cards = m.get("cards", {})
        tarjetas += len(cards.get("yellow", [])) + len(cards.get("red", []))

    return {
        "gf": goles_favor,
        "gc": goles_contra,
        "wins": victorias,
        "matches": partidos,
        "cards": tarjetas
    }

@app.post("/prediccion")
def prediccion(data: dict):
    equipo1 = data["equipo1"]
    equipo2 = data["equipo2"]

    headers = headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

    # Buscar equipos
    res1 = requests.get(
        f"https://v3.football.api-sports.io/teams?search={equipo1}",
        headers=headers
    ).json()

    res2 = requests.get(
        f"https://v3.football.api-sports.io/teams?search={equipo2}",
        headers=headers
    ).json()

    if not res1["response"] or not res2["response"]:
        return {"error": "Equipo no encontrado"}

    id1 = res1["response"][0]["team"]["id"]
    id2 = res2["response"][0]["team"]["id"]

    # Últimos partidos
    matches1 = requests.get(
        f"https://v3.football.api-sports.io/fixtures?team={id1}&last=5",
        headers=headers
    ).json()

    matches2 = requests.get(
        f"https://v3.football.api-sports.io/fixtures?team={id2}&last=5",
        headers=headers
    ).json()

    # Analizar stats
    stats1 = analizar_partidos(matches1, id1)
    stats2 = analizar_partidos(matches2, id2)

    # Score tipster
    score1 = (
        stats1["wins"] * 4 +
        stats1["gf"] * 1.5 -
        stats1["gc"] * 1.2 -
        stats1["cards"] * 0.2
    )

    score2 = (
        stats2["wins"] * 4 +
        stats2["gf"] * 1.5 -
        stats2["gc"] * 1.2 -
        stats2["cards"] * 0.2
    )

    # Forma reciente
    forma1 = stats1["wins"] / stats1["matches"] if stats1["matches"] > 0 else 0.5
    forma2 = stats2["wins"] / stats2["matches"] if stats2["matches"] > 0 else 0.5

    score1 += forma1 * 10
    score2 += forma2 * 10

    # Probabilidades
    total = score1 + score2
    prob1 = score1 / total if total > 0 else 0.5
    prob2 = 1 - prob1

    return {
        "equipo1": equipo1,
        "equipo2": equipo2,
        "probabilidad_equipo1": round(prob1 * 100),
        "probabilidad_equipo2": round(prob2 * 100),
        "stats_equipo1": stats1,
        "stats_equipo2": stats2
    }


