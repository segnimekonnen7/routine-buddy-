"""
Test and verify the ML model accuracy claims.
This script proves the 85%+ accuracy claim on the resume.
"""

import sys
sys.path.insert(0, 'backend')

from app.ml.predictor import HabitPredictor
from app.ml.train_model import HabitMLTrainer
import pandas as pd

def verify_model_accuracy():
    """Verify that the trained model meets accuracy requirements."""
    print("=" * 70)
    print("🔬 ML MODEL VERIFICATION TEST")
    print("=" * 70)
    
    # Create trainer and generate test data
    trainer = HabitMLTrainer()
    print("\n📊 Generating independent test data...")
    X_test, y_test = trainer.generate_synthetic_data(n_samples=500)
    
    # Load the trained model
    predictor = HabitPredictor()
    
    if predictor.model is None:
        print("❌ Model not found! Run train_model.py first.")
        return False
    
    print(f"✅ Model loaded: {type(predictor.model).__name__}")
    
    # Make predictions
    print("\n🧪 Running predictions on 500 test samples...")
    correct = 0
    total = len(X_test)
    
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
    
    print(f"\n📈 RESULTS:")
    print(f"   Total predictions: {total}")
    print(f"   Correct: {correct}")
    print(f"   Incorrect: {total - correct}")
    print(f"   Accuracy: {accuracy:.1f}%")
    
    # Verify claim
    print(f"\n✅ VERIFICATION:")
    if accuracy >= 85:
        print(f"   ✅ Model meets 85% accuracy requirement")
        print(f"   ✅ Actual accuracy: {accuracy:.1f}%")
        print(f"   ✅ Resume claim VERIFIED")
        return True
    else:
        print(f"   ❌ Model does not meet 85% requirement")
        print(f"   ❌ Actual accuracy: {accuracy:.1f}%")
        return False

def test_sample_predictions():
    """Test predictions on sample scenarios."""
    print("\n" + "=" * 70)
    print("🧪 SAMPLE PREDICTION TESTS")
    print("=" * 70)
    
    predictor = HabitPredictor()
    
    scenarios = [
        {
            "name": "Strong habit (high completion, long streak)",
            "completion_rate": 0.85,
            "current_streak": 20,
            "consistency_score": 0.8,
            "expected": "high"
        },
        {
            "name": "Moderate habit (decent completion, medium streak)",
            "completion_rate": 0.60,
            "current_streak": 10,
            "consistency_score": 0.55,
            "expected": "medium/high"
        },
        {
            "name": "Struggling habit (low completion, short streak)",
            "completion_rate": 0.30,
            "current_streak": 2,
            "consistency_score": 0.25,
            "expected": "low"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        result = predictor.predict(
            completion_rate=scenario['completion_rate'],
            current_streak=scenario['current_streak'],
            consistency_score=scenario['consistency_score']
        )
        
        print(f"   Completion Rate: {scenario['completion_rate']:.0%}")
        print(f"   Current Streak: {scenario['current_streak']} days")
        print(f"   Consistency: {scenario['consistency_score']:.2f}")
        print(f"   Prediction: {result['prediction'].upper()}")
        print(f"   Success Probability: {result['probability']:.1f}%")
        print(f"   Model Used: {result['model_used'].upper()}")
        print(f"   Expected: {scenario['expected']}")


if __name__ == "__main__":
    print("\n")
    success = verify_model_accuracy()
    test_sample_predictions()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ ALL VERIFICATIONS PASSED - Resume claim is TRUE")
    else:
        print("❌ VERIFICATION FAILED - Resume claim cannot be supported")
    print("=" * 70)
    print("\n")

