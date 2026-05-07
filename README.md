# RentasAI

RentasAI is a live-ready, simulation-safe MVP for agentic mobility recovery in Malaysia. It observes transport and weather context, detects disruption impact, generates three deterministic recovery options, scores them without an LLM, validates safety, and uses OpenAI only to phrase the final structured explanation.

## What Is Included

- `backend/`: FastAPI, LangGraph sequential agent workflow, deterministic scenario engine, live API wrappers, PostgreSQL persistence, OpenAI explanation service.
- `frontend/`: Next.js, React, TypeScript, Tailwind CSS, Mapbox GL JS hackathon dashboard.
- `docker-compose.yml`: PostgreSQL plus backend service.
- `backend/app/db/schema.sql`: UUID and JSONB schema for trips, agent runs, route options, recommendations, operator events, API snapshots, and cached GTFS metadata.

## Modes

- `simulation`: no external APIs required. Always returns a full demo recommendation.
- `hybrid`: default judge mode. Uses live GTFS/weather when reachable and deterministic scenario disruption.
- `live`: attempts Malaysia public APIs and gracefully falls back if data is unavailable.

Prepared live endpoints:

- GTFS Static: Rapid Rail KL, MRT feeder, Rapid Bus KL, KTMB from `api.data.gov.my`
- GTFS Realtime: Rapid Bus MRT feeder and Rapid Bus KL vehicle-position feeds
- Weather: Malaysia forecast and warning APIs

Rail realtime is not assumed stable. Bus realtime is used as supporting evidence only.

## Reliability Guarantees

The judge demo is designed to keep working when optional dependencies fail:

- OpenAI missing or failing: backend uses a deterministic explanation template.
- Mapbox token missing or invalid: frontend shows a route preview and keeps all recommendation data visible.
- GTFS Static unavailable: backend uses built-in demo stop metadata.
- GTFS Realtime empty or malformed: backend marks realtime as fallback and keeps deterministic route recovery.
- Weather API unavailable: backend uses scenario weather and flood-risk values.
- PostgreSQL offline: `/api/trip/plan` still returns a full response and reports `persistence.database = error`.
- Live/hybrid graph failure: backend retries with simulation mode and records the fallback in `errors` and `agent_trace`.

For the most predictable presentation, use `hybrid` mode with `Heavy Rain + Bus Delay`.

## Environment

Backend:

```bash
cd rentasai/backend
copy .env.example .env
```

Set values as needed:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rentasai
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4.1-mini
APP_DEFAULT_MODE=hybrid
ENABLE_LIVE_APIS=true
```

Frontend:

```bash
cd rentasai/frontend
copy .env.local.example .env.local
```

Set:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
```

## Run Locally

Start PostgreSQL:

```bash
cd rentasai
docker compose up -d postgres
```

The app can still plan trips if PostgreSQL is not running; persistence will be marked as degraded in the API status panel.

Run backend:

```bash
cd rentasai/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Run frontend:

```bash
cd rentasai/frontend
npm install
npm run dev
```

Open:

- Frontend: `http://localhost:3000`
- Backend health: `http://localhost:8000/api/health`
- API docs: `http://localhost:8000/docs`

You can also run PostgreSQL and backend together:

```bash
cd rentasai
docker compose up --build
```

## Demo Steps

1. Open `http://localhost:3000`.
2. Keep mode on `hybrid`.
3. Keep preference on `rain_safe`.
4. Click `Heavy Rain + Bus Delay`.
5. Confirm the recommendation selects `E-hailing to nearest LRT, then rail`.
6. Point out the API status panel: `fallback` is acceptable and means the demo is using deterministic recovery data.
7. Show the recommendation card: it should highlight short e-hailing to rail, saved time, low walking, and rain safety.
8. Show the agent reasoning cards to demonstrate the full LangGraph workflow.
9. Show the operator dashboard for corridor-level operational impact.
10. Optional stress test: temporarily remove `OPENAI_API_KEY`, stop PostgreSQL, or omit `NEXT_PUBLIC_MAPBOX_TOKEN`; the demo should still return and display a full plan.

## Core API

Plan a trip:

```bash
curl -X POST http://localhost:8000/api/trip/plan ^
  -H "Content-Type: application/json" ^
  -d "{\"origin\":\"Wangsa Maju\",\"destination\":\"KL Sentral\",\"arrival_deadline\":\"08:45\",\"preference\":\"rain_safe\",\"scenario\":\"heavy_rain_bus_delay\",\"mode\":\"hybrid\"}"
```

Useful endpoints:

- `GET /`
- `GET /api/health`
- `POST /api/trip/plan`
- `GET /api/scenarios`
- `GET /api/dashboard/operator`
- `GET /api/live/stops/search?q=Wangsa`
- `GET /api/live/vehicles`
- `GET /api/live/weather`

## Notes For Judges

- The backend never uses OpenAI to calculate routes, scores, travel times, weather, or disruption facts.
- Route generation and scoring are deterministic.
- Simulation mode works offline.
- Hybrid mode remains demo-safe if live APIs fail.
- Mapbox token is read from `NEXT_PUBLIC_MAPBOX_TOKEN`; no secrets are hardcoded.

## Troubleshooting

- Backend unavailable in UI: start FastAPI with `uvicorn app.main:app --reload --port 8000` from `rentasai/backend`.
- `database: error`: start PostgreSQL with `docker compose up -d postgres`; planning still works without it.
- `openai: not_configured_template_fallback`: add `OPENAI_API_KEY` only if you want OpenAI phrasing. It is not required for the demo.
- Map not visible: set `NEXT_PUBLIC_MAPBOX_TOKEN`; otherwise the fallback route preview is expected.
- Live APIs show `fallback`: this is expected during outages, latency, malformed responses, or offline judging. The deterministic scenario engine remains active.
