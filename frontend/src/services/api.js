import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const checkHealth = async () => {
    try {
        const response = await api.get('/');
        return response.data;
    } catch (error) {
        console.error('API Health Check Failed:', error);
        throw error;
    }
};

export const predictDiabetes = async (data) => {
    try {
        // Ensure numeric values are sent as numbers
        const payload = {
            Pregnancies: Number(data.Pregnancies),
            Glucose: Number(data.Glucose),
            BloodPressure: Number(data.BloodPressure),
            SkinThickness: Number(data.SkinThickness),
            Insulin: Number(data.Insulin),
            BMI: Number(data.BMI),
            DiabetesPedigreeFunction: Number(data.DiabetesPedigreeFunction),
            Age: Number(data.Age)
        };

        const response = await api.post('/predict/diabetes', payload);
        return response.data;
    } catch (error) {
        console.error('Diabetes Prediction Failed:', error);
        throw error;
    }
};

export const predictHeartDisease = async (data) => {
    try {
        // Ensure numeric values are sent as numbers
        const payload = {
            Age: Number(data.Age),
            Sex: Number(data.Sex),
            ChestPainType: Number(data.ChestPainType),
            RestingBP: Number(data.RestingBP),
            Cholesterol: Number(data.Cholesterol),
            FastingBS: Number(data.FastingBS),
            RestingECG: Number(data.RestingECG),
            MaxHR: Number(data.MaxHR),
            ExerciseAngina: Number(data.ExerciseAngina),
            Oldpeak: Number(data.Oldpeak),
            ST_Slope: Number(data.ST_Slope)
        };

        const response = await api.post('/predict/heart-disease', payload);
        return response.data;
    } catch (error) {
        console.error('Heart Disease Prediction Failed:', error);
        throw error;
    }
};
