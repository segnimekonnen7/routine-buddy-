"""
ML-powered habit success predictor using trained scikit-learn model.
"""

import joblib
import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class HabitPredictor:
    """Production ML predictor for habit success."""
    
    def __init__(self, model_dir='backend/app/ml'):
        """
        Initialize predictor with trained model.
        
        Args:
            model_dir: Directory containing the trained model
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.feature_names = []
        self.load_model()
    
    def load_model(self):
        """Load trained model and metadata."""
        try:
            # Load model
            model_file = self.model_dir / 'habit_predictor.pkl'
            if model_file.exists():
                self.model = joblib.load(model_file)
                logger.info(f"✅ Loaded ML model from {model_file}")
            else:
                logger.warning(f"⚠️ Model file not found at {model_file}. Run train_model.py first.")
                self.model = None
                return
            
            # Load metadata
            metadata_file = self.model_dir / 'model_metadata.json'
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    self.feature_names = metadata.get('feature_names', [])
                    logger.info(f"📄 Loaded model metadata: {metadata.get('model_type')}")
            else:
                # Default feature names
                self.feature_names = [
                    'completion_rate',
                    'current_streak',
                    'consistency_score',
                    'avg_checkin_hour',
                    'days_since_start',
                    'grace_used_ratio'
                ]
        
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            self.model = None
    
    def extract_features(
        self,
        completion_rate: float,
        current_streak: int,
        consistency_score: float,
        avg_checkin_hour: int = 12,
        days_since_start: int = 30,
        grace_used_ratio: float = 0.5
    ) -> np.ndarray:
        """
        Extract features from habit data.
        
        Args:
            completion_rate: Fraction of days completed (0-1)
            current_streak: Current consecutive days
            consistency_score: Consistency metric (0-1)
            avg_checkin_hour: Average hour of check-ins (0-23)
            days_since_start: Days since habit started
            grace_used_ratio: Ratio of grace days used (0-1)
        
        Returns:
            Feature array ready for prediction
        """
        features = np.array([[
            completion_rate,
            current_streak,
            consistency_score,
            avg_checkin_hour,
            days_since_start,
            grace_used_ratio
        ]])
        
        return features
    
    def predict(
        self,
        completion_rate: float,
        current_streak: int,
        consistency_score: float,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Predict habit success probability.
        
        Args:
            completion_rate: Historical completion rate (0-1)
            current_streak: Current streak length
            consistency_score: Consistency score (0-1)
            **kwargs: Additional optional features
        
        Returns:
            Dictionary with prediction, probability, and confidence
        """
        if self.model is None:
            # Fallback to rule-based prediction
            return self._rule_based_prediction(
                completion_rate, current_streak, consistency_score
            )
        
        try:
            # Extract features
            features = self.extract_features(
                completion_rate=completion_rate,
                current_streak=current_streak,
                consistency_score=consistency_score,
                avg_checkin_hour=kwargs.get('avg_checkin_hour', 12),
                days_since_start=kwargs.get('days_since_start', 30),
                grace_used_ratio=kwargs.get('grace_used_ratio', 0.5)
            )
            
            # Get prediction
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0]
            
            # Extract probabilities
            prob_failure = probability[0]
            prob_success = probability[1]
            
            # Determine prediction category
            if prob_success >= 0.8:
                category = "high"
            elif prob_success >= 0.5:
                category = "medium"
            else:
                category = "low"
            
            result = {
                'prediction': category,
                'probability': float(prob_success * 100),  # Convert to percentage
                'confidence': float(max(prob_success, prob_failure) * 100),
                'will_succeed': bool(prediction == 1),
                'model_used': 'ml',
                'factors': {
                    'completion_rate': float(completion_rate * 100),
                    'current_streak': int(current_streak),
                    'consistency': float(consistency_score)
                }
            }
            
            logger.info(f"ML Prediction: {category} ({prob_success:.1%} success probability)")
            
            return result
        
        except Exception as e:
            logger.error(f"Error making ML prediction: {e}")
            # Fallback to rule-based
            return self._rule_based_prediction(
                completion_rate, current_streak, consistency_score
            )
    
    def _rule_based_prediction(
        self,
        completion_rate: float,
        current_streak: int,
        consistency_score: float
    ) -> Dict[str, Any]:
        """
        Fallback rule-based prediction (used when ML model unavailable).
        """
        # Calculate probability using simple rules
        base_prob = completion_rate * 100
        streak_bonus = min(20, current_streak * 2)
        consistency_bonus = consistency_score * 15
        
        probability = min(95, base_prob + streak_bonus + consistency_bonus)
        
        if probability >= 80:
            category = "high"
        elif probability >= 50:
            category = "medium"
        else:
            category = "low"
        
        return {
            'prediction': category,
            'probability': probability,
            'confidence': 70.0,  # Lower confidence for rule-based
            'will_succeed': probability >= 50,
            'model_used': 'rule_based',
            'factors': {
                'completion_rate': completion_rate * 100,
                'current_streak': current_streak,
                'consistency': consistency_score
            }
        }


# Global predictor instance
_predictor = None


def get_predictor() -> HabitPredictor:
    """Get or create global predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = HabitPredictor()
    return _predictor

