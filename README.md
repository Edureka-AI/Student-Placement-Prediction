# Student Placement Prediction System

A machine learning system that predicts student job placement outcomes using scikit-learn and provides predictions via a FastAPI REST endpoint. The project includes comprehensive MLOps features with MLflow experiment tracking, model registry support, and Airflow pipeline orchestration.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Model Training](#model-training)
- [Deployment](#deployment)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## Features

- **ML Model**: Random Forest Classifier for binary placement prediction
- **MLOps Integration**: MLflow experiment tracking and model registry
- **REST API**: FastAPI-based prediction endpoint with logging
- **Data Pipeline**: Automated data preprocessing with Airflow DAG
- **Model Evaluation**: Comprehensive metrics (accuracy, precision, recall, F1)
- **Docker Support**: Containerized deployment ready
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing and deployment

## Project Structure

```
├── data/                          # Data directory
│   ├── raw/                       # Raw input data
│   │   └── student_placement_data_v1.csv
│   ├── interim/                   # Intermediate processed data
│   └── processed/                 # Final processed data
├── models/                        # Trained model storage
│   └── model.pkl                  # Serialized RandomForest model
├── reports/                       # Generated reports & metrics
│   └── figures/                   # Visualization outputs
├── notebooks/                     # Jupyter notebooks for exploration
├── src/                           # Source code
│   ├── api.py                     # FastAPI application
│   ├── train_model.py             # Model training entrypoint
│   ├── evaluate_model.py          # Model evaluation & metrics
│   ├── data_preprocessing.py      # Data cleaning & preprocessing
│   ├── data/                      # Data processing modules
│   │   └── make_dataset.py        # Dataset creation utilities
│   ├── features/                  # Feature engineering modules
│   │   └── build_features.py      # Feature extraction (extensible)
│   ├── models/                    # Model modules
│   │   ├── train_model.py         # Core training logic
│   │   ├── predict_model.py       # Inference utilities
│   │   └── model_registry.py      # MLflow registry management
│   ├── visualization/             # Visualization utilities
│   │   └── visualize.py           # Plotting & reporting
│   └── frontend/                  # Web interface
│       ├── index.html             # UI entry point
│       └── static/                # Static assets
├── dags/                          # Apache Airflow DAGs
│   └── pipeline_dag.py            # ML pipeline orchestration
├── mlruns/                        # MLflow experiment tracking data
├── Dockerfile                     # Container configuration
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
├── Makefile                       # Development commands
├── test_environment.py            # Environment validation script
└── README.md                      # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or conda package manager
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Edureka-AI/Student-Placement-Prediction.git
   cd "Student Placement Project"
   ```

2. **Verify Python environment**
   ```bash
   python test_environment.py
   ```
   Expected output: `>>> Development environment passes all tests!`

3. **Install dependencies**
   ```bash
   make requirements
   ```
   Or manually:
   ```bash
   pip install -U pip setuptools wheel
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import pandas; import sklearn; import mlflow; import joblib; print('✓ All dependencies installed')"
   ```

## Quick Start

### 1. Prepare Data

```bash
python src/data_preprocessing.py
```

This will:
- Load raw data from `data/raw/student_placement_data_v1.csv`
- Remove duplicates
- Save cleaned data to `data/raw/student_placement_data.csv`

### 2. Train Model

```bash
python src/models/train_model.py
```

This will:
- Split data into train/test sets (80/20)
- Train a RandomForest classifier with 100 estimators
- Log experiments and metrics to MLflow
- Save model to `models/model.pkl`
- Output accuracy score

Example output:
```
Model trained successfully! Accuracy: 0.92
```

### 3. Evaluate Model

```bash
python src/evaluate_model.py
```

This will:
- Load the trained model
- Compute evaluation metrics
- Save results to `reports/evaluation_metrics.json`

Metrics generated:
- **Accuracy**: Overall correctness
- **Precision**: True positives / (true positives + false positives)
- **Recall**: True positives / (true positives + false negatives)
- **F1-Score**: Harmonic mean of precision and recall

### 4. Run Prediction API

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Server will start at `http://localhost:8000`

## API Documentation

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{"message": "ML API running"}
```

#### 2. Make Prediction
```http
POST /predict
Content-Type: application/json

{
  "data": {
    "feature1": 1.5,
    "feature2": 2.0,
    "feature3": 0,
    ...
  }
}
```

**Response (Success - 200):**
```json
{"prediction": 1}
```

**Response (Missing Model - 503):**
```json
{"detail": "Trained model not found at models/model.pkl. Train the model before calling /predict."}
```

**Response (Invalid Input - 400):**
```json
{"detail": "features_dict cannot be empty"}
```

### Usage Examples

**Using curl:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"data": {"feature1": 1.5, "feature2": 2.0}}'
```

**Using Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"data": {"feature1": 1.5, "feature2": 2.0}}
)
print(response.json())
```

**Using Python http.client:**
```python
import http.client
import json

