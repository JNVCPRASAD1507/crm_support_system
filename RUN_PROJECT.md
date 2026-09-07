# CRM Support System — Run Guide

## Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
Open http://localhost:5173

## Backend (local Python)
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```
API: http://localhost:8000 — docs: http://localhost:8000/docs

## Docker backend + PostgreSQL
From the project root, copy `.env.example` to `.env`, replace the example password and secret, then:
```bash
docker compose up --build
```
The compose service waits for PostgreSQL, applies Alembic migrations, and starts FastAPI.

## Frontend API connection
Set `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```
For production, use your HTTPS backend URL and set backend `CORS_ORIGINS` to the exact HTTPS frontend origin(s).

## Security note
Do not commit real `.env` files, database passwords, JWT secrets, or production credentials. HTTPS/TLS is normally terminated by your production host/reverse proxy; the application is configured to consume environment-specific HTTPS URLs.
