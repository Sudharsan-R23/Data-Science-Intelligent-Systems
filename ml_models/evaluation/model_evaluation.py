"""
Model Evaluation Module with Explainable AI Features
Includes feature importance, SHAP values, and model interpretability.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
import joblib
import logging
from pathlib import Path
import json

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    logging.warning("SHAP not available. Install with: pip install shap")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluate models with explainable AI features."""
    
    def __init__(self, model, model_name, feature_names=None):
        """
        Initialize Model Evaluator.
        
        Args:
            model: Trained model
            model_name (str): Name of the model
            feature_names (list): List of feature names
        """
        self.model = model
        self.model_name = model_name
        self.feature_names = feature_names
        self.shap_explainer = None
        
    def get_feature_importance(self):
        """
        Get feature importance from model.
        
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            importances = np.abs(self.model.coef_[0])
        else:
            logger.warning(f"{self.model_name} does not support feature importance")
            return None
        
        if self.feature_names is None:
            self.feature_names = [f'Feature_{i}' for i in range(len(importances))]
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        logger.info("Feature importance calculated")
        return importance_df
    
    def plot_feature_importance(self, top_n=15, save_path=None):
        """
        Plot feature importance.
        
        Args:
            top_n (int): Number of top features to display
            save_path (str): Path to save the plot
        """
        importance_df = self.get_feature_importance()
        if importance_df is None:
            return
        
        plt.figure(figsize=(10, 8))
        top_features = importance_df.head(top_n)
        sns.barplot(data=top_features, x='importance', y='feature', palette='viridis')
        plt.title(f'{self.model_name} - Top {top_n} Feature Importance')
        plt.xlabel('Importance')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved feature importance plot to {save_path}")
        else:
            plt.show()
    
    def calculate_shap_values(self, X_sample, max_samples=100):
        """
        Calculate SHAP values for model interpretability.
        
        Args:
            X_sample (pd.DataFrame): Sample data for SHAP calculation
            max_samples (int): Maximum samples to use
        
        Returns:
            np.array: SHAP values
        """
        if not SHAP_AVAILABLE:
            logger.warning("SHAP not available. Skipping SHAP value calculation.")
            return None
        
        # Limit samples for performance
        if len(X_sample) > max_samples:
            X_sample = X_sample.sample(n=max_samples, random_state=42)
        
        try:
            if hasattr(self.model, 'predict_proba'):
                # Tree-based models
                if isinstance(self.model, (type(self.model).__module__.split('.')[0] if hasattr(self.model, '__module__') else None)):
                    self.shap_explainer = shap.TreeExplainer(self.model)
                else:
                    self.shap_explainer = shap.KernelExplainer(self.model.predict_proba, X_sample)
            else:
                self.shap_explainer = shap.KernelExplainer(self.model.predict, X_sample)
            
            shap_values = self.shap_explainer.shap_values(X_sample)
            
            # Handle multi-class output
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # Use positive class
            
            logger.info("SHAP values calculated")
            return shap_values
        except Exception as e:
            logger.error(f"Error calculating SHAP values: {str(e)}")
            return None
    
    def plot_shap_summary(self, X_sample, max_samples=100, save_path=None):
        """
        Plot SHAP summary.
        
        Args:
            X_sample (pd.DataFrame): Sample data
            max_samples (int): Maximum samples
            save_path (str): Path to save plot
        """
        if not SHAP_AVAILABLE:
            return
        
        shap_values = self.calculate_shap_values(X_sample, max_samples)
        if shap_values is None:
            return
        
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_sample, show=False)
        plt.title(f'{self.model_name} - SHAP Summary Plot')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved SHAP plot to {save_path}")
        else:
            plt.show()
    
    def plot_confusion_matrix(self, y_true, y_pred, save_path=None):
        """
        Plot confusion matrix.
        
        Args:
            y_true (np.array): True labels
            y_pred (np.array): Predicted labels
            save_path (str): Path to save plot
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Negative', 'Positive'],
                   yticklabels=['Negative', 'Positive'])
        plt.title(f'{self.model_name} - Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved confusion matrix to {save_path}")
        else:
            plt.show()
    
    def plot_roc_curve(self, y_true, y_pred_proba, save_path=None):
        """
        Plot ROC curve.
        
        Args:
            y_true (np.array): True labels
            y_pred_proba (np.array): Predicted probabilities
            save_path (str): Path to save plot
        """
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'{self.model_name} - ROC Curve')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved ROC curve to {save_path}")
        else:
            plt.show()
    
    def generate_explanation_report(self, X_sample, y_true=None, y_pred=None, 
                                   output_dir="ml_models/evaluation/reports"):
        """
        Generate comprehensive explanation report.
        
        Args:
            X_sample (pd.DataFrame): Sample data
            y_true (np.array): True labels (optional)
            y_pred (np.array): Predicted labels (optional)
            output_dir (str): Output directory
        
        Returns:
            dict: Report data
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        report = {
            'model_name': self.model_name,
            'feature_importance': None,
            'shap_available': SHAP_AVAILABLE
        }
        
        # Feature importance
        importance_df = self.get_feature_importance()
        if importance_df is not None:
            report['feature_importance'] = importance_df.to_dict('records')
            self.plot_feature_importance(
                save_path=str(output_path / f"{self.model_name}_feature_importance.png")
            )
        
        # SHAP values
        if SHAP_AVAILABLE:
            shap_values = self.calculate_shap_values(X_sample)
            if shap_values is not None:
                self.plot_shap_summary(
                    X_sample,
                    save_path=str(output_path / f"{self.model_name}_shap_summary.png")
                )
        
        # Confusion matrix
        if y_true is not None and y_pred is not None:
            self.plot_confusion_matrix(
                y_true, y_pred,
                save_path=str(output_path / f"{self.model_name}_confusion_matrix.png")
            )
        
        # Save report JSON
        report_path = output_path / f"{self.model_name}_explanation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Generated explanation report for {self.model_name}")
        return report


def main():
    """Example usage."""
    pass


if __name__ == "__main__":
    main()
