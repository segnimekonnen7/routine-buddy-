"""Main FastAPI application."""

import logging
import socket
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

from app.core.config import settings
from app.routers import insights

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_free_port():
    """Find a free port automatically."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

# Create FastAPI app
app = FastAPI(
    title="Habit Loop API",
    description="Science-backed habit builder with adaptive reminders",
    version="1.0.0"
)

# Add CORS middleware with explicit origins for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now to fix the issue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HabitCreate(BaseModel):
    title: str
    notes: Optional[str] = None
    schedule_json: Dict[str, Any]
    goal_type: str
    target_value: Optional[float] = None
    grace_per_week: int = 1
    timezone: str = "UTC"

class HabitResponse(BaseModel):
    id: str
    title: str
    notes: Optional[str]
    goal_type: str
    target_value: Optional[float]
    grace_per_week: int
    timezone: str
    created_at: str
    current_streak_length: int
    is_due_today: bool
    best_hour: Optional[int]

# In-memory storage for demo
habits_db = [
    {
        "id": "demo-1",
        "title": "Drink Water",
        "notes": "Stay hydrated",
        "goal_type": "count",
        "target_value": 8,
        "grace_per_week": 2,
        "timezone": "UTC",
        "created_at": "2024-01-01T00:00:00Z",
        "current_streak_length": 5,
        "is_due_today": True,
        "best_hour": 9
    },
    {
        "id": "demo-2", 
        "title": "Exercise",
        "notes": "30 minutes daily",
        "goal_type": "duration",
        "target_value": 30,
        "grace_per_week": 1,
        "timezone": "UTC",
        "created_at": "2024-01-01T00:00:00Z",
        "current_streak_length": 3,
        "is_due_today": False,
        "best_hour": 7
    }
]

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/habits", response_model=List[HabitResponse])
async def get_habits():
    """Get all habits."""
    return habits_db

@app.post("/habits", response_model=HabitResponse)
async def create_habit(habit: HabitCreate):
    """Create a new habit."""
    # Validate goal_type
    if habit.goal_type not in ["check", "count", "duration"]:
        raise HTTPException(status_code=400, detail="goal_type must be 'check', 'count', or 'duration'")
    
    # Create new habit
    new_habit = {
        "id": str(uuid.uuid4()),
        "title": habit.title,
        "notes": habit.notes,
        "goal_type": habit.goal_type,
        "target_value": habit.target_value,
        "grace_per_week": habit.grace_per_week,
        "timezone": habit.timezone,
        "created_at": datetime.now().isoformat() + "Z",
        "current_streak_length": 0,
        "is_due_today": True,  # New habits are due today
        "best_hour": None
    }
    
    habits_db.append(new_habit)
    logger.info(f"Created new habit: {new_habit['title']}")
    
    return new_habit

@app.post("/habits/{habit_id}/checkin")
async def checkin_habit(habit_id: str):
    """Check in a habit."""
    # Find habit
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Update streak
    habit["current_streak_length"] += 1
    habit["is_due_today"] = False  # Mark as completed for today
    
    logger.info(f"Habit {habit_id} checked in successfully")
    return {"message": f"Habit {habit_id} checked in successfully", "streak": habit["current_streak_length"]}

@app.post("/habits/{habit_id}/miss")
async def miss_habit(habit_id: str):
    """Miss a habit."""
    # Find habit
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Reset streak if it was > 0
    if habit["current_streak_length"] > 0:
        habit["current_streak_length"] = 0
    
    habit["is_due_today"] = False  # Mark as missed for today
    
    logger.info(f"Habit {habit_id} marked as missed")
    return {"message": f"Habit {habit_id} marked as missed", "streak": habit["current_streak_length"]}

# Include insights router for ML features
app.include_router(insights.router)

if __name__ == "__main__":
    import uvicorn
    
    # Find a free port automatically
    port = find_free_port()
    
    print("🚀 Starting Habit Loop API Server...")
    print(f"📡 Server running on: http://127.0.0.1:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"🔍 Interactive API: http://localhost:{port}/redoc")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=port)
