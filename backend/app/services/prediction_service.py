"""Prediction service for habit success forecasting using ML-like data analysis."""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion

logger = logging.getLogger(__name__)


class PredictionService:
    """Service for predicting habit success and providing recommendations using statistical analysis."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_recent_completions(self, habit_id: str, days: int = 30) -> List[HabitCompletion]:
        """Get recent completions for a habit within specified days."""
        try:
            since_date = datetime.utcnow() - timedelta(days=days)
            return self.db.query(HabitCompletion).filter(
                HabitCompletion.habit_id == habit_id,
                HabitCompletion.completed_at >= since_date
            ).order_by(HabitCompletion.completed_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting recent completions for habit {habit_id}: {e}")
            return []
    
    def calculate_current_streak(self, completions: List[HabitCompletion]) -> int:
        """Calculate current streak length from completion data."""
        if not completions:
            return 0
        
        try:
            # Convert to pandas for easier analysis
            completion_dates = [c.completed_at.date() for c in completions]
            df = pd.DataFrame({'date': completion_dates})
            df = df.drop_duplicates().sort_values('date', ascending=False)
            
            if df.empty:
                return 0
            
            current_streak = 0
            today = datetime.utcnow().date()
            
            # Check if most recent completion is today or yesterday
            most_recent = df.iloc[0]['date']
            days_diff = (today - most_recent).days
            
            if days_diff <= 1:
                current_streak = 1
                
                # Count consecutive days backwards
                for i in range(1, len(df)):
                    prev_date = df.iloc[i-1]['date']
                    curr_date = df.iloc[i]['date']
                    if (prev_date - curr_date).days == 1:
                        current_streak += 1
                    else:
                        break
            
            return current_streak
            
        except Exception as e:
            logger.error(f"Error calculating current streak: {e}")
            return 0
    
    def calculate_consistency(self, completions: List[HabitCompletion]) -> float:
        """Calculate consistency score based on completion patterns."""
        if not completions:
            return 0.0
        
        try:
            # Group completions by day
            completion_dates = [c.completed_at.date() for c in completions]
            df = pd.DataFrame({'date': completion_dates})
            daily_completions = df.groupby('date').size()
            
            if len(daily_completions) < 2:
                return 1.0 if len(daily_completions) == 1 else 0.0
            
            # Calculate variance in daily completion counts
            mean_completions = daily_completions.mean()
            variance = daily_completions.var()
            
            # Consistency score (lower variance = higher consistency)
            # Normalize by mean to get relative consistency
            consistency = max(0, 1 - (variance / (mean_completions + 1)))
            
            return round(consistency, 2)
            
        except Exception as e:
            logger.error(f"Error calculating consistency: {e}")
            return 0.0
    
    def predict_habit_success(self, habit_id: str) -> Dict[str, Any]:
        """
        Predict likelihood of maintaining habit streak using ML-like analysis.
        
        Uses completion rate, streak length, and consistency for prediction.
        Returns prediction (high/medium/low), probability, and recommendations.
        """
        try:
            # Get habit and recent completions
            habit = self.db.query(Habit).filter(Habit.id == habit_id).first()
            if not habit:
                return {"error": "Habit not found"}
            
            completions = self.get_recent_completions(habit_id, days=30)
            
            if not completions:
                return {
                    "prediction": "low",
                    "probability": 10.0,
                    "factors": {
                        "completion_rate": 0.0,
                        "current_streak": 0,
                        "consistency": 0.0
                    },
                    "recommendation": "Start building your habit! Complete it a few times to get personalized insights."
                }
            
            # Calculate key metrics
            completion_rate = len(completions) / 30
            streak_length = self.calculate_current_streak(completions)
            consistency_score = self.calculate_consistency(completions)
            
            # ML-like prediction using rule-based logic with statistical analysis
            prediction, probability = self._calculate_prediction(
                completion_rate, streak_length, consistency_score
            )
            
            # Generate personalized recommendation
            recommendation = self.generate_recommendation(prediction, habit, completion_rate, streak_length)
            
            logger.info(f"Success prediction for habit {habit.title}: {prediction} ({probability}%)")
            
            return {
                "prediction": prediction,
                "probability": round(probability, 1),
                "factors": {
                    "completion_rate": round(completion_rate * 100, 1),
                    "current_streak": streak_length,
                    "consistency": consistency_score
                },
                "recommendation": recommendation,
                "analysis_quality": "high" if len(completions) >= 10 else "medium" if len(completions) >= 5 else "low"
            }
            
        except Exception as e:
            logger.error(f"Error predicting habit success for {habit_id}: {e}")
            return {"error": str(e)}
    
    def _calculate_prediction(self, completion_rate: float, streak_length: int, consistency: float) -> tuple[str, float]:
        """Calculate prediction and probability using statistical analysis."""
        
        # Base probability from completion rate
        base_probability = completion_rate * 100
        
        # Streak bonus (longer streaks = higher success probability)
        streak_bonus = min(20, streak_length * 2)
        
        # Consistency bonus (more consistent = higher success probability)
        consistency_bonus = consistency * 15
        
        # Calculate final probability
        probability = min(95, base_probability + streak_bonus + consistency_bonus)
        
        # Determine prediction category
        if probability >= 80:
            prediction = "high"
        elif probability >= 50:
            prediction = "medium"
        else:
            prediction = "low"
        
        return prediction, probability
    
    def generate_recommendation(self, prediction: str, habit: Habit, completion_rate: float, streak_length: int) -> str:
        """Generate personalized recommendations based on prediction and habit data."""
        
        if prediction == "high":
            if completion_rate >= 0.9:
                return f"Excellent work with {habit.title}! You're maintaining a strong habit. Consider adding a new habit to build momentum."
            else:
                return f"Great progress with {habit.title}! You're on track to success. Keep up the consistency."
        
        elif prediction == "medium":
            if completion_rate < 0.6:
                return f"Good start with {habit.title}. Try setting a daily reminder to improve consistency. Consider reducing the target if it feels too difficult."
            elif streak_length < 7:
                return f"You're building momentum with {habit.title}. Focus on maintaining your current streak for a full week."
            else:
                return f"Solid progress with {habit.title}. You have a good foundation - try to increase your completion rate slightly."
        
        else:  # low prediction
            if completion_rate < 0.3:
                return f"Consider breaking {habit.title} into smaller, more manageable steps. Start with just 2-3 times per week."
            elif streak_length == 0:
                return f"Don't give up on {habit.title}! Try adjusting the timing or reducing the target value. Every small step counts."
            else:
                return f"Keep working on {habit.title}. Focus on consistency over perfection. Even small improvements matter."
    
    def get_habit_insights(self, habit_id: str) -> Dict[str, Any]:
        """Get comprehensive insights for a habit including trends and patterns."""
        try:
            habit = self.db.query(Habit).filter(Habit.id == habit_id).first()
            if not habit:
                return {"error": "Habit not found"}
            
            # Get completions for different time periods
            completions_7d = self.get_recent_completions(habit_id, days=7)
            completions_30d = self.get_recent_completions(habit_id, days=30)
            
            # Calculate trends
            weekly_rate = len(completions_7d) / 7
            monthly_rate = len(completions_30d) / 30
            
            # Trend analysis
            if weekly_rate > monthly_rate * 1.1:
                trend = "improving"
            elif weekly_rate < monthly_rate * 0.9:
                trend = "declining"
            else:
                trend = "stable"
            
            # Time pattern analysis
            if completions_30d:
                completion_hours = [c.completed_at.hour for c in completions_30d]
                df_hours = pd.DataFrame({'hour': completion_hours})
                hour_distribution = df_hours['hour'].value_counts().to_dict()
                most_common_hour = max(hour_distribution.items(), key=lambda x: x[1])[0] if hour_distribution else None
            else:
                hour_distribution = {}
                most_common_hour = None
            
            return {
                "habit_title": habit.title,
                "trend": trend,
                "weekly_completion_rate": round(weekly_rate, 2),
                "monthly_completion_rate": round(monthly_rate, 2),
                "most_common_hour": most_common_hour,
                "hour_distribution": hour_distribution,
                "total_completions_30d": len(completions_30d),
                "current_streak": self.calculate_current_streak(completions_30d),
                "consistency_score": self.calculate_consistency(completions_30d)
            }
            
        except Exception as e:
            logger.error(f"Error getting habit insights for {habit_id}: {e}")
            return {"error": str(e)}
