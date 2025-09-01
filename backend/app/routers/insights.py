"""Insights router with ML-powered features."""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.habit import Habit
from app.routers.auth import get_current_user
from app.services.prediction_service import PredictionService
from app.services.scheduler_service import SmartReminderService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/habits/{habit_id}/success-prediction")
async def predict_habit_success(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict likelihood of maintaining habit streak using ML-like analysis.
    
    Uses completion rate, streak length, and consistency for prediction.
    Returns prediction (high/medium/low), probability, and recommendations.
    """
    try:
        # Verify habit belongs to user
        habit = db.query(Habit).filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id
        ).first()
        
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        
        # Get prediction using ML-like analysis
        prediction_service = PredictionService(db)
        result = prediction_service.predict_habit_success(str(habit_id))
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        logger.info(f"Success prediction generated for habit {habit.title}: {result['prediction']}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating success prediction for habit {habit_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/habits/{habit_id}/optimal-reminder")
async def get_optimal_reminder_time(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get optimal reminder time based on completion patterns using ML analysis.
    
    Analyzes user's historical completion data to suggest best reminder time.
    """
    try:
        # Verify habit belongs to user
        habit = db.query(Habit).filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id
        ).first()
        
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        
        # Get optimal reminder time using ML analysis
        reminder_service = SmartReminderService(db)
        result = reminder_service.analyze_optimal_reminder_time(
            str(current_user.id), 
            str(habit_id)
        )
        
        if not result:
            return {
                "message": "Not enough data for analysis. Complete the habit a few more times to get personalized insights.",
                "min_completions_needed": 3,
                "current_completions": 0
            }
        
        logger.info(f"Optimal reminder analysis generated for habit {habit.title}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing optimal reminder time for habit {habit_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/habits/{habit_id}/completion-stats")
async def get_completion_stats(
    habit_id: uuid.UUID,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive completion statistics for a habit using ML analysis.
    
    Returns detailed statistics including completion rates, patterns, and streaks.
    """
    try:
        # Verify habit belongs to user
        habit = db.query(Habit).filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id
        ).first()
        
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        
        # Validate days parameter
        if days < 1 or days > 365:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
        
        # Get completion stats using ML analysis
        reminder_service = SmartReminderService(db)
        result = reminder_service.get_completion_stats(
            str(current_user.id), 
            str(habit_id), 
            days
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        logger.info(f"Completion stats generated for habit {habit.title} over {days} days")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting completion stats for habit {habit_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/habits/{habit_id}/insights")
async def get_habit_insights(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive insights for a habit including trends and patterns.
    
    Uses ML-like analysis to provide detailed insights about habit performance.
    """
    try:
        # Verify habit belongs to user
        habit = db.query(Habit).filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id
        ).first()
        
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        
        # Get comprehensive insights using ML analysis
        prediction_service = PredictionService(db)
        result = prediction_service.get_habit_insights(str(habit_id))
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        logger.info(f"Comprehensive insights generated for habit {habit.title}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting habit insights for habit {habit_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/habits/{habit_id}/recommendations")
async def get_habit_recommendations(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized recommendations for improving habit success.
    
    Combines multiple ML analyses to provide actionable recommendations.
    """
    try:
        # Verify habit belongs to user
        habit = db.query(Habit).filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id
        ).first()
        
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        
        # Get prediction and reminder analysis
        prediction_service = PredictionService(db)
        reminder_service = SmartReminderService(db)
        
        prediction = prediction_service.predict_habit_success(str(habit_id))
        reminder_analysis = reminder_service.analyze_optimal_reminder_time(
            str(current_user.id), str(habit_id)
        )
        
        # Combine insights for comprehensive recommendations
        recommendations = []
        
        if "error" not in prediction:
            recommendations.append({
                "type": "success_prediction",
                "priority": "high" if prediction["prediction"] == "low" else "medium",
                "title": "Success Prediction",
                "message": prediction["recommendation"],
                "probability": prediction["probability"]
            })
        
        if reminder_analysis and reminder_analysis.get("confidence", 0) > 70:
            recommendations.append({
                "type": "reminder_timing",
                "priority": "medium",
                "title": "Optimal Reminder Time",
                "message": f"Set your reminder for {reminder_analysis['suggested_reminder_hour']}:00 based on your completion patterns",
                "suggested_hour": reminder_analysis["suggested_reminder_hour"],
                "confidence": reminder_analysis["confidence"]
            })
        
        # Add general recommendations based on habit type
        if habit.goal_type == "duration" and habit.target_value and habit.target_value > 60:
            recommendations.append({
                "type": "goal_adjustment",
                "priority": "low",
                "title": "Goal Adjustment",
                "message": "Consider breaking down long duration goals into smaller chunks for better consistency"
            })
        
        logger.info(f"Generated {len(recommendations)} recommendations for habit {habit.title}")
        
        return {
            "habit_title": habit.title,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendations for habit {habit_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
