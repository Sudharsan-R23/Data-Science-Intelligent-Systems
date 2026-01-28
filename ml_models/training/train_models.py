"""
ML Model Training Module
Trains multiple ML models: Logistic Regression, Random Forest, SVM, XGBoost
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
import joblib
import logging
from pathlib import Path
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Train and compare multiple ML models."""
    
    def __init__(self, models_dir="ml_models/models"):
        """
        Initialize Model Trainer.
        
        Args:
            models_dir (str): Directory to save trained models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'SVM': SVC(probability=True, random_state=42),
            'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss')
        }
        
        self.trained_models = {}
        self.model_scores = {}
        
    def prepare_data(self, df, target_column, test_size=0.2, random_state=42):
        """
        Prepare data for training.
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_column (str): Target column name
            test_size (float): Test set size
            random_state (int): Random seed
        
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Data split: Train={len(X_train)}, Test={len(X_test)}")
        return X_train, X_test, y_train, y_test
    
    def train_model(self, model_name, X_train, y_train):
        """
        Train a single model.
        
        Args:
            model_name (str): Name of the model
            X_train (pd.DataFrame): Training features
            y_train (pd.Series): Training target
        
        Returns:
            Trained model
        """
        model = self.models[model_name]
        logger.info(f"Training {model_name}...")
        model.fit(X_train, y_train)
        self.trained_models[model_name] = model
        logger.info(f"{model_name} training completed")
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        Evaluate a trained model.
        
        Args:
            model: Trained model
            X_test (pd.DataFrame): Test features
            y_test (pd.Series): Test target
            model_name (str): Name of the model
        
        Returns:
            dict: Evaluation metrics
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
        
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        self.model_scores[model_name] = metrics
        
        logger.info(f"{model_name} - Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, "
                   f"Recall: {recall:.4f}, F1: {f1:.4f}")
        
        return metrics
    
    def cross_validate(self, model, X, y, cv=5):
        """
        Perform cross-validation.
        
        Args:
            model: Model to validate
            X (pd.DataFrame): Features
            y (pd.Series): Target
            cv (int): Number of folds
        
        Returns:
            dict: Cross-validation scores
        """
        cv_scores = cross_val_score(model, X, y, cv=StratifiedKFold(n_splits=cv, shuffle=True, random_state=42), 
                                    scoring='accuracy')
        return {
            'mean': cv_scores.mean(),
            'std': cv_scores.std(),
            'scores': cv_scores.tolist()
        }
    
    def train_all_models(self, X_train, X_test, y_train, y_test):
        """
        Train all models and evaluate them.
        
        Args:
            X_train (pd.DataFrame): Training features
            X_test (pd.DataFrame): Test features
            y_train (pd.Series): Training target
            y_test (pd.Series): Test target
        
        Returns:
            dict: All model scores
        """
        for model_name in self.models.keys():
            model = self.train_model(model_name, X_train, y_train)
            self.evaluate_model(model, X_test, y_test, model_name)
        
        return self.model_scores
    
    def select_best_model(self, metric='f1_score'):
        """
        Select the best model based on a metric.
        
        Args:
            metric (str): Metric to use for selection ('accuracy', 'precision', 'recall', 'f1_score')
        
        Returns:
            tuple: (best_model_name, best_model, best_score)
        """
        best_model_name = None
        best_score = -1
        
        for model_name, scores in self.model_scores.items():
            if scores[metric] > best_score:
                best_score = scores[metric]
                best_model_name = model_name
        
        best_model = self.trained_models[best_model_name]
        
        logger.info(f"Best model: {best_model_name} with {metric}={best_score:.4f}")
        
        return best_model_name, best_model, best_score
    
    def save_model(self, model, model_name, filename=None):
        """
        Save a trained model.
        
        Args:
            model: Trained model
            model_name (str): Name of the model
            filename (str): Filename (optional)
        
        Returns:
            str: Path to saved model
        """
        if filename is None:
            filename = f"{model_name.replace(' ', '_').lower()}_model.pkl"
        
        filepath = self.models_dir / filename
        joblib.dump(model, filepath)
        logger.info(f"Saved {model_name} to {filepath}")
        return str(filepath)
    
    def save_all_models(self):
        """Save all trained models."""
        saved_paths = {}
        for model_name, model in self.trained_models.items():
            filepath = self.save_model(model, model_name)
            saved_paths[model_name] = filepath
        return saved_paths
    
    def save_evaluation_results(self, filename="model_evaluation_results.json"):
        """
        Save evaluation results to JSON.
        
        Args:
            filename (str): Output filename
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'models': {}
        }
        
        for model_name, scores in self.model_scores.items():
            results['models'][model_name] = {
                'accuracy': float(scores['accuracy']),
                'precision': float(scores['precision']),
                'recall': float(scores['recall']),
                'f1_score': float(scores['f1_score'])
            }
        
        filepath = self.models_dir / filename
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved evaluation results to {filepath}")
        return str(filepath)


def main():
    """Example usage."""
    # Example:
    # df = pd.read_csv('data/processed/dataset_processed.csv')
    # trainer = ModelTrainer()
    # X_train, X_test, y_train, y_test = trainer.prepare_data(df, target_column='diagnosis')
    # trainer.train_all_models(X_train, X_test, y_train, y_test)
    # best_name, best_model, best_score = trainer.select_best_model()
    # trainer.save_model(best_model, best_name, 'best_model.pkl')
    # trainer.save_all_models()
    # trainer.save_evaluation_results()
    pass


if __name__ == "__main__":
    main()
