"""
Machine Learning Model Training Pipeline
Trains and evaluates multiple ML models for healthcare diagnosis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import pickle
from datetime import datetime

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)

import warnings
warnings.filterwarnings('ignore')

# Create output directories
Path("models").mkdir(exist_ok=True)
Path("results").mkdir(exist_ok=True)
Path("results/plots").mkdir(exist_ok=True)

class HealthcareDiagnosisModel:
    """
    End-to-end ML pipeline for healthcare diagnosis
    """
    
    def __init__(self, dataset_path, target_column, dataset_name):
        self.dataset_path = dataset_path
        self.target_column = target_column
        self.dataset_name = dataset_name
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        
    def load_data(self):
        """Load dataset"""
        print(f"\n{'='*70}")
        print(f"Loading {self.dataset_name} Dataset")
        print(f"{'='*70}")
        
        self.df = pd.read_csv(self.dataset_path)
        print(f"Dataset shape: {self.df.shape}")
        print(f"\nColumns: {list(self.df.columns)}")
        print(f"\nFirst 5 rows:")
        print(self.df.head())
        
        # Basic statistics
        print(f"\nDataset Statistics:")
        print(self.df.describe())
        
        # Check for missing values
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(f"\nMissing Values:\n{missing[missing > 0]}")
        else:
            print("\n✓ No missing values found")
            
        # Target distribution
        print(f"\nTarget Distribution ({self.target_column}):")
        print(self.df[self.target_column].value_counts())
        print(f"Positive cases: {self.df[self.target_column].sum()} ({self.df[self.target_column].mean()*100:.1f}%)")
        
    def preprocess_data(self, test_size=0.2, random_state=42):
        """Preprocess and split data"""
        print(f"\n{'='*70}")
        print("Data Preprocessing")
        print(f"{'='*70}")
        
        # Separate features and target
        X = self.df.drop(columns=[self.target_column])
        y = self.df[self.target_column]
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"Training set size: {len(self.X_train)}")
        print(f"Test set size: {len(self.X_test)}")
        
        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        print("✓ Features scaled using StandardScaler")
        
    def train_models(self):
        """Train multiple ML models"""
        print(f"\n{'='*70}")
        print("Model Training")
        print(f"{'='*70}")
        
        # Define models
        self.models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(probability=True, random_state=42),
            'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss')
        }
        
        # Train each model
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            model.fit(self.X_train, self.y_train)
            print(f"✓ {name} trained successfully")
            
    def evaluate_models(self):
        """Evaluate all models"""
        print(f"\n{'='*70}")
        print("Model Evaluation")
        print(f"{'='*70}")
        
        for name, model in self.models.items():
            print(f"\n--- {name} ---")
            
            # Predictions
            y_pred = model.predict(self.X_test)
            y_pred_proba = model.predict_proba(self.X_test)[:, 1]
            
            # Calculate metrics
            metrics = {
                'Accuracy': accuracy_score(self.y_test, y_pred),
                'Precision': precision_score(self.y_test, y_pred, zero_division=0),
                'Recall': recall_score(self.y_test, y_pred, zero_division=0),
                'F1-Score': f1_score(self.y_test, y_pred, zero_division=0),
                'ROC-AUC': roc_auc_score(self.y_test, y_pred_proba)
            }
            
            self.results[name] = metrics
            
            # Print metrics
            for metric, value in metrics.items():
                print(f"{metric}: {value:.4f}")
                
            # Confusion Matrix
            cm = confusion_matrix(self.y_test, y_pred)
            print(f"\nConfusion Matrix:\n{cm}")
            
        # Create comparison DataFrame
        results_df = pd.DataFrame(self.results).T
        results_df = results_df.round(4)
        
        print(f"\n{'='*70}")
        print("MODEL COMPARISON")
        print(f"{'='*70}")
        print(results_df)
        
        # Determine best model
        self.best_model_name = results_df['Accuracy'].idxmax()
        self.best_model = self.models[self.best_model_name]
        
        print(f"\n🏆 Best Model: {self.best_model_name}")
        print(f"   Accuracy: {results_df.loc[self.best_model_name, 'Accuracy']:.4f}")
        
        # Save results
        results_path = f"results/{self.dataset_name}_results.json"
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Results saved to {results_path}")
        
        # Save results DataFrame as CSV
        csv_path = f"results/{self.dataset_name}_comparison.csv"
        results_df.to_csv(csv_path)
        print(f"✓ Comparison saved to {csv_path}")
        
        return results_df
        
    def plot_model_comparison(self, results_df):
        """Create visualization of model performance"""
        print(f"\nGenerating performance visualizations...")
        
        # Set style
        sns.set_style("whitegrid")
        
        # Create comparison plot
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot 1: All metrics comparison
        results_df.plot(kind='bar', ax=axes[0])
        axes[0].set_title(f'{self.dataset_name} - Model Performance Comparison', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Models', fontsize=12)
        axes[0].set_ylabel('Score', fontsize=12)
        axes[0].set_ylim([0, 1])
        axes[0].legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Accuracy comparison
        accuracy_data = results_df['Accuracy'].sort_values(ascending=False)
        colors = ['#2ecc71' if x == accuracy_data.max() else '#3498db' for x in accuracy_data]
        accuracy_data.plot(kind='barh', ax=axes[1], color=colors)
        axes[1].set_title(f'{self.dataset_name} - Accuracy Comparison', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Accuracy', fontsize=12)
        axes[1].set_xlim([0, 1])
        
        plt.tight_layout()
        plot_path = f"results/plots/{self.dataset_name}_comparison.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Comparison plot saved to {plot_path}")
        plt.close()
        
    def plot_feature_importance(self):
        """Plot feature importance for tree-based models"""
        print(f"\nGenerating feature importance plot...")
        
        # Use Random Forest or XGBoost for feature importance
        if self.best_model_name in ['Random Forest', 'XGBoost']:
            feature_names = self.df.drop(columns=[self.target_column]).columns
            importances = self.best_model.feature_importances_
            
            # Create DataFrame
            feat_imp_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importances
            }).sort_values('Importance', ascending=False)
            
            # Plot
            plt.figure(figsize=(10, 6))
            sns.barplot(data=feat_imp_df, x='Importance', y='Feature', palette='viridis')
            plt.title(f'{self.dataset_name} - Feature Importance ({self.best_model_name})', 
                     fontsize=14, fontweight='bold')
            plt.xlabel('Importance', fontsize=12)
            plt.ylabel('Features', fontsize=12)
            plt.tight_layout()
            
            plot_path = f"results/plots/{self.dataset_name}_feature_importance.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            print(f"✓ Feature importance plot saved to {plot_path}")
            plt.close()
            
            return feat_imp_df
        else:
            print(f"Feature importance not available for {self.best_model_name}")
            return None
            
    def save_model(self):
        """Save the best model and scaler"""
        print(f"\n{'='*70}")
        print("Saving Model")
        print(f"{'='*70}")
        
        # Save model
        model_path = f"models/{self.dataset_name}_model.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        print(f"✓ Model saved to {model_path}")
        
        # Save scaler
        scaler_path = f"models/{self.dataset_name}_scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"✓ Scaler saved to {scaler_path}")
        
        # Save metadata
        metadata = {
            'model_name': self.best_model_name,
            'dataset': self.dataset_name,
            'features': list(self.df.drop(columns=[self.target_column]).columns),
            'target': self.target_column,
            'metrics': self.results[self.best_model_name],
            'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'train_size': len(self.X_train),
            'test_size': len(self.X_test)
        }
        
        metadata_path = f"models/{self.dataset_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Metadata saved to {metadata_path}")
        
    def run_pipeline(self):
        """Execute full ML pipeline"""
        self.load_data()
        self.preprocess_data()
        self.train_models()
        results_df = self.evaluate_models()
        self.plot_model_comparison(results_df)
        self.plot_feature_importance()
        self.save_model()
        
        print(f"\n{'='*70}")
        print(f"✅ {self.dataset_name} Pipeline Complete!")
        print(f"{'='*70}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("HEALTHCARE DIAGNOSIS - ML TRAINING PIPELINE")
    print("="*70)
    
    # Train Diabetes Model
    print("\n\n🩺 DIABETES PREDICTION MODEL")
    diabetes_pipeline = HealthcareDiagnosisModel(
        dataset_path="data/diabetes_data.csv",
        target_column="Outcome",
        dataset_name="diabetes"
    )
    diabetes_pipeline.run_pipeline()
    
    # Train Heart Disease Model
    print("\n\n❤️ HEART DISEASE PREDICTION MODEL")
    heart_pipeline = HealthcareDiagnosisModel(
        dataset_path="data/heart_disease_data.csv",
        target_column="HeartDisease",
        dataset_name="heart_disease"
    )
    heart_pipeline.run_pipeline()
    
    print("\n\n" + "="*70)
    print("🎉 ALL MODELS TRAINED SUCCESSFULLY!")
    print("="*70)
    print("\nGenerated Files:")
    print("  📁 models/")
    print("     - diabetes_model.pkl")
    print("     - heart_disease_model.pkl")
    print("     - *_scaler.pkl")
    print("     - *_metadata.json")
    print("  📁 results/")
    print("     - *_results.json")
    print("     - *_comparison.csv")
    print("     - plots/*.png")
