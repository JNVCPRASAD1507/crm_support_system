# Resolve CRM & Customer Support Management System

EOD submission project built as a **monolithic full-stack application**.

**Backend:** FastAPI · SQLAlchemy · PostgreSQL · Pydantic · JWT · Alembic · Repository Pattern · Service Layer

**Frontend:** React + Vite · Axios · React Router · Lucide icons · custom React-Bits-inspired Spotlight cards

## Run

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
# set PostgreSQL DATABASE_URL in .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` and use `admin@crm.local / Admin@123` for the seeded development admin.

See `backend/README.md` for architecture, business rules, API groups, migrations, testing and Docker instructions.
