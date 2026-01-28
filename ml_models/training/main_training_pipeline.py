"""
Main Training Pipeline
Complete end-to-end pipeline: Data extraction -> Preprocessing -> Training -> Evaluation
"""

import pandas as pd
import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from data_extraction.extract_pdf import PDFExtractor
from preprocessing.data_preprocessing import DataPreprocessor
from training.train_models import ModelTrainer
from evaluation.model_evaluation import ModelEvaluator
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrainingPipeline:
    """Complete training pipeline."""
    
    def __init__(self, config=None):
        """
        Initialize training pipeline.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config or self.default_config()
        self.preprocessor = DataPreprocessor()
        self.trainer = ModelTrainer()
        
    def default_config(self):
        """Default configuration."""
        return {
            'pdf_path': None,
            'csv_path': None,
            'target_column': 'diagnosis',
            'test_size': 0.2,
            'preprocessing': {
                'handle_missing': True,
                'encode_cat': True,
                'normalize': True,
                'feature_selection': False
            },
            'models': ['Logistic Regression', 'Random Forest', 'SVM', 'XGBoost']
        }
    
    def extract_data(self, pdf_path=None):
        """
        Extract data from PDF.
        
        Args:
            pdf_path (str): Path to PDF file
        
        Returns:
            str: Path to extracted CSV file
        """
        pdf_path = pdf_path or self.config.get('pdf_path')
        if not pdf_path:
            logger.warning("No PDF path provided. Skipping extraction.")
            return None
        
        logger.info(f"Extracting data from {pdf_path}")
        extractor = PDFExtractor(pdf_path)
        saved_files = extractor.extract_and_save(method='pdfplumber')
        
        if saved_files:
            logger.info(f"Extracted {len(saved_files)} tables")
            return saved_files[0]  # Return first extracted file
        return None
    
    def load_data(self, csv_path):
        """
        Load data from CSV.
        
        Args:
            csv_path (str): Path to CSV file
        
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        logger.info(f"Loading data from {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df
    
    def preprocess_data(self, df, target_column):
        """
        Preprocess data.
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_column (str): Target column name
        
        Returns:
            pd.DataFrame: Preprocessed dataframe
        """
        logger.info("Starting data preprocessing...")
        
        prep_config = self.config.get('preprocessing', {})
        df_processed = self.preprocessor.preprocess_pipeline(
            df,
            target_column=target_column,
            handle_missing=prep_config.get('handle_missing', True),
            encode_cat=prep_config.get('encode_cat', True),
            normalize=prep_config.get('normalize', True),
            feature_selection=prep_config.get('feature_selection', False),
            y=df[target_column] if prep_config.get('feature_selection') else None,
            **prep_config
        )
        
        # Save preprocessor
        preprocessor_path = Path("ml_models/models/preprocessor.pkl")
        self.preprocessor.save_preprocessor(preprocessor_path)
        
        # Save processed data
        processed_path = Path("data/processed/dataset_processed.csv")
        df_processed.to_csv(processed_path, index=False)
        logger.info(f"Saved processed data to {processed_path}")
        
        return df_processed
    
    def train_models(self, df, target_column):
        """
        Train all models.
        
        Args:
            df (pd.DataFrame): Preprocessed dataframe
            target_column (str): Target column name
        
        Returns:
            dict: Model scores
        """
        logger.info("Starting model training...")
        
        X_train, X_test, y_train, y_test = self.trainer.prepare_data(
            df, target_column, test_size=self.config.get('test_size', 0.2)
        )
        
        # Train all models
        scores = self.trainer.train_all_models(X_train, X_test, y_train, y_test)
        
        # Select best model
        best_name, best_model, best_score = self.trainer.select_best_model()
        
        # Save best model
        self.trainer.save_model(best_model, best_name, 'best_model.pkl')
        
        # Save all models
        self.trainer.save_all_models()
        
        # Save evaluation results
        self.trainer.save_evaluation_results()
        
        # Generate evaluation reports
        self.generate_evaluation_reports(best_model, best_name, X_test, y_test)
        
        return scores
    
    def generate_evaluation_reports(self, model, model_name, X_test, y_test):
        """
        Generate evaluation reports with explainable AI.
        
        Args:
            model: Trained model
            model_name (str): Model name
            X_test (pd.DataFrame): Test features
            y_test (pd.Series): Test target
        """
        logger.info("Generating evaluation reports...")
        
        evaluator = ModelEvaluator(model, model_name, feature_names=X_test.columns.tolist())
        
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        evaluator.generate_explanation_report(
            X_test.sample(min(100, len(X_test)), random_state=42),
            y_true=y_test.values,
            y_pred=y_pred
        )
        
        logger.info("Evaluation reports generated")
    
    def run(self, csv_path=None, pdf_path=None, target_column=None):
        """
        Run complete pipeline.
        
        Args:
            csv_path (str): Path to CSV file (optional if PDF provided)
            pdf_path (str): Path to PDF file (optional if CSV provided)
            target_column (str): Target column name
        """
        logger.info("=" * 50)
        logger.info("Starting Complete Training Pipeline")
        logger.info("=" * 50)
        
        # Step 1: Extract data from PDF if provided
        if pdf_path:
            csv_path = self.extract_data(pdf_path)
        
        # Step 2: Load data
        if not csv_path:
            raise ValueError("Either csv_path or pdf_path must be provided")
        
        df = self.load_data(csv_path)
        
        # Step 3: Preprocess data
        target_col = target_column or self.config.get('target_column')
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataset")
        
        df_processed = self.preprocess_data(df, target_col)
        
        # Step 4: Train models
        scores = self.train_models(df_processed, target_col)
        
        logger.info("=" * 50)
        logger.info("Training Pipeline Completed Successfully!")
        logger.info("=" * 50)
        
        return scores


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ML Training Pipeline')
    parser.add_argument('--csv', type=str, help='Path to CSV file')
    parser.add_argument('--pdf', type=str, help='Path to PDF file')
    parser.add_argument('--target', type=str, default='diagnosis', help='Target column name')
    
    args = parser.parse_args()
    
    pipeline = TrainingPipeline()
    pipeline.run(csv_path=args.csv, pdf_path=args.pdf, target_column=args.target)


if __name__ == "__main__":
    main()
