"""
Simplified Habit Loop Backend - Guaranteed to work with GitHub Pages
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import os

# Create FastAPI app
app = FastAPI(
    title="Habit Loop API",
    description="Science-backed habit builder",
    version="1.0.0"
)

# Add CORS middleware - Allow all origins for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins to fix GitHub Pages issue
    allow_credentials=False,  # Disable credentials for wildcard origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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

# In-memory storage for demo
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
    },
    {
        "id": "demo-3",
        "title": "Read",
        "notes": "Read for personal development",
        "goal_type": "duration",
        "target_value": 20.0,
        "grace_per_week": 1,
        "created_at": "2024-01-01T00:00:00Z",
        "current_streak_length": 2,
        "is_due_today": True,
        "best_hour": 21
    }
]

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Habit Loop API is running!", "status": "ok", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/habits", response_model=List[HabitResponse])
async def get_habits():
    """Get all habits."""
    print(f"DEBUG: Serving {len(habits_db)} habits")
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
        "created_at": datetime.now().isoformat() + "Z",
        "current_streak_length": 0,
        "is_due_today": True,  # New habits are due today
        "best_hour": None
    }
    
    habits_db.append(new_habit)
    print(f"DEBUG: Created new habit: {new_habit['title']}")
    
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
    
    print(f"DEBUG: Habit {habit_id} checked in successfully")
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
    
    print(f"DEBUG: Habit {habit_id} marked as missed")
    return {"message": f"Habit {habit_id} marked as missed", "streak": habit["current_streak_length"]}

# Simple insights endpoints
@app.get("/insights/habits/{habit_id}/success-prediction")
async def predict_habit_success(habit_id: str):
    """Predict likelihood of maintaining habit streak."""
    # Find habit
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Simple prediction logic
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
        "recommendation": recommendation,
        "analysis": f"Based on your current {streak}-day streak"
    }

@app.get("/insights/habits/{habit_id}/optimal-reminder")
async def get_optimal_reminder_time(habit_id: str):
    """Get optimal reminder time."""
    # Find habit
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Simple reminder logic
    best_hour = habit.get("best_hour", 9)
    
    return {
        "habit_id": habit_id,
        "habit_title": habit["title"],
        "optimal_hour": best_hour,
        "optimal_time": f"{best_hour}:00",
        "reasoning": f"Based on your habit pattern, {best_hour}:00 seems to be your optimal time",
        "suggestion": f"Set a reminder for {best_hour}:00 to maximize your chances of completion"
    }

@app.get("/insights/habits/{habit_id}/completion-stats")
async def get_completion_stats(habit_id: str):
    """Get completion statistics for a habit."""
    # Find habit
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Simple stats
    streak = habit["current_streak_length"]
    total_days = 30  # Demo assumption
    
    return {
        "habit_id": habit_id,
        "habit_title": habit["title"],
        "current_streak": streak,
        "longest_streak": max(streak, 7),  # Demo assumption
        "completion_rate": min((streak / total_days) * 100, 100),
        "total_attempts": total_days,
        "successful_completions": streak,
        "analysis": f"You're currently on a {streak}-day streak. Keep it up!"
    }

@app.get("/insights/habits/{habit_id}/recommendations")
async def get_habit_recommendations(habit_id: str):
    """Get personalized recommendations for a habit."""
    # Find habit
    habit = next((h for h in habits_db if h["id"] == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Simple recommendations
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
    else:  # check
        recommendations = [
            "Make it part of your daily routine",
            "Pair it with an existing habit",
            "Celebrate small wins to build momentum"
        ]
    
    return {
        "habit_id": habit_id,
        "habit_title": habit["title"],
        "current_streak": streak,
        "recommendations": recommendations,
        "motivation": f"Great job on your {streak}-day streak! You're building a lasting habit."
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simplified Habit Loop API...")
    print("📡 CORS: Allowing all origins for GitHub Pages compatibility")
    print("🔍 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
