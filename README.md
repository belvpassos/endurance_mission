# 🛰️ Endurance Mission Control

A highly realistic space mission control system, inspired by the universe of the movie *Interstellar*. Designed with a strong focus on robustness, scalability, and scientific data.

> ⚠️ **This API is still under development.** Features and structure may change as the project evolves.

## 🚀 Technologies

- Python + FastAPI  
- PostgreSQL  
- Tailwind CSS + JS/TS  
- Testing with Pytest and/or Cypress  
- Docker (coming soon)  

## 🧩 Features (Planned & In Progress)

- Mission registration and status tracking  
- Crew management  
- Telemetry (altitude, temperature, fuel, etc.)  
- Planet analysis  
- Gargantua black hole data  

## 📦 How to Run

```bash
git clone https://github.com/yourusername/interstellar-mission-control.git
cd interstellar-mission-control
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 🧪 Running Tests

```bash
pytest
