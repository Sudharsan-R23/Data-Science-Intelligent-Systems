# Sample Data Directory

## Purpose
This directory is for sample datasets and example CSV files.

## Dataset Format

Your medical dataset CSV should follow this structure:

### Example: Diabetes Dataset
```csv
pregnancies,glucose,blood_pressure,skin_thickness,insulin,bmi,diabetes_pedigree,age,diagnosis
6,148,72,35,0,33.6,0.627,50,1
1,85,66,29,0,26.6,0.351,31,0
8,183,64,0,0,23.3,0.672,32,1
...
```

### Example: Heart Disease Dataset
```csv
age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target
63,1,3,145,233,1,0,150,0,2.3,0,0,1,1
37,1,2,130,250,0,1,187,0,3.5,0,0,2,1
...
```

## Column Types

- **Numerical**: Age, glucose, blood pressure, BMI, etc.
- **Categorical**: Gender, diagnosis (0/1 or Positive/Negative)
- **Target Column**: Usually named 'diagnosis', 'target', or 'outcome'

## Notes

1. **Target Column**: Must be binary (0/1 or Positive/Negative)
2. **Missing Values**: Can be handled by preprocessing pipeline
3. **Encoding**: Categorical variables will be encoded automatically
4. **Normalization**: Numerical features will be normalized

## Getting Sample Datasets

You can find sample medical datasets at:
- UCI Machine Learning Repository
- Kaggle Datasets
- Medical research databases

## Important

- Replace sample data with your actual medical dataset
- Ensure data privacy and compliance with regulations
- Remove any personally identifiable information (PII)
