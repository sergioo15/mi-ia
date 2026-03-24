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

# 👇 PON TU API KEY AQUÍ
API_KEY = "ad1319c3fa2f328a63fb60550d70c05b"

@app.get("/")
def home():
    return {"mensaje": "IA funcionando"}

@app.post("/prediccion")
def prediccion(data: dict):
    equipo1 = data["equipo1"]
    equipo2 = data["equipo2"]

    headers = {
        "x-apisports-key": API_KEY
    }

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

    # lógica básica
    prob1 = 55
    prob2 = 45

    return {
        "equipo1": equipo1,
        "equipo2": equipo2,
        "probabilidad_equipo1": prob1,
        "probabilidad_equipo2": prob2
    }


