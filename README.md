# 🛰️ Interstellar Mission Control

Um sistema de controle de missões espaciais altamente realista, inspirado no universo do filme Interstellar. Desenvolvido com foco em robustez, escalabilidade e dados científicos.

## 🚀 Tecnologias

- Python + FastAPI
- PostgreSQL
- Tailwind CSS + JS/TS
- Testes com Pytest e/ou Cypress
- Docker (futuramente)

## 🧩 Funcionalidades

- Cadastro e status de missões
- Gerenciamento da tripulação
- Telemetria (altitude, temperatura, combustível, etc.)
- Análise de planetas
- Dados do buraco negro Gargântua

## 📦 Como rodar

```bash
git clone https://github.com/seuusuario/interstellar-mission-control.git
cd interstellar-mission-control
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

🧪 Testes
pytest