"""
Simple JSON-based database backend for Habit Loop.
This provides persistent storage without requiring complex database setup.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class SimpleDB:
    """Simple JSON-based database."""
    
    def __init__(self, db_file: str = "habits.json"):
        self.db_file = db_file
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"habits": []}
        return {"habits": []}
    
    def _save(self):
        """Save data to JSON file."""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_all_habits(self) -> List[Dict[str, Any]]:
        """Get all habits."""
        return self.data.get("habits", [])
    
    def create_habit(self, habit: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new habit."""
        habits = self.data.get("habits", [])
        habits.append(habit)
        self.data["habits"] = habits
        self._save()
        return habit
    
    def update_habit(self, habit_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a habit."""
        habits = self.data.get("habits", [])
        for habit in habits:
            if habit["id"] == habit_id:
                habit.update(updates)
                self.data["habits"] = habits
                self._save()
                return habit
        return None
    
    def get_habit(self, habit_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific habit."""
        habits = self.data.get("habits", [])
        return next((h for h in habits if h["id"] == habit_id), None)


# Initialize database
db = SimpleDB()

