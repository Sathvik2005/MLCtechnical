# CodeCity Life — A Living Developer World

CodeCity Life transforms developer profiles into a warm 3D village where residents (users), homes (profile summary), and buildings (repositories) are explorable.

## Monorepo Structure

- `backend/` FastAPI API, AI services, Mongo persistence, WebSocket presence.
- `frontend/` React + Vite + Three.js experience.

## Features

- GitHub + LeetCode profile fetch and normalization.
- AI-generated home metadata, repo building design, and mentor insights (OpenAI).
- Village-like 3D world with movement (WASD) and click interactions.
- Basic multiplayer position broadcast over WebSocket.
- MongoDB storage for generated worlds.

## Backend Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export MONGO_URI='mongodb+srv://...'
export OPENAI_API_KEY='sk-...'
# optional
export GITHUB_TOKEN='ghp_...'
export REDIS_URL='redis://localhost:6379/0'
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

## Frontend Setup

```bash
cd frontend
npm install
export VITE_API_URL='http://localhost:10000'
npm run dev
```

## API Endpoints

- `GET /leetcode/{username}`
- `GET /github/{username}`
- `POST /generate-world`
- `GET /world/{username}`
- `WS /ws/world/{world_id}`

## Data Model

```json
{
  "username": "string",
  "platform": ["github", "leetcode"],
  "problems_solved": 0,
  "repos": [],
  "skills": [],
  "languages": {},
  "activity": {},
  "rank": "string"
}
```

## Deployment

### Backend (Render)

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- Environment vars: `MONGO_URI`, `OPENAI_API_KEY`, `GITHUB_TOKEN` (optional), `REDIS_URL` (optional).

### Frontend (Vercel)

- Framework preset: Vite
- Build command: `npm run build`
- Output directory: `dist`
- Environment vars: `VITE_API_URL`

## Notes

- Repositories are capped to 15 for rendering performance.
- Geometry stays simple for smoother FPS on low-end devices.
- AI outputs are cached in Redis (if configured) or memory fallback.
