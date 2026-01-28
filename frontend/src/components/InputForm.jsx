import React, { useState } from 'react';

const InputForm = ({ modelType, onSubmit, loading }) => {
    const [formData, setFormData] = useState({});

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    const diabetesFields = [
        { name: 'Pregnancies', label: 'Pregnancies', type: 'number', placeholder: '0' },
        { name: 'Glucose', label: 'Glucose (mg/dL)', type: 'number', placeholder: '120' },
        { name: 'BloodPressure', label: 'Blood Pressure', type: 'number', placeholder: '80' },
        { name: 'SkinThickness', label: 'Skin Thickness', type: 'number', placeholder: '20' },
        { name: 'Insulin', label: 'Insulin', type: 'number', placeholder: '85' },
        { name: 'BMI', label: 'BMI', type: 'number', step: '0.1', placeholder: '24.5' },
        { name: 'DiabetesPedigreeFunction', label: 'Diabetes Pedigree', type: 'number', step: '0.001', placeholder: '0.47' },
        { name: 'Age', label: 'Age', type: 'number', placeholder: '45' },
    ];

    const heartFields = [
        { name: 'Age', label: 'Age', type: 'number', placeholder: '52' },
        { name: 'Sex', label: 'Sex', type: 'select', options: [{ value: 1, label: 'Male' }, { value: 0, label: 'Female' }, { value: 0, label: 'Lesban' }] },
        { name: 'ChestPainType', label: 'Chest Pain', type: 'select', options: [{ value: 0, label: 'Type 0' }, { value: 1, label: 'Type 1' }, { value: 2, label: 'Type 2' }, { value: 3, label: 'Type 3' }] },
        { name: 'RestingBP', label: 'Resting BP', type: 'number', placeholder: '130' },
        { name: 'Cholesterol', label: 'Cholesterol', type: 'number', placeholder: '210' },
        { name: 'FastingBS', label: 'Fasting BS > 120', type: 'select', options: [{ value: 0, label: 'No' }, { value: 1, label: 'Yes' }] },
        { name: 'RestingECG', label: 'Resting ECG', type: 'select', options: [{ value: 0, label: '0' }, { value: 1, label: '1' }, { value: 2, label: '2' }] },
        { name: 'MaxHR', label: 'Max Heart Rate', type: 'number', placeholder: '160' },
        { name: 'ExerciseAngina', label: 'Exercise Angina', type: 'select', options: [{ value: 0, label: 'No' }, { value: 1, label: 'Yes' }] },
        { name: 'Oldpeak', label: 'Oldpeak (ST)', type: 'number', step: '0.1', placeholder: '1.2' },
        { name: 'ST_Slope', label: 'ST Slope', type: 'select', options: [{ value: 0, label: '0' }, { value: 1, label: '1' }, { value: 2, label: '2' }] },
    ];

    const fields = modelType === 'diabetes' ? diabetesFields : heartFields;

    return (
        <form onSubmit={handleSubmit} className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {fields.map((field) => (
                    <div key={field.name} className="flex flex-col">
                        <label className="text-[10px] font-black text-brand-accent/60 uppercase tracking-[0.2em] mb-3 ml-1">
                            {field.label}
                        </label>
                        {field.type === 'select' ? (
                            <select
                                name={field.name}
                                required
                                className="input-field appearance-none bg-[url('data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20fill%3D%22none%22%20viewBox%3D%220%200%2020%2020%22%3E%3Cpath%20stroke%3D%22%239A8873%22%20stroke-opacity%3D%220.5%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%20stroke-width%3D%221.5%22%20d%3D%22m6%208%204%204%204-4%22%2F%3E%3C%2Fsvg%3E')] bg-[length:1.25rem_1.25rem] bg-[right_1rem_center] bg-no-repeat"
                                onChange={handleChange}
                                defaultValue=""
                            >
                                <option value="" disabled className="bg-brand-surface text-brand-text">Select {field.label}</option>
                                {field.options.map(opt => (
                                    <option key={opt.value} value={opt.value} className="bg-brand-surface text-brand-text">{opt.label}</option>
                                ))}
                            </select>
                        ) : (
                            <input
                                type={field.type}
                                name={field.name}
                                step={field.step || "1"}
                                required
                                placeholder={field.placeholder}
                                className="input-field placeholder:text-brand-accent/20"
                                onChange={handleChange}
                            />
                        )}
                    </div>
                ))}
            </div>

            <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary mt-8 mb-4 overflow-hidden relative group"
            >
                {loading ? (
                    <div className="flex items-center justify-center space-x-3">
                        <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                        <span className="tracking-widest uppercase text-xs font-black">Processing...</span>
                    </div>
                ) : (
                    <span className="flex items-center justify-center space-x-2">
                        <span className="tracking-widest uppercase text-xs font-black">Run System Analysis</span>
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                        </svg>
                    </span>
                )}
            </button>
        </form>
    );
};

export default InputForm;
