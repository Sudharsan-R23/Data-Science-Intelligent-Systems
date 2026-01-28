# System Architecture & Diagrams

## 1. System Architecture
The system follows a standard Client-Server architecture with a decoupled ML inference engine.

```mermaid
graph TD
    Client[Client Browser (React App)]
    API[FastAPI Backend Server]
    ML[ML Inference Engine]
    Models[(Trained Models .pkl)]
    Data[(Data Processing Pipeline)]

    Client -- HTTPS/JSON --> API
    API -- Input Data --> ML
    ML -- Load --> Models
    ML -- Preprocess --> Data
    ML -- Prediction --> API
    API -- Response --> Client
```

## 2. Data Flow Diagram (DFD) - Level 0

```mermaid
graph LR
    User((Doctor)) -- Enters Patient Data --> System[Healthcare DSS]
    System -- Returns Prediction & Advice --> User
```

## 3. Data Flow Diagram (DFD) - Level 1

```mermaid
graph LR
    User((Doctor))
    Input[Input Interface]
    Validate[Validation Service]
    Predict[Prediction Module]
    Recomm[Recommendation Engine]
    Output[Result Display]

    User -- Input Data --> Input
    Input -- Raw Data --> Validate
    Validate -- Validated Data --> Predict
    Predict -- Risk Score --> Recomm
    Predict -- Probability --> Output
    Recomm -- Medical Advice --> Output
    Output -- Report --> User
```

## 4. Activity Diagram (Prediction Workflow)

```mermaid
stateDiagram-v2
    [*] --> SelectDisease
    SelectDisease --> EnterData
    EnterData --> ValidateInput
    
    state ValidateInput {
        [*] --> CheckRanges
        CheckRanges --> Valid: Yes
        CheckRanges --> Invalid: No
        Invalid --> ShowError
        ShowError --> [*]
    }

    Valid --> PreprocessData
    PreprocessData --> LoadModel
    LoadModel --> GeneratePrediction
    GeneratePrediction --> CalculateProbability
    CalculateProbability --> GenerateAdvice
    GenerateAdvice --> DisplayResults
    DisplayResults --> [*]
```

## 5. Technology Stack
| Component | Technology | Description |
|-----------|------------|-------------|
| **Frontend** | React.js | Component-based UI library |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **Backend** | FastAPI | High-performance Python web framework |
| **ML Libraries** | Scikit-learn, XGBoost | Model training and inference |
| **Data Processing** | Pandas, NumPy | Data manipulation and analysis |
| **Serialization** | Pickle | Model persistence |
| **Validation** | Pydantic | Data validation and settings management |
