"""Database seed script for demo user and saved cities."""

from app.database import SessionLocal, init_db
from app import models


def seed_database():
    """Seed initial demo user, preferences, and saved cities."""
    init_db()
    db = SessionLocal()
    try:
        # Check if demo user already exists
        existing_user = db.query(models.User).filter(models.User.email == "rahul@mausam.app").first()
        if existing_user:
            print(f"Demo user already exists: {existing_user.name} (ID: {existing_user.id})")
            return existing_user.id

        # Create demo user
        user = models.User(
            name="Rahul Sharma",
            email="rahul@mausam.app"
        )
        db.add(user)
        db.flush()

        # Create preferences
        pref = models.UserPreference(
            user_id=user.id,
            units="metric",
            language="en",
            interests=["commute", "fitness"],
            sensitivities=["heat", "allergies"],
            commute_morning="08:30",
            commute_evening="18:00",
        )
        db.add(pref)

        # Create saved cities
        cities = [
            models.SavedCity(
                user_id=user.id,
                name="New Delhi",
                state="Delhi",
                country="India",
                lat=28.6139,
                lon=77.2090,
                is_favorite=True,
                display_order=0,
            ),
            models.SavedCity(
                user_id=user.id,
                name="Bengaluru",
                state="Karnataka",
                country="India",
                lat=12.9716,
                lon=77.5946,
                is_favorite=False,
                display_order=1,
            ),
            models.SavedCity(
                user_id=user.id,
                name="Mumbai",
                state="Maharashtra",
                country="India",
                lat=19.0760,
                lon=72.8777,
                is_favorite=False,
                display_order=2,
            ),
        ]
        db.add_all(cities)
        db.commit()
        print(f"Successfully seeded demo user '{user.name}' (ID: {user.id}) with {len(cities)} saved cities.")
        return user.id
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
