"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice basketball and participate in tournaments",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create your own masterpieces",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Learn acting skills and participate in school plays",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["sophia@mergington.edu", "amelia@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["ethan@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["harper@mergington.edu", "ella@mergington.edu"]
    }
}


class CityList(BaseModel):
    cities: List[str]


@app.get("/")
def root():
    """
    Redireciona para a página inicial estática da aplicação web.
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """
    Retorna todas as atividades extracurriculares disponíveis.
    """
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """
    Inscreve um estudante em uma atividade específica.
    Args:
        activity_name (str): O nome da atividade para inscrição.
        email (str): O endereço de e-mail do estudante.
    Raises:
        HTTPException: Se a atividade não existir (404).
        HTTPException: Se o estudante já estiver inscrito na atividade (400).
    Returns:
        dict: Uma mensagem confirmando que o estudante foi inscrito na atividade.
    """
    # Valida se a atividade existe
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Obtém a atividade específica
    activity = activities[activity_name]

    # Valida se o aluno já está inscrito
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Já inscrito")
    
    # Adiciona o estudante
    activity["participants"].append(email)
    return {"message": f"{email} inscrito em {activity_name}"}


@app.get("/countries/{country_name}", response_model=CityList)
def get_country(country_name: str):
    """
    Retorna as cidades de um país.
    """
    # Simula consulta ao banco de dados
    country_cities = {
        "USA": ["New York", "Los Angeles", "Chicago"],
        "Canada": ["Toronto", "Montreal", "Vancouver"],
        "Brazil": ["Sao Paulo", "Rio de Janeiro", "Brasilia"]
    }

    if country_name in country_cities:
        return CityList(cities=country_cities[country_name])
    else:
        raise HTTPException(status_code=404, detail="País não encontrado")
