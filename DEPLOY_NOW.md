# RentasAI emergency deployment guide

## Recommended fastest route: Render backend + Vercel frontend

### 1) Push the correct folder to GitHub
Push the folder that directly contains `backend/`, `frontend/`, `docker-compose.yml`, and `README.md`.
Do not push `frontend/node_modules`, `frontend/.next`, `backend/.env`, or `frontend/.env.local`.

```bash
cd rentasai
git init
git add .
git commit -m "ready for demo deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rentasai.git
git push -u origin main
```

### 2) Deploy backend on Render
Create a new Web Service from the GitHub repo.

Use these settings:

- Root Directory: `backend`
- Runtime/Language: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/api/health`

Environment variables:

```env
APP_DEFAULT_MODE=hybrid
ENABLE_LIVE_APIS=true
OPENAI_MODEL=gpt-4.1-mini
OPENAI_API_KEY=optional_for_demo
```

Skip PostgreSQL if you are rushing. The app still demos with persistence degraded.

After deploy, test:

```bash
curl https://YOUR_RENDER_BACKEND.onrender.com/api/health
```

### 3) Deploy frontend on Vercel
Import the same GitHub repo.

Use these settings:

- Root Directory: `frontend`
- Framework Preset: Next.js
- Install Command: `npm ci`
- Build Command: `npm run build`

Environment variables:

```env
NEXT_PUBLIC_API_URL=https://YOUR_RENDER_BACKEND.onrender.com/api
NEXT_PUBLIC_MAPBOX_TOKEN=optional_for_demo
```

Redeploy after setting/changing `NEXT_PUBLIC_API_URL`.

### 4) Final demo click path

1. Open the Vercel frontend URL.
2. Select `hybrid` mode.
3. Select preference `rain_safe`.
4. Click `Heavy Rain + Bus Delay`.
5. Show recommendation, API status panel, agent reasoning cards, and operator dashboard.

## Backup: single VPS with Docker Compose

Copy this patch's files into your project, replacing existing files where names match:

- `backend/Dockerfile`
- `frontend/package.json`
- `frontend/Dockerfile`
- `frontend/.dockerignore`
- `docker-compose.prod.yml`

Create a `.env` in the project root:

```env
POSTGRES_PASSWORD=strong_password_here
OPENAI_API_KEY=
ENABLE_LIVE_APIS=true
NEXT_PUBLIC_API_URL=http://YOUR_SERVER_IP:8000/api
NEXT_PUBLIC_MAPBOX_TOKEN=
```

Run:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

Open:

- Frontend: `http://YOUR_SERVER_IP:3000`
- Backend health: `http://YOUR_SERVER_IP:8000/api/health`
