from fastapi import FastAPI
from app.routes import missions, crew
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Endurance Mission Control")

app.include_router(missions.router)
app.include_router(crew.router)
