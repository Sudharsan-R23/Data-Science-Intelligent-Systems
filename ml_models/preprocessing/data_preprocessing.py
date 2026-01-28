"""
Data Preprocessing Module
Handles data cleaning, normalization, encoding, and feature selection.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif, chi2
import logging
import joblib
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Handle data preprocessing tasks."""
    
    def __init__(self):
        """Initialize preprocessor with default settings."""
        self.scaler = None
        self.label_encoders = {}
        self.onehot_encoders = {}
        self.imputer = None
        self.feature_selector = None
        self.selected_features = None
        self.categorical_columns = []
        self.numerical_columns = []
        
    def identify_column_types(self, df):
        """
        Identify categorical and numerical columns.
        
        Args:
            df (pd.DataFrame): Input dataframe
        
        Returns:
            tuple: (categorical_columns, numerical_columns)
        """
        categorical = []
        numerical = []
        
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype == 'category':
                categorical.append(col)
            else:
                numerical.append(col)
        
        self.categorical_columns = categorical
        self.numerical_columns = numerical
        
        logger.info(f"Identified {len(categorical)} categorical and {len(numerical)} numerical columns")
        return categorical, numerical
    
    def handle_missing_values(self, df, strategy='mean', numerical_strategy='mean', categorical_strategy='most_frequent'):
        """
        Handle missing values in the dataset.
        
        Args:
            df (pd.DataFrame): Input dataframe
            strategy (str): Overall strategy ('mean', 'median', 'most_frequent', 'knn')
            numerical_strategy (str): Strategy for numerical columns
            categorical_strategy (str): Strategy for categorical columns
        
        Returns:
            pd.DataFrame: Dataframe with missing values handled
        """
        df_processed = df.copy()
        
        # Handle numerical columns
        if self.numerical_columns:
            if strategy == 'knn':
                imputer = KNNImputer(n_neighbors=5)
                df_processed[self.numerical_columns] = imputer.fit_transform(df_processed[self.numerical_columns])
                self.imputer = imputer
            else:
                imputer = SimpleImputer(strategy=numerical_strategy)
                df_processed[self.numerical_columns] = imputer.fit_transform(df_processed[self.numerical_columns])
                self.imputer = imputer
        
        # Handle categorical columns
        if self.categorical_columns:
            imputer_cat = SimpleImputer(strategy=categorical_strategy)
            df_processed[self.categorical_columns] = imputer_cat.fit_transform(df_processed[self.categorical_columns])
        
        logger.info("Handled missing values")
        return df_processed
    
    def encode_categorical(self, df, target_column=None, encoding_method='label'):
        """
        Encode categorical variables.
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_column (str): Target column name (if exists)
            encoding_method (str): 'label' or 'onehot'
        
        Returns:
            pd.DataFrame: Dataframe with encoded categorical variables
        """
        df_encoded = df.copy()
        
        # Exclude target column from encoding
        cat_cols_to_encode = [col for col in self.categorical_columns if col != target_column]
        
        if encoding_method == 'label':
            for col in cat_cols_to_encode:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                self.label_encoders[col] = le
                logger.info(f"Label encoded column: {col}")
        
        elif encoding_method == 'onehot':
            for col in cat_cols_to_encode:
                ohe = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
                encoded = ohe.fit_transform(df_encoded[[col]])
                encoded_df = pd.DataFrame(
                    encoded,
                    columns=[f"{col}_{cat}" for cat in ohe.categories_[0][1:]]
                )
                df_encoded = pd.concat([df_encoded.drop(columns=[col]), encoded_df], axis=1)
                self.onehot_encoders[col] = ohe
                logger.info(f"One-hot encoded column: {col}")
        
        return df_encoded
    
    def normalize_features(self, df, method='standard', columns=None):
        """
        Normalize numerical features.
        
        Args:
            df (pd.DataFrame): Input dataframe
            method (str): 'standard' (z-score) or 'minmax' (0-1 scaling)
            columns (list): Columns to normalize (None for all numerical)
        
        Returns:
            pd.DataFrame: Dataframe with normalized features
        """
        if columns is None:
            columns = self.numerical_columns
        
        df_normalized = df.copy()
        
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError("Method must be 'standard' or 'minmax'")
        
        df_normalized[columns] = self.scaler.fit_transform(df_normalized[columns])
        logger.info(f"Normalized {len(columns)} columns using {method} scaling")
        
        return df_normalized
    
    def feature_selection(self, X, y, method='mutual_info', k=10):
        """
        Perform feature selection.
        
        Args:
            X (pd.DataFrame): Feature dataframe
            y (pd.Series): Target variable
            method (str): 'mutual_info', 'f_classif', or 'chi2'
            k (int): Number of features to select
        
        Returns:
            pd.DataFrame: Dataframe with selected features
        """
        if method == 'mutual_info':
            selector = SelectKBest(score_func=mutual_info_classif, k=k)
        elif method == 'f_classif':
            selector = SelectKBest(score_func=f_classif, k=k)
        elif method == 'chi2':
            selector = SelectKBest(score_func=chi2, k=k)
        else:
            raise ValueError("Method must be 'mutual_info', 'f_classif', or 'chi2'")
        
        X_selected = selector.fit_transform(X, y)
        self.feature_selector = selector
        self.selected_features = X.columns[selector.get_support()].tolist()
        
        logger.info(f"Selected {len(self.selected_features)} features using {method}")
        logger.info(f"Selected features: {self.selected_features}")
        
        return pd.DataFrame(X_selected, columns=self.selected_features, index=X.index)
    
    def preprocess_pipeline(self, df, target_column=None, 
                           handle_missing=True, encode_cat=True, normalize=True,
                           feature_selection=False, y=None, **kwargs):
        """
        Complete preprocessing pipeline.
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_column (str): Target column name
            handle_missing (bool): Whether to handle missing values
            encode_cat (bool): Whether to encode categorical variables
            normalize (bool): Whether to normalize features
            feature_selection (bool): Whether to perform feature selection
            y (pd.Series): Target variable for feature selection
            **kwargs: Additional arguments for preprocessing steps
        
        Returns:
            pd.DataFrame: Preprocessed dataframe
        """
        df_processed = df.copy()
        
        # Identify column types
        self.identify_column_types(df_processed)
        
        # Handle missing values
        if handle_missing:
            df_processed = self.handle_missing_values(
                df_processed,
                strategy=kwargs.get('missing_strategy', 'mean')
            )
        
        # Encode categorical variables
        if encode_cat:
            df_processed = self.encode_categorical(
                df_processed,
                target_column=target_column,
                encoding_method=kwargs.get('encoding_method', 'label')
            )
        
        # Normalize features
        if normalize:
            df_processed = self.normalize_features(
                df_processed,
                method=kwargs.get('normalization_method', 'standard')
            )
        
        # Feature selection
        if feature_selection and y is not None:
            X_features = df_processed.drop(columns=[target_column]) if target_column else df_processed
            X_selected = self.feature_selection(
                X_features,
                y,
                method=kwargs.get('selection_method', 'mutual_info'),
                k=kwargs.get('n_features', 10)
            )
            if target_column:
                df_processed = pd.concat([X_selected, df_processed[[target_column]]], axis=1)
            else:
                df_processed = X_selected
        
        logger.info("Preprocessing pipeline completed")
        return df_processed
    
    def save_preprocessor(self, filepath):
        """Save preprocessor objects to disk."""
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'onehot_encoders': self.onehot_encoders,
            'imputer': self.imputer,
            'feature_selector': self.feature_selector,
            'selected_features': self.selected_features,
            'categorical_columns': self.categorical_columns,
            'numerical_columns': self.numerical_columns
        }
        joblib.dump(preprocessor_data, filepath)
        logger.info(f"Saved preprocessor to {filepath}")
    
    def load_preprocessor(self, filepath):
        """Load preprocessor objects from disk."""
        preprocessor_data = joblib.load(filepath)
        self.scaler = preprocessor_data['scaler']
        self.label_encoders = preprocessor_data['label_encoders']
        self.onehot_encoders = preprocessor_data['onehot_encoders']
        self.imputer = preprocessor_data['imputer']
        self.feature_selector = preprocessor_data['feature_selector']
        self.selected_features = preprocessor_data['selected_features']
        self.categorical_columns = preprocessor_data['categorical_columns']
        self.numerical_columns = preprocessor_data['numerical_columns']
        logger.info(f"Loaded preprocessor from {filepath}")


def main():
    """Example usage."""
    # Example: Load data and preprocess
    # df = pd.read_csv('data/processed/dataset.csv')
    # preprocessor = DataPreprocessor()
    # df_processed = preprocessor.preprocess_pipeline(df, target_column='diagnosis')
    # df_processed.to_csv('data/processed/dataset_processed.csv', index=False)
    pass


if __name__ == "__main__":
    main()
