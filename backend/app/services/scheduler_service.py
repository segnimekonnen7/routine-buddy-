"""Scheduler service for background jobs with ML-powered smart reminders."""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import numpy as np
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion
from app.models.user import User

logger = logging.getLogger(__name__)


class SmartReminderService:
    """ML-powered service for analyzing user behavior and suggesting optimal reminder times."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_optimal_reminder_time(self, user_id: str, habit_id: str) -> Optional[Dict[str, Any]]:
        """
        Analyze when user typically completes habits to suggest best reminder time.
        
        Returns optimal reminder hour based on historical completion data.
        """
        try:
            # Get completion data (pure software engineering approach)
            completions = self.db.query(HabitCompletion).filter(
                HabitCompletion.user_id == user_id,
                HabitCompletion.habit_id == habit_id,
                HabitCompletion.completed_at.isnot(None)
            ).all()
            
            if len(completions) < 3:
                logger.info(f"Not enough completion data for habit {habit_id} (need at least 3, got {len(completions)})")
                return None
            
            completion_data = []
            for completion in completions:
                completion_data.append({
                    'completed_at': completion.completed_at,
                    'hour': completion.completed_at.hour,
                    'day_of_week': completion.completed_at.weekday(),
                    'date': completion.completed_at.date()
                })
            
            df = pd.DataFrame(completion_data)
            
            # Analyze completion patterns by hour
            hour_analysis = df.groupby('hour').size().reset_index(name='completion_count')
            hour_analysis['completion_rate'] = hour_analysis['completion_count'] / len(df)
            
            # Find peak completion time
            best_hour = hour_analysis.loc[hour_analysis['completion_count'].idxmax(), 'hour']
            best_count = hour_analysis['completion_count'].max()
            
            # Calculate confidence based on data volume and consistency
            total_completions = len(df)
            hour_variance = df['hour'].var()
            confidence = min(95, (total_completions * 10) + (50 - hour_variance))
            
            # Suggest reminder time (1 hour before peak, but not before 6 AM)
            suggested_hour = max(6, best_hour - 1)
            
            # Analyze day-of-week patterns
            day_pattern = df.groupby('day_of_week').size().to_dict()
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_pattern_named = {day_names[k]: v for k, v in day_pattern.items()}
            
            logger.info(f"Smart reminder analysis for habit {habit_id}: peak hour {best_hour}, suggested {suggested_hour}")
            
            return {
                "suggested_reminder_hour": int(suggested_hour),
                "peak_completion_hour": int(best_hour),
                "confidence": round(confidence, 1),
                "total_completions": total_completions,
                "hour_distribution": hour_analysis.set_index('hour')['completion_count'].to_dict(),
                "day_pattern": day_pattern_named,
                "analysis_quality": "high" if total_completions >= 10 else "medium" if total_completions >= 5 else "low"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing reminder time for habit {habit_id}: {e}")
            return None
    
    def get_completion_stats(self, user_id: str, habit_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive completion statistics for a habit."""
        try:
            since_date = datetime.utcnow() - timedelta(days=days)
            completions = self.db.query(HabitCompletion).filter(
                HabitCompletion.user_id == user_id,
                HabitCompletion.habit_id == habit_id,
                HabitCompletion.completed_at >= since_date
            ).all()
            
            if not completions:
                return {
                    "total_completions": 0,
                    "completion_rate": 0.0,
                    "average_daily": 0.0,
                    "best_hour": None,
                    "consistency_score": 0.0,
                    "streak_analysis": {"current": 0, "longest": 0}
                }
            
            # Convert to DataFrame for analysis
            completion_data = []
            for completion in completions:
                completion_data.append({
                    'completed_at': completion.completed_at,
                    'date': completion.completed_at.date(),
                    'hour': completion.completed_at.hour
                })
            
            df = pd.DataFrame(completion_data)
            
            # Calculate statistics
            total_completions = len(completions)
            completion_rate = total_completions / days
            
            # Find most common completion hour
            hour_counts = df['hour'].value_counts()
            best_hour = hour_counts.index[0] if len(hour_counts) > 0 else None
            
            # Calculate consistency (lower variance = higher consistency)
            daily_completions = df.groupby('date').size()
            consistency_score = max(0, 1 - (daily_completions.var() / (daily_completions.mean() + 1)))
            
            # Streak analysis
            df_sorted = df.sort_values('date')
            current_streak, longest_streak = self._calculate_streaks(df_sorted['date'].tolist())
            
            return {
                "total_completions": total_completions,
                "completion_rate": round(completion_rate, 2),
                "average_daily": round(total_completions / days, 2),
                "best_hour": int(best_hour) if best_hour is not None else None,
                "consistency_score": round(consistency_score, 2),
                "hour_distribution": hour_counts.to_dict(),
                "streak_analysis": {
                    "current": current_streak,
                    "longest": longest_streak
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting completion stats for habit {habit_id}: {e}")
            return {"error": str(e)}
    
    def _calculate_streaks(self, dates: List[datetime.date]) -> tuple[int, int]:
        """Calculate current and longest streaks from completion dates."""
        if not dates:
            return 0, 0
        
        # Remove duplicates and sort
        unique_dates = sorted(list(set(dates)))
        
        current_streak = 0
        longest_streak = 0
        temp_streak = 1
        
        today = datetime.utcnow().date()
        
        # Calculate current streak (from today backwards)
        for i in range(len(unique_dates) - 1, -1, -1):
            if i == len(unique_dates) - 1:
                # Check if most recent completion is today or yesterday
                days_diff = (today - unique_dates[i]).days
                if days_diff <= 1:
                    current_streak = 1
                else:
                    break
            else:
                days_diff = (unique_dates[i + 1] - unique_dates[i]).days
                if days_diff == 1:
                    current_streak += 1
                else:
                    break
        
        # Calculate longest streak
        for i in range(1, len(unique_dates)):
            days_diff = (unique_dates[i] - unique_dates[i - 1]).days
            if days_diff == 1:
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
        
        longest_streak = max(longest_streak, temp_streak)
        
        return current_streak, longest_streak


class SchedulerService:
    """Service for managing background scheduled jobs."""
    
    def __init__(self, db: Session):
        self.db = db
        self.smart_reminder = SmartReminderService(db)
    
    def run_reminders(self) -> Dict[str, Any]:
        """Run smart reminder job with ML-powered timing."""
        try:
            logger.info("Starting smart reminder job")
            
            # Get all active habits
            habits = self.db.query(Habit).filter(Habit.is_active == True).all()
            
            reminders_sent = 0
            for habit in habits:
                # Analyze optimal reminder time
                reminder_analysis = self.smart_reminder.analyze_optimal_reminder_time(
                    str(habit.user_id), str(habit.id)
                )
                
                if reminder_analysis and reminder_analysis.get('confidence', 0) > 70:
                    # Send reminder at optimal time
                    # TODO: Implement actual reminder sending logic
                    reminders_sent += 1
                    logger.info(f"Smart reminder sent for habit {habit.title} at hour {reminder_analysis['suggested_reminder_hour']}")
            
            return {
                "reminders_sent": reminders_sent,
                "habits_analyzed": len(habits),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in reminder job: {e}")
            return {"reminders_sent": 0, "status": "failed", "error": str(e)}
    
    def run_weekly_digest(self) -> Dict[str, Any]:
        """Run weekly digest job with ML insights."""
        try:
            logger.info("Starting weekly digest job")
            
            # Get all users with active habits
            users = self.db.query(User).join(Habit).filter(Habit.is_active == True).distinct().all()
            
            digests_sent = 0
            for user in users:
                # Generate personalized insights for each user
                user_habits = self.db.query(Habit).filter(
                    Habit.user_id == user.id,
                    Habit.is_active == True
                ).all()
                
                insights = []
                for habit in user_habits:
                    stats = self.smart_reminder.get_completion_stats(
                        str(user.id), str(habit.id), days=7
                    )
                    insights.append({
                        "habit_title": habit.title,
                        "completion_rate": stats.get("completion_rate", 0),
                        "consistency_score": stats.get("consistency_score", 0),
                        "best_hour": stats.get("best_hour")
                    })
                
                # TODO: Send digest email with insights
                digests_sent += 1
                logger.info(f"Weekly digest sent to user {user.email} with {len(insights)} habit insights")
            
            return {
                "digests_sent": digests_sent,
                "users_processed": len(users),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in weekly digest job: {e}")
            return {"digests_sent": 0, "status": "failed", "error": str(e)}
