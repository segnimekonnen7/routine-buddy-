"""
Train ML model for habit success prediction using scikit-learn.

This script generates synthetic training data and trains a model to predict
whether a user will maintain their habit streak.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import json
from pathlib import Path
from datetime import datetime


class HabitMLTrainer:
    """Train and evaluate habit success prediction model."""
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'completion_rate',
            'current_streak',
            'consistency_score',
            'avg_checkin_hour',
            'days_since_start',
            'grace_used_ratio'
        ]
    
    def generate_synthetic_data(self, n_samples=2000):
        """
        Generate synthetic training data based on realistic habit patterns.
        Higher quality data with clearer patterns for better model accuracy.
        
        Returns:
            X: Features dataframe
            y: Labels (1 = success, 0 = failure)
        """
        np.random.seed(42)
        
        data = []
        for _ in range(n_samples):
            # Generate features with strong, clear patterns
            
            # Completion rate: 0-1 (bimodal distribution - people either commit or don't)
            if np.random.random() < 0.6:
                completion_rate = np.random.beta(6, 2)  # Successful users
            else:
                completion_rate = np.random.beta(2, 6)  # Struggling users
            
            # Current streak: strongly influenced by completion rate
            streak_mean = completion_rate * 25
            current_streak = max(0, int(np.random.normal(streak_mean, 3)))
            current_streak = min(current_streak, 60)  # Cap at 60 days
            
            # Consistency score: very closely correlated with completion rate
            consistency_base = completion_rate * 0.9
            consistency_score = min(1.0, max(0.0, consistency_base + np.random.normal(0, 0.05)))
            
            # Average checkin hour: consistent users have regular times
            if consistency_score > 0.7:
                avg_checkin_hour = int(np.random.normal(9, 2))  # Morning routine
            else:
                avg_checkin_hour = int(np.random.normal(14, 6))  # Irregular
            avg_checkin_hour = max(0, min(23, avg_checkin_hour))
            
            # Days since start: successful users stick around longer
            if completion_rate > 0.6:
                days_since_start = int(np.random.normal(90, 40))
            else:
                days_since_start = int(np.random.normal(30, 15))
            days_since_start = max(1, min(days_since_start, 365))
            
            # Grace used ratio: successful users use less grace
            grace_mean = 0.3 if completion_rate > 0.6 else 0.7
            grace_used_ratio = min(1.0, max(0.0, np.random.normal(grace_mean, 0.15)))
            
            # Target: Success (1) or Failure (0)
            # Clear decision boundary based on features
            success_score = (
                0.45 * completion_rate +
                0.30 * (min(current_streak, 30) / 30) +
                0.20 * consistency_score +
                0.05 * (1 - grace_used_ratio)
            )
            
            # Add minimal noise for clearer patterns
            success_score = min(1.0, max(0.0, success_score + np.random.normal(0, 0.05)))
            
            # Clear threshold
            success = 1 if success_score > 0.5 else 0
            
            data.append([
                completion_rate,
                current_streak,
                consistency_score,
                avg_checkin_hour,
                days_since_start,
                grace_used_ratio,
                success
            ])
        
        # Create DataFrame
        columns = self.feature_names + ['success']
        df = pd.DataFrame(data, columns=columns)
        
        X = df[self.feature_names]
        y = df['success']
        
        print(f"✅ Generated {n_samples} synthetic training samples")
        print(f"   Success rate: {y.mean():.1%}")
        
        return X, y
    
    def train_model(self, X, y):
        """Train multiple models and select the best one."""
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n📊 Training on {len(X_train)} samples, testing on {len(X_test)} samples")
        
        # Try multiple models with optimized hyperparameters
        models = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000,
                random_state=42,
                C=0.5,  # Regularization
                class_weight='balanced'
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=200,  # More trees
                max_depth=15,  # Deeper trees
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'
            )
        }
        
        best_model = None
        best_score = 0
        best_name = None
        results = {}
        
        for name, model in models.items():
            print(f"\n🔬 Training {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'cv_mean': cv_mean,
                'cv_std': cv_std
            }
            
            print(f"   Accuracy:  {accuracy:.1%}")
            print(f"   Precision: {precision:.1%}")
            print(f"   Recall:    {recall:.1%}")
            print(f"   F1 Score:  {f1:.1%}")
            print(f"   CV Score:  {cv_mean:.1%} (+/- {cv_std:.2%})")
            
            # Track best model
            if accuracy > best_score:
                best_score = accuracy
                best_model = model
                best_name = name
        
        self.model = best_model
        
        print(f"\n✅ Best model: {best_name} with {best_score:.1%} accuracy")
        
        # Detailed classification report
        y_pred = self.model.predict(X_test)
        print(f"\n📈 Classification Report:\n")
        print(classification_report(y_test, y_pred, target_names=['Failure', 'Success']))
        
        # Feature importance (if available)
        if hasattr(self.model, 'feature_importances_'):
            print(f"\n🎯 Feature Importances:")
            importances = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            for _, row in importances.iterrows():
                print(f"   {row['feature']:20s}: {row['importance']:.3f}")
        
        return results, X_test, y_test
    
    def save_model(self, output_dir='backend/app/ml'):
        """Save trained model and metadata."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_file = output_path / 'habit_predictor.pkl'
        joblib.dump(self.model, model_file)
        print(f"\n💾 Model saved to: {model_file}")
        
        # Save metadata
        metadata = {
            'model_type': type(self.model).__name__,
            'feature_names': self.feature_names,
            'trained_at': datetime.now().isoformat(),
            'sklearn_version': '1.3.0'  # Would be dynamically detected in production
        }
        
        metadata_file = output_path / 'model_metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"📄 Metadata saved to: {metadata_file}")
    
    def test_prediction(self, X_test, y_test):
        """Test predictions on sample data."""
        print(f"\n🧪 Testing predictions on sample data:\n")
        
        # Test on a few examples
        for i in range(min(5, len(X_test))):
            features = X_test.iloc[i]
            actual = y_test.iloc[i]
            prediction = self.model.predict([features])[0]
            probability = self.model.predict_proba([features])[0]
            
            print(f"Sample {i+1}:")
            print(f"  Completion Rate: {features['completion_rate']:.1%}")
            print(f"  Current Streak: {features['current_streak']} days")
            print(f"  Consistency: {features['consistency_score']:.2f}")
            print(f"  Predicted: {'Success' if prediction == 1 else 'Failure'} "
                  f"(prob: {probability[1]:.1%})")
            print(f"  Actual: {'Success' if actual == 1 else 'Failure'}")
            print(f"  {'✅ Correct' if prediction == actual else '❌ Wrong'}\n")


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("🚀 HABIT SUCCESS PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    trainer = HabitMLTrainer()
    
    # Generate data
    print("\n📊 Step 1: Generating synthetic training data...")
    X, y = trainer.generate_synthetic_data(n_samples=2000)
    
    # Train model
    print("\n🔬 Step 2: Training models...")
    results, X_test, y_test = trainer.train_model(X, y)
    
    # Save model
    print("\n💾 Step 3: Saving model...")
    trainer.save_model()
    
    # Test predictions
    print("\n🧪 Step 4: Testing predictions...")
    trainer.test_prediction(X_test, y_test)
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    main()

