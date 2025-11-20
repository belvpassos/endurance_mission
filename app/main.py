from fastapi import FastAPI
from app.database import Base, engine

# Importar todos os routers
from app.routes import (
    mission, crew, planet, telemetryData, spacecraftStatus, abortRecoverySystem,
    anomalyDetection, commandQueue, dataRecorder, dockingSystem, navigationSystem,
    softwareUpdateLog, alertSystem, environmentMonitor, payloadSystem, powerSystem,
    fuelSystem, lifeSupportSystem, propulsionSystem, resourceManagement,
    resourceUsageLog, systemHealthCheck, thermalControlSystem, communicationSystem
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Endurance Mission Control")

# Incluir todos os routers
routers = [
    mission, crew, planet, telemetryData, spacecraftStatus, abortRecoverySystem,
    anomalyDetection, commandQueue, dataRecorder, dockingSystem, navigationSystem,
    softwareUpdateLog, alertSystem, environmentMonitor, payloadSystem, powerSystem,
    fuelSystem, lifeSupportSystem, propulsionSystem, resourceManagement,
    resourceUsageLog, systemHealthCheck, thermalControlSystem, communicationSystem
]

for r in routers:
    app.include_router(r.router)
