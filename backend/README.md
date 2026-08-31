# Resolve — CRM & Customer Support Management System

A production-style **monolithic FastAPI + PostgreSQL** CRM/support backend with a realistic React frontend. The code intentionally keeps domain concerns separated inside one deployable application.

## Architecture

```text
backend/app/
├── core/           # config, JWT security, dependencies, background monitoring
├── db/             # SQLAlchemy session and startup seeding
├── models/         # database entities and relationships
├── schemas/        # Pydantic request/response contracts
├── repositories/   # data-access abstractions
├── services/       # business rules, SLA, notifications, auditing
├── routers/        # REST API endpoints
└── utils/          # reusable helpers

frontend/src/
├── api/            # Axios client + endpoint modules
├── components/     # reusable UI components
├── context/        # authentication state
├── layouts/        # application shell/navigation
└── pages/          # dashboard, tickets, customers, categories, agents, notifications
```

## Roles
- **Admin:** global management, agents, categories, customers, tickets, SLA and audit access.
- **Support Agent:** assigned-ticket workflow, customer/ticket communication and attachments.
- **Customer:** own tickets, comments, attachments and customer dashboard.

## Backend setup

1. Create PostgreSQL database `crm_support`.
2. Copy `.env.example` to `.env` and update `DATABASE_URL` and `SECRET_KEY`.
3. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start API:

```bash
uvicorn app.main:app --reload
```

Swagger: `http://localhost:8000/docs`

The development startup also creates the schema if needed and seeds:
- Admin: `admin@crm.local`
- Password: `Admin@123`
- SLA: Low 48h, Medium 24h, High 8h, Critical 2h

Change the demo password before any real deployment.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The frontend reads `VITE_API_URL` from `.env` and defaults to `http://localhost:8000`.

## Docker

From the project root:

```bash
copy backend\\.env.example backend\\.env
docker compose up --build
```

Set `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/crm_support` in the backend `.env` for Docker.

## Key API groups

- `/auth`
- `/users`
- `/customers`
- `/categories`
- `/tickets`
- `/tickets/{ticket_id}/comments`
- `/tickets/{ticket_id}/attachments`
- `/notifications`
- `/sla`
- `/dashboard`
- `/audit-logs`

## Business rules implemented

JWT authentication, RBAC, customer isolation, assigned-agent isolation, inactive-agent protection, valid ticket state transitions, closed/cancelled immutability, comment ownership rules, duplicate category prevention, attachment validation, SLA deadlines/statuses, notifications, audit logs, search/filter/pagination, SQL relationships/indexes, Alembic migration, and a continuous background SLA monitor.

## Testing

```bash
pytest -q
```

The included tests cover the core status-transition matrix. Add API/integration tests with a dedicated test PostgreSQL database before production deployment.
