from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import hash_password
from app.db.session import Base, engine, SessionLocal
from app.models.user import User
from app.models.customer import Customer
from app.routers import auth, customers , categories
from app.routers import tickets


def seed_admin():
    db = SessionLocal()

    try:
        existing = db.query(User).filter(User.email == "admin@crm.local").first()

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
    # Base.metadata.create_all(bind=engine)
    seed_admin()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="CRM Support API — Authentication & Customers only",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.r)
app.include_router(customers.r)
app.include_router(categories.router)
app.include_router(tickets.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
