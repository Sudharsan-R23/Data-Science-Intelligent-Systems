"""
Generate realistic sample healthcare datasets for demonstration
Creates datasets for Diabetes and Heart Disease diagnosis
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def generate_diabetes_dataset(n_samples=1000):
    """
    Generate a realistic diabetes dataset based on standard risk factors
    """
    print(f"Generating diabetes dataset with {n_samples} samples...")
    
    data = {
        'Pregnancies': np.random.randint(0, 17, n_samples),
        'Glucose': np.random.randint(44, 200, n_samples),
        'BloodPressure': np.random.randint(24, 122, n_samples),
        'SkinThickness': np.random.randint(7, 99, n_samples),
        'Insulin': np.random.randint(14, 846, n_samples),
        'BMI': np.round(np.random.uniform(18.2, 67.1, n_samples), 1),
        'DiabetesPedigreeFunction': np.round(np.random.uniform(0.078, 2.42, n_samples), 3),
        'Age': np.random.randint(21, 81, n_samples),
    }
    
    # Create realistic outcome based on risk factors
    # Higher risk with high glucose, BMI, age
    risk_score = (
        (data['Glucose'] > 140).astype(int) * 0.3 +
        (data['BMI'] > 30).astype(int) * 0.2 +
        (data['Age'] > 45).astype(int) * 0.2 +
        (data['Insulin'] > 200).astype(int) * 0.15 +
        (data['DiabetesPedigreeFunction'] > 0.5).astype(int) * 0.15 +
        np.random.uniform(0, 0.3, n_samples)  # Random noise
    )
    
    data['Outcome'] = (risk_score > 0.6).astype(int)
    
    df = pd.DataFrame(data)
    print(f"Diabetes dataset shape: {df.shape}")
    print(f"Positive cases: {df['Outcome'].sum()} ({df['Outcome'].mean()*100:.1f}%)")
    
    return df

def generate_heart_disease_dataset(n_samples=1000):
    """
    Generate a realistic heart disease dataset
    """
    print(f"\nGenerating heart disease dataset with {n_samples} samples...")
    
    data = {
        'Age': np.random.randint(29, 77, n_samples),
        'Sex': np.random.randint(0, 2, n_samples),  # 0=female, 1=male
        'ChestPainType': np.random.randint(0, 4, n_samples),  # 0-3: pain types
        'RestingBP': np.random.randint(94, 200, n_samples),
        'Cholesterol': np.random.randint(126, 564, n_samples),
        'FastingBS': np.random.randint(0, 2, n_samples),  # 0 or 1
        'RestingECG': np.random.randint(0, 3, n_samples),  # 0-2: ECG results
        'MaxHR': np.random.randint(71, 202, n_samples),
        'ExerciseAngina': np.random.randint(0, 2, n_samples),  # 0=no, 1=yes
        'Oldpeak': np.round(np.random.uniform(0, 6.2, n_samples), 1),
        'ST_Slope': np.random.randint(0, 3, n_samples),  # 0-2: slope types
    }
    
    # Create realistic outcome based on risk factors
    risk_score = (
        (data['Age'] > 55).astype(int) * 0.2 +
        (data['Cholesterol'] > 240).astype(int) * 0.2 +
        (data['RestingBP'] > 140).astype(int) * 0.15 +
        (data['ChestPainType'] >= 2).astype(int) * 0.15 +
        (data['ExerciseAngina'] == 1).astype(int) * 0.15 +
        (data['Oldpeak'] > 2).astype(int) * 0.10 +
        np.random.uniform(0, 0.3, n_samples)  # Random noise
    )
    
    data['HeartDisease'] = (risk_score > 0.5).astype(int)
    
    df = pd.DataFrame(data)
    print(f"Heart disease dataset shape: {df.shape}")
    print(f"Positive cases: {df['HeartDisease'].sum()} ({df['HeartDisease'].mean()*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("="*60)
    print("HEALTHCARE DATASET GENERATOR")
    print("="*60)
    
    # Generate and save diabetes dataset
    diabetes_df = generate_diabetes_dataset(1000)
    diabetes_path = data_dir / "diabetes_data.csv"
    diabetes_df.to_csv(diabetes_path, index=False)
    print(f"\nSaved to: {diabetes_path}")
    
    print("\nDiabetes Dataset Preview:")
    print(diabetes_df.head())
    print(f"\nColumns: {list(diabetes_df.columns)}")
    
    # Generate and save heart disease dataset
    heart_df = generate_heart_disease_dataset(1000)
    heart_path = data_dir / "heart_disease_data.csv"
    heart_df.to_csv(heart_path, index=False)
    print(f"\nSaved to: {heart_path}")
    
    print("\nHeart Disease Dataset Preview:")
    print(heart_df.head())
    print(f"\nColumns: {list(heart_df.columns)}")
    
    print("\n" + "="*60)
    print("DATASET GENERATION COMPLETE!")
    print("="*60)
    print(f"\nTotal datasets created: 2")
    print(f"Total samples: {len(diabetes_df) + len(heart_df)}")