conn = http.client.HTTPConnection("localhost", 8000)
payload = json.dumps({"data": {"feature1": 1.5, "feature2": 2.0}})
conn.request("POST", "/predict", payload, {"Content-Type": "application/json"})
response = conn.getresponse()
print(response.read().decode())
```

### Logging

All predictions are logged to `logs/predictions.log` with the following format:
```
INFO:root:prediction_request={...} prediction={result}
```

## Model Training

### Training Process

The model training pipeline:

1. **Data Loading**: Loads `data/raw/student_placement_data.csv`
2. **Train-Test Split**: 80% training, 20% testing (random_state=42)
3. **Model Training**: RandomForestClassifier with:
   - n_estimators: 100
   - random_state: 42
4. **Evaluation**: Accuracy computed on test set
5. **Logging**: MLflow tracks params, metrics, and artifacts
6. **Persistence**: Model saved as `models/model.pkl`

### MLflow Integration

View experiments and runs:
```bash
mlflow ui
```

Then open `http://localhost:5000` in your browser

**MLflow Configuration:**
- Tracking URI: `sqlite:///mlflow.db`
- Experiment: "Student Placement Prediction"
- Artifacts: Stored in `mlruns/` directory

### Model Registry (Optional)

For managed model versions:

```bash
# Register latest run
python src/models/model_registry_demo.py register

# List all versions
python src/models/model_registry_demo.py list

# Promote to production
python src/models/model_registry_demo.py set-alias --alias production --version 1

# Load by alias
python src/models/model_registry_demo.py load --alias production
```

To use registry-managed models in the API:
```bash
export USE_MODEL_REGISTRY=true
export MODEL_REGISTRY_NAME=student-placement-model
export MODEL_REGISTRY_ALIAS=production
uvicorn src.api:app
```

## Deployment

### Docker Deployment

1. **Build Docker image:**
   ```bash
   docker build -t student-placement:latest .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 -v $(pwd)/models:/app/models student-placement:latest
   ```

3. **Access API:**
   ```
   http://localhost:8000
   ```

### Dockerfile Details

- **Base Image**: `python:3.10-slim`
- **Workdir**: `/app`
- **Port**: 8000
- **Default Command**: `python main.py`

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| USE_MODEL_REGISTRY | false | Enable MLflow model registry |
| MODEL_REGISTRY_NAME | student-placement-model | Registry model name |
| MODEL_REGISTRY_ALIAS | production | Model alias to load |

### Deployment Checklist

- [ ] Run `python test_environment.py` ✓
- [ ] All Python files pass syntax validation ✓
- [ ] Dependencies installed successfully ✓
- [ ] Model trained and available at `models/model.pkl` ✓
- [ ] API starts without errors
- [ ] Predictions working via `/predict` endpoint
- [ ] Logs generated in `logs/predictions.log`
- [ ] Docker image builds successfully
- [ ] Container runs on target port

