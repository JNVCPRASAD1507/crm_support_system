
from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import Base, engine, SessionLocal

from app.models.user import User
from app.models.customer import Customer

from app.routers import auth, customers, categories
from app.routers import tickets
from app.routers.ticket_comments import router as ticket_comments_router
from app.routers import ticket_attachments
from app.routers.notifications import router as notifications_router
from app.routers import slas
from app.routers import dashboard
from app.routers.audit_logs import router as audit_logs_router

from app.services.sla_monitor_scheduler import run_sla_monitor


def seed_admin():
    db = SessionLocal()

    try:
        existing = (
            db.query(User)
            .filter(
                User.email == "admin@crm.local"
            )
            .first()
        )

        if existing:
            return

        admin = User(
            full_name="System Administrator",
            email="admin@crm.local",
            password_hash=hash_password("Admin@123"),
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()

    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Seed default administrator
    # Base.metadata.create_all(bind=engine)
    seed_admin()

    # Start background SLA monitor
    sla_monitor_task = asyncio.create_task(
        run_sla_monitor()
    )

    try:
        yield

    finally:
        # Stop SLA monitor when application shuts down
        sla_monitor_task.cancel()

        try:
            await sla_monitor_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="CRM Support API",
    lifespan=lifespan,
)


# ============================================================
# CORS
# ============================================================


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================


app.include_router(auth.r)
app.include_router(customers.r)
app.include_router(categories.router)
app.include_router(tickets.router)
app.include_router(ticket_comments_router)
app.include_router(ticket_attachments.router)
app.include_router(notifications_router)
app.include_router(slas.router)
app.include_router(dashboard.router)
app.include_router(audit_logs_router)


# ============================================================
# HEALTH CHECK
# ============================================================


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }
