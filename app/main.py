from fastapi import FastAPI
from app.database import Base, engine
from app import models

# Importar todos os routers
from app.routes import (
    mission, crew, planet, telemetryData, spacecraftStatus, abortRecoverySystem,
    anomalyDetection, commandQueue, dataRecorder, dockingSystem, navigationSystem,
    softwareUpdateLog, alertSystem, environmentMonitor, payloadSystem, powerSystem,
    fuelSystem, lifeSupportSystem, propulsionSystem, resourceManagement,
    resourceUsageLog, systemHealthCheck, thermalControlSystem, communicationSystem,
    groundControlLog, missionEvents, subsystemDiagnostics, spacecraft,
    missionControl
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Endurance Mission Control",
    summary="Mission control backend for deep-space mission monitoring and subsystem operations.",
    description=(
        "Endurance Mission Control is a FastAPI backend inspired by deep-space mission "
        "operations in the spirit of Interstellar. The API models mission planning, "
        "crew coordination, vehicle health, telemetry, navigation, docking, life support, "
        "alerts, and ground-control communication for a recruiter-friendly portfolio demo."
    ),
    version="0.2.0",
    contact={
        "name": "Maria Izabel Vieira Passos",
        "url": "https://github.com/belvpassos",
    },
    openapi_tags=[
        {"name": "Mission Control", "description": "Operational overview and executive mission summary."},
        {"name": "Demo Data", "description": "Bootstrap realistic demo data for portfolio walkthroughs."},
        {"name": "Spacecraft", "description": "Space vehicle records and mission-ready spacecraft catalog."},
        {"name": "Missions", "description": "Mission lifecycle records and high-level mission planning."},
        {"name": "Crew", "description": "Crew manifest and role assignments."},
        {"name": "Planets", "description": "Destination and celestial body reference data."},
    ],
)

# Incluir todos os routers
routers = [
    mission, crew, planet, telemetryData, spacecraftStatus, abortRecoverySystem,
    anomalyDetection, commandQueue, dataRecorder, dockingSystem, navigationSystem,
    softwareUpdateLog, alertSystem, environmentMonitor, payloadSystem, powerSystem,
    fuelSystem, lifeSupportSystem, propulsionSystem, resourceManagement,
    resourceUsageLog, systemHealthCheck, thermalControlSystem, communicationSystem,
    groundControlLog, missionEvents, subsystemDiagnostics, spacecraft,
    missionControl
]

for r in routers:
    app.include_router(r.router)


@app.get("/", tags=["Mission Control"])
def read_root():
    return {
        "service": "Endurance Mission Control",
        "version": app.version,
        "docs": "/docs",
        "status": "ready",
    }


@app.get("/health", tags=["Mission Control"])
def health_check():
    return {"status": "ok"}
