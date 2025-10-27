#!/usr/bin/env python3
"""
My personal test script for the habit prediction model.
Test the accuracy and make individual predictions.
"""

import sys
sys.path.insert(0, 'backend')

from app.ml.predictor import HabitPredictor
from app.ml.train_model import HabitMLTrainer
import pandas as pd

def test_my_model():
    """Test the model with my own scenarios."""
    print("🧪 MY PERSONAL HABIT PREDICTION TEST")
    print("=" * 50)
    
    # Load the predictor
    predictor = HabitPredictor()
    
    if predictor.model is None:
        print("❌ Model not found! Run train_model.py first.")
        return
    
    print("✅ Model loaded successfully!")
    
    # Test different scenarios
    test_cases = [
        {
            "name": "Perfect Student (me on a good day)",
            "completion_rate": 0.95,
            "current_streak": 15,
            "consistency_score": 0.9,
            "avg_checkin_hour": 8,  # Morning person
            "days_since_start": 30,
            "grace_used_ratio": 0.1
        },
        {
            "name": "Struggling Student (me during finals)",
            "completion_rate": 0.3,
            "current_streak": 2,
            "consistency_score": 0.4,
            "avg_checkin_hour": 22,  # Night owl
            "days_since_start": 10,
            "grace_used_ratio": 0.8
        },
        {
            "name": "Average Student (me most days)",
            "completion_rate": 0.7,
            "current_streak": 8,
            "consistency_score": 0.6,
            "avg_checkin_hour": 14,  # Afternoon
            "days_since_start": 45,
            "grace_used_ratio": 0.3
        }
    ]
    
    print("\n📊 Testing different scenarios:")
    print("-" * 50)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['name']}")
        print(f"   Completion Rate: {case['completion_rate']:.0%}")
        print(f"   Current Streak: {case['current_streak']} days")
        print(f"   Consistency: {case['consistency_score']:.1f}")
        
        result = predictor.predict(
            completion_rate=case['completion_rate'],
            current_streak=case['current_streak'],
            consistency_score=case['consistency_score'],
            avg_checkin_hour=case['avg_checkin_hour'],
            days_since_start=case['days_since_start'],
            grace_used_ratio=case['grace_used_ratio']
        )
        
        print(f"   🎯 Prediction: {result['prediction'].upper()}")
        print(f"   📈 Success Probability: {result['probability']:.1f}%")
        print(f"   🤖 Model Used: {result['model_used'].upper()}")
        print(f"   ✅ Will Succeed: {'YES' if result['will_succeed'] else 'NO'}")

def test_accuracy_with_my_data():
    """Test accuracy with my own generated data."""
    print("\n" + "=" * 50)
    print("🔬 ACCURACY TEST WITH MY DATA")
    print("=" * 50)
    
    # Generate test data
    trainer = HabitMLTrainer()
    print("📊 Generating 1000 test samples...")
    X_test, y_test = trainer.generate_synthetic_data(n_samples=1000)
    
    # Load predictor
    predictor = HabitPredictor()
    
    if predictor.model is None:
        print("❌ Model not found!")
        return
    
    # Test accuracy
    correct = 0
    total = len(X_test)
    
    print(f"🧪 Testing on {total} samples...")
    
    for i in range(total):
        features = X_test.iloc[i]
        actual = y_test.iloc[i]
        
        result = predictor.predict(
            completion_rate=features['completion_rate'],
            current_streak=features['current_streak'],
            consistency_score=features['consistency_score'],
            avg_checkin_hour=features['avg_checkin_hour'],
            days_since_start=features['days_since_start'],
            grace_used_ratio=features['grace_used_ratio']
        )
        
        predicted = 1 if result['will_succeed'] else 0
        if predicted == actual:
            correct += 1
    
    accuracy = (correct / total) * 100
    
    print(f"\n📈 MY TEST RESULTS:")
    print(f"   Total predictions: {total}")
    print(f"   Correct: {correct}")
    print(f"   Incorrect: {total - correct}")
    print(f"   Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 90:
        print(f"   🎉 EXCELLENT! Accuracy is {accuracy:.1f}%")
    elif accuracy >= 85:
        print(f"   ✅ GOOD! Accuracy is {accuracy:.1f}%")
    else:
        print(f"   ⚠️ Accuracy is {accuracy:.1f}% - needs improvement")

if __name__ == "__main__":
    test_my_model()
    test_accuracy_with_my_data()
    
    print("\n" + "=" * 50)
    print("✅ MY PERSONAL TEST COMPLETE!")
    print("=" * 50)