## Development

### Available Commands

```bash
# Install dependencies
make requirements

# Create datasets
make data

# Run linting
make lint

# Clean Python cache files
make clean

# Sync data to S3 (requires AWS setup)
make sync_data_to_s3
make sync_data_from_s3
```

### Development Workflow

1. **Data exploration**: Use Jupyter notebooks in `notebooks/`
2. **Feature development**: Extend `src/features/build_features.py`
3. **Model experimentation**: Modify `src/models/train_model.py`
4. **Testing**: Run validation via `test_environment.py`
5. **Linting**: Check code style with `make lint`

### GitHub Actions CI/CD

The project includes automated workflows:

- **CI**: Runs on PRs and pushes to main/master
  - Environment validation
  - Linting with flake8
  - Python 3.10+ compatibility check

- **CD**: Runs on version tags (e.g., `v0.1.1`)
  - Builds package
  - Publishes to PyPI (if `PYPI_API_TOKEN` is configured)

See `.github/workflows/ci-cd.yml` for details

### Extending the Project

**Add new features:**
```python
# src/features/build_features.py
def extract_feature_x(data):
    # Your feature logic
    return feature_values
```

**Add visualization:**
```python
# src/visualization/visualize.py
def plot_results(predictions):
    # Your plotting logic
    pass
```

## Troubleshooting

### Common Issues

#### 1. Module Not Found Error
```
ModuleNotFoundError: No module named 'mlflow'
```

**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. Dataset Not Found
```
FileNotFoundError: No input dataset found in data/raw/
```

**Solution:**
- Ensure `student_placement_data_v1.csv` exists in `data/raw/`
- Run preprocessing: `python src/data_preprocessing.py`

#### 3. Model Not Found for Prediction
```
FileNotFoundError: Trained model not found at models/model.pkl
```

**Solution:**
- Train the model first: `python src/models/train_model.py`

#### 4. Port Already in Use
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Use different port
uvicorn src.api:app --port 8001

# Or kill process using port 8000
# Windows: netstat -ano | findstr :8000
# Unix: lsof -i :8000
```

#### 5. Python Version Mismatch
```
TypeError: This project requires Python 3. Found: Python 2
```

**Solution:**
```bash
python3 test_environment.py
python3 -m pip install -r requirements.txt
```

### Performance Optimization

1. **Increase model ensemble**: Modify `n_estimators` in `src/models/train_model.py`
2. **Tune hyperparameters**: Use grid search in feature development
3. **Parallel prediction**: Deploy multiple API instances behind load balancer

### Debugging

1. **Enable verbose logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check MLflow runs:**
   ```bash
   mlflow ui
   ```

3. **Inspect predictions locally:**
   ```python
   from src.models.predict_model import predict
   result = predict({"feature1": 1.5, "feature2": 2.0})
   print(result)
   ```

## CI/CD Configuration

### GitHub Setup

1. **Create GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M master
   git remote add origin https://github.com/Edureka-AI/Student-Placement-Prediction.git
   git push -u origin master
   ```

2. **Add PyPI token (optional):**
   - Go to repository Settings → Secrets
   - Add `PYPI_API_TOKEN` for PyPI publishing

3. **Release process:**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   # GitHub Actions automatically builds and publishes
   ```

## Airflow Pipeline

### DAG Specification

- **DAG ID**: `ml_pipeline`
- **Schedule**: Daily (`@daily`)
- **Owner**: airflow
- **Retries**: 1

### DAG Tasks

1. **data_preprocessing**: Cleans raw data
2. **model_training**: Trains RandomForest classifier
3. **model_evaluation**: Computes evaluation metrics

### Running DAG

```bash
airflow db init
airflow webserver  # Access at http://localhost:8080
airflow scheduler
```

## Contact & Support

- **Repository**: https://github.com/Edureka-AI/Student-Placement-Prediction
- **Issues**: GitHub Issues page
- **Author**: Your Organization/Team

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
