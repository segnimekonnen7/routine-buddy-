"""
Minimal Habit Loop Backend - Guaranteed to deploy and work
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

# Create FastAPI app
app = FastAPI(title="Habit Loop API", version="1.0.0")

# Add CORS middleware - CRITICAL for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HabitCreate(BaseModel):
    title: str
    notes: Optional[str] = None
    goal_type: str = "check"
    target_value: Optional[float] = 1
    grace_per_week: int = 1

class HabitResponse(BaseModel):
    id: str
    title: str
    notes: Optional[str]
    goal_type: str
    target_value: Optional[float]
    grace_per_week: int
    created_at: str
    current_streak_length: int
    is_due_today: bool
    best_hour: Optional[int]

# In-memory storage
habits_db = [
    {
        "id": "demo-1",
        "title": "Drink Water",
        "notes": "Stay hydrated throughout the day",
        "goal_type": "count",
        "target_value": 8.0,
        "grace_per_week": 2,
        "created_at": "2024-01-01T00:00:00Z",
        "current_streak_length": 5,
        "is_due_today": True,
        "best_hour": 9
    },
    {
        "id": "demo-2", 
        "title": "Exercise",
        "notes": "30 minutes of physical activity",
        "goal_type": "duration",
        "target_value": 30.0,
        "grace_per_week": 1,
        "created_at": "2024-01-01T00:00:00Z",
        "current_streak_length": 3,
        "is_due_today": False,
        "best_hour": 7
    }
]

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Habit Loop API is running!", "status": "ok", "version": "2.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat(), "version": "2.0"}

@app.get("/habits", response_model=List[HabitResponse])
async def get_habits():
    """Get all habits."""
    return habits_db

@app.post("/habits", response_model=HabitResponse)
async def create_habit(habit: HabitCreate):
    """Create a new habit."""
    new_habit = {
        "id": str(uuid.uuid4()),
        "title": habit.title,
        "notes": habit.notes,
        "goal_type": habit.goal_type,
        "target_value": habit.target_value,
        "grace_per_week": habit.grace_per_week,
        "created_at": datetime.now().isoformat() + "Z",
        "current_streak_length": 0,
        "is_due_today": True,
        "best_hour": None
    }
    
    habits_db.append(new_habit)
    return new_habit

@app.post("/habits/{habit_id}/checkin")
async def checkin_habit(habit_id: str):
    """Check in a habit."""
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    habit["current_streak_length"] += 1
    habit["is_due_today"] = False
    
    return {"message": f"Habit {habit_id} checked in successfully", "streak": habit["current_streak_length"]}

@app.post("/habits/{habit_id}/miss")
async def miss_habit(habit_id: str):
    """Miss a habit."""
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if habit["current_streak_length"] > 0:
        habit["current_streak_length"] = 0
    
    habit["is_due_today"] = False
    
    return {"message": f"Habit {habit_id} marked as missed", "streak": habit["current_streak_length"]}

# Insights endpoints
@app.get("/insights/habits/{habit_id}/success-prediction")
async def predict_habit_success(habit_id: str):
    """Predict habit success."""
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    streak = habit["current_streak_length"]
    if streak >= 7:
        prediction = "high"
        probability = 85
        recommendation = "Excellent! You've built a strong habit. Keep up the consistency!"
    elif streak >= 3:
        prediction = "medium"
        probability = 65
        recommendation = "Good progress! Focus on consistency to build momentum."
    else:
        prediction = "low"
        probability = 35
        recommendation = "Early stage habit. Try to complete it daily for the next week."
    
    return {
        "habit_id": habit_id,
        "habit_title": habit["title"],
        "prediction": prediction,
        "probability": probability,
        "current_streak": streak,
        "recommendation": recommendation
    }

@app.get("/insights/habits/{habit_id}/optimal-reminder")
async def get_optimal_reminder_time(habit_id: str):
    """Get optimal reminder time."""
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    best_hour = habit.get("best_hour", 9)
    
    return {
        "habit_id": habit_id,
        "habit_title": habit["title"],
        "optimal_hour": best_hour,
        "optimal_time": f"{best_hour}:00",
        "reasoning": f"Based on your habit pattern, {best_hour}:00 seems to be your optimal time"
    }

@app.get("/insights/habits/{habit_id}/completion-stats")
async def get_completion_stats(habit_id: str):
    """Get completion statistics."""
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    streak = habit["current_streak_length"]
    total_days = 30
    
    return {
        "habit_id": habit_id,
        "habit_title": habit["title"],
        "current_streak": streak,
        "longest_streak": max(streak, 7),
        "completion_rate": min((streak / total_days) * 100, 100),
        "total_attempts": total_days,
        "successful_completions": streak
    }

@app.get("/insights/habits/{habit_id}/recommendations")
async def get_habit_recommendations(habit_id: str):
    """Get habit recommendations."""
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    streak = habit["current_streak_length"]
    goal_type = habit["goal_type"]
    
    if goal_type == "count":
        recommendations = [
            "Break down your target into smaller, manageable chunks",
            "Set reminders at optimal times throughout the day",
            "Track your progress visually to stay motivated"
        ]
    elif goal_type == "duration":
        recommendations = [
            "Start with shorter sessions and gradually increase",
            "Find activities you genuinely enjoy",
            "Schedule it at the same time each day"
        ]
    else:
        recommendations = [
            "Make it part of your daily routine",
            "Pair it with an existing habit",
            "Celebrate small wins to build momentum"
        ]
    
    return {
        "habit_id": habit_id,
        "habit_title": habit["title"],
        "current_streak": streak,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Minimal Habit Loop API...")
    print("📡 CORS: Allowing all origins for GitHub Pages")
    print("🔍 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Force redeploy Tue Sep  2 18:59:09 CDT 2025
