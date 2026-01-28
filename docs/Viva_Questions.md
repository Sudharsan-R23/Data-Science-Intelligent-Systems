# Viva Questions and Answers (Q&A)

### 1. General Project Questions
**Q: What is the main objective of your project?**
A: To build an end-to-end Decision Support System (DSS) using Machine Learning that helps doctors diagnose diseases like Diabetes and Heart Disease by providing risk scores and medical recommendations based on patient data.

**Q: Why did you choose a "Decision Support System" instead of an "Automated Diagnosis System"?**
A: In healthcare, AI should assist doctors, not replace them. A DSS provides data-driven evidence and suggestions which a professional can then validate, ensuring safety and accountability.

### 2. Machine Learning Questions
**Q: Which algorithm performed best and why?**
A: XGBoost and Random Forest performed best. This is because ensemble methods are excellent at handling non-linear relationships and interactions between medical features (e.g., how Age combined with Blood Pressure affects risk).

**Q: What is Feature Scaling and why did you use it?**
A: Feature scaling (we used StandardScaler) normalizes the range of independent variables. Since medical data has different units (Age in years, Glucose in mg/dL), scaling prevents features with larger ranges from dominating the model.

**Q: What are Precision and Recall in the context of your project?**
A: 
- **Precision**: Of all patients the model predicted as "High Risk," how many actually had the disease? (Avoids false alarms).
- **Recall**: Of all patients who actually had the disease, how many did the model correctly identify? (In healthcare, high Recall is often prioritized to avoid missing sick patients).

### 3. Technical & Implementation Questions
**Q: Why did you use FastAPI for the backend?**
A: FastAPI is high-performance, supports asynchronous programming, and automatically generates interactive API documentation (Swagger/OpenAPI), which speeds up development and testing.

**Q: How does the communication between React and the Python backend work?**
A: The React frontend sends a POST request with JSON-formatted patient data to a specific FastAPI endpoint (e.g., `/predict/diabetes`). The backend processes this with the ML model and returns a JSON response with the diagnosis and recommendations.

**Q: What is the purpose of Pydantic in your backend?**
A: We use Pydantic for data validation. It ensures that the data sent from the frontend meets the required schema (e.g., age must be an integer, glucose must be a number) before it reaches the ML model.

### 4. Future Scope Questions
**Q: How can you make this system production-ready?**
A: By implementing user authentication, ensuring HIPAA compliance for data privacy, integrating with live clinic databases (EHR), and deploying on a cloud platform like AWS or Azure.

**Q: How would you handle "Model Drift"?**
A: Medical standards and patient demographics change over time. We would need to periodically retrain the model with fresh data to ensure its accuracy remains high.
