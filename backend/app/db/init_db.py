from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password


def seed_admin():
    db: Session = SessionLocal()

    try:
        existing_admin = (
            db.query(User)
            .filter(User.email == "admin@crm.local")
            .first()
        )

        if not existing_admin:
            admin = User(
                full_name="System Admin",
                email="admin@crm.local",
                password_hash=hash_password("Admin@123"),
                role="admin",
                is_active=True,
            )

            db.add(admin)
            db.commit()

            print("✅ Admin user created")
        else:
            print("ℹ️ Admin user already exists")

    except Exception as e:
        db.rollback()
        print(f"❌ Admin seed failed: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()