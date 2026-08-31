from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
import os
from app.core.config import settings
from app.db.session import Base, engine

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
    customers,
    tickets,
    users,
]:
    app.include_router(x.r)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
