# Radian · AI-Native Business OS

Foundation monorepo for Radian. The first milestone provides a reusable dark enterprise shell, typed frontend, modular FastAPI service, health check, and local PostgreSQL/Redis services.

## Run locally

1. Copy `.env.example` to `.env` and add Clerk keys from the Clerk dashboard. Configure the Clerk JWT issuer and JWKS URL for FastAPI verification.
2. Start services: `docker compose up -d`.
3. Backend: `cd backend; python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -r requirements.txt; uvicorn app.main:app --reload --port 8000`.
4. Frontend: `cd frontend; npm install; npm run dev`.
5. Open http://localhost:3000 and verify http://localhost:8000/health.

Clerk handles authentication and organization membership; Radian's PostgreSQL database stores application-specific profiles, roles, and business data.

