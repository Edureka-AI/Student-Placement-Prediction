"""Train model for student placement and track runs with MLflow."""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from pathlib import Path

import mlflow
import mlflow.sklearn


EXPERIMENT_NAME = "Student Placement Prediction"


def get_project_root():
    return Path(__file__).resolve().parents[2]


def configure_mlflow():
    project_root = get_project_root()
    mlflow_db_path = str(project_root / "mlflow.db").replace("\\", "/")

    mlflow.set_tracking_uri(f"sqlite:///{mlflow_db_path}")
    mlflow.set_experiment(EXPERIMENT_NAME)


def train():
    project_root = get_project_root()
    configure_mlflow()

    # Load dataset
    df = pd.read_csv(
        project_root / "data" / "raw" / "student_placement_data.csv"
    )

    # Features and target
    X = df.drop("Placement", axis=1)
    y = df["Placement"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run():

        n_estimators = 100
        random_state = 42

        # Train model
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Log params
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("random_state", random_state)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)

        # Save locally
        models_dir = project_root / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, models_dir / "model.pkl")

        mlflow.sklearn.log_model(model, "model")

        print(f"Model trained successfully! Accuracy: {accuracy}")


if __name__ == "__main__":
    train()