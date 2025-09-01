"""Demo data seeding script."""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion


def seed_demo_data():
    """Seed demo data for development."""
    db = SessionLocal()
    
    try:
        # Create demo user
        demo_user = db.query(User).filter(User.email == "demo@habitloop.local").first()
        if not demo_user:
            demo_user = User(
                email="demo@habitloop.local",
                name="Demo User"
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
        
        # Create demo habits
        habits_data = [
            {
                "title": "Drink Water",
                "notes": "Stay hydrated throughout the day",
                "goal_type": "count",
                "target_value": 8.0,
                "grace_per_week": 2,
                "schedule_json": {"days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
            },
            {
                "title": "Exercise",
                "notes": "30 minutes of physical activity",
                "goal_type": "duration",
                "target_value": 30.0,
                "grace_per_week": 1,
                "schedule_json": {"days": ["monday", "wednesday", "friday"]}
            },
            {
                "title": "Read",
                "notes": "Read for personal development",
                "goal_type": "duration",
                "target_value": 20.0,
                "grace_per_week": 1,
                "schedule_json": {"days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
            }
        ]
        
        for habit_data in habits_data:
            existing_habit = db.query(Habit).filter(
                Habit.user_id == demo_user.id,
                Habit.title == habit_data["title"]
            ).first()
            
            if not existing_habit:
                habit = Habit(
                    user_id=demo_user.id,
                    **habit_data
                )
                db.add(habit)
                db.commit()
                db.refresh(habit)
                
                # Add some demo completions
                for i in range(5):
                    completion_date = datetime.utcnow() - timedelta(days=i)
                    completion = HabitCompletion(
                        user_id=demo_user.id,
                        habit_id=habit.id,
                        completed_at=completion_date,
                        value=habit_data["target_value"]
                    )
                    db.add(completion)
        
        db.commit()
        print("✅ Demo data seeded successfully")
        
    except Exception as e:
        print(f"❌ Error seeding demo data: {e}")
        db.rollback()
    finally:
        db.close()
