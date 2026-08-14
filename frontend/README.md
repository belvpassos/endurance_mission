# Endurance Mission Control UI

Frontend React do projeto `Endurance Mission Control`.

Esta aplicação apresenta uma primeira experiência visual para o backend de mission control da nave `Endurance`, com foco em leitura operacional rápida para demo de portfólio. A interface consome o endpoint `mission-control/overview` e destaca readiness, fase da missão, alvo atual, alertas ativos e timeline recente.

## Stack

- `React`
- `TypeScript`
- `Vite`

## Current Scope

- dashboard inicial de `mission control`
- integração com `GET /mission-control/overview`
- ação para `POST /demo/bootstrap`
- proxy local para o backend FastAPI durante o desenvolvimento

## Local Development

### 1. Start the backend

No projeto backend:

```bash
cd /Users/mariaizabelvieirapassos/Desktop/endurance_mission/endurance_mission
source /Users/mariaizabelvieirapassos/Desktop/endurance_mission/venv/bin/activate
AUTO_CREATE_TABLES=false alembic upgrade head
DATABASE_URL=sqlite:///./test.db AUTO_CREATE_TABLES=false uvicorn app.main:app --reload
```

### 2. Start the frontend

```bash
cd /Users/mariaizabelvieirapassos/Documents/New\ project/endurance-mission-control-ui
npm install
npm run dev
```

### 3. Open the app

- [http://127.0.0.1:5173](http://127.0.0.1:5173)

## Notes

- o frontend usa proxy do Vite para redirecionar `/api/*` para `http://127.0.0.1:8000`
- isso evita dor com `CORS` durante desenvolvimento local
- a próxima etapa natural é expandir o dashboard com painéis de subsistemas, command queue e visualização da timeline de missão
