from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# 👇 ESTO ES LO IMPORTANTE (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "IA funcionando"}

@app.post("/prediccion")
def prediccion(data: dict):
    equipo1 = data["equipo1"]
    equipo2 = data["equipo2"]

    prob1 = random.randint(40, 60)
    prob2 = 100 - prob1

    return {
        "equipo1": equipo1,
        "equipo2": equipo2,
        "probabilidad_equipo1": prob1,
        "probabilidad_equipo2": prob2
    }

