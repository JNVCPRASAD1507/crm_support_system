from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
from app.core.background import sla_monitor
import os
from app.core.config import settings
from app.db.session import Base, engine
from app.db.init_db import seed_admin
from app.services.sla_service import seed_slas
from app.routers import (
    auth,
    customers,
    categories,
    tickets,
    comments,
    attachments,
    notifications,
    sla,
    dashboard,
    audit_logs,
    users,
)


@asynccontextmanager
async def lifespan(app):
    # Alembic is the preferred schema manager; create_all makes a first local run convenient.
    Base.metadata.create_all(bind=engine)
    seed_admin()
    from sqlalchemy.orm import Session

    with Session(engine) as db:
        seed_slas(db)
    os.makedirs(settings.upload_dir, exist_ok=True)
    task = asyncio.create_task(sla_monitor())
    yield
    task.cancel()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-style monolithic CRM & customer support API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
for x in [
    auth,
    customers,
    categories,
    tickets,
    comments,
    attachments,
    notifications,
    sla,
    dashboard,
    audit_logs,
    users,
]:
    app.include_router(x.r)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
