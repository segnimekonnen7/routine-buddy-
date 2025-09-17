"""Simplified insights router for demo purposes."""

import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/insights", tags=["insights"])

# Demo habits data (same as in main.py)
demo_habits = [
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

@router.get("/habits/{habit_id}/success-prediction")
async def predict_habit_success(habit_id: str) -> Dict[str, Any]:
    """Predict likelihood of maintaining habit streak using simple analysis."""
    try:
        # Find habit
        habit = next((h for h in demo_habits if h["id"] == habit_id), None)
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
        
    except Exception as e:
        logger.error(f"Error generating success prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/habits/{habit_id}/optimal-reminder")
async def get_optimal_reminder_time(habit_id: str) -> Dict[str, Any]:
    """Get optimal reminder time based on simple analysis."""
    try:
        # Find habit
        habit = next((h for h in demo_habits if h["id"] == habit_id), None)
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
        
    except Exception as e:
        logger.error(f"Error analyzing optimal reminder time: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/habits/{habit_id}/completion-stats")
async def get_completion_stats(habit_id: str) -> Dict[str, Any]:
    """Get completion statistics for a habit."""
    try:
        # Find habit
        habit = next((h for h in demo_habits if h["id"] == habit_id), None)
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
        
    except Exception as e:
        logger.error(f"Error getting completion stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/habits/{habit_id}/recommendations")
async def get_habit_recommendations(habit_id: str) -> Dict[str, Any]:
    """Get personalized recommendations for a habit."""
    try:
        # Find habit
        habit = next((h for h in demo_habits if h["id"] == habit_id), None)
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
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
