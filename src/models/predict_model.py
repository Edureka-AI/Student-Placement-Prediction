"""Prediction helpers for the placement API."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import os

import joblib
import pandas as pd
import mlflow
import mlflow.sklearn


def _get_model_path() -> Path:
    return Path(__file__).resolve().parents[2] / "models" / "model.pkl"


def _configure_tracking_uri() -> None:
    project_root = Path(__file__).resolve().parents[2]
    db_path = str(project_root / "mlflow.db").replace("\\", "/")
    mlflow.set_tracking_uri(f"sqlite:///{db_path}")


def _load_from_registry():
    model_name = os.getenv("MODEL_REGISTRY_NAME", "student-placement-model")
    model_alias = os.getenv("MODEL_REGISTRY_ALIAS", "production")
    model_uri = f"models:/{model_name}@{model_alias}"
    return mlflow.sklearn.load_model(model_uri)


@lru_cache(maxsize=1)
def load_model():
    # Optional registry-based loading for managed model versions.
    if os.getenv("USE_MODEL_REGISTRY", "false").lower() == "true":
        _configure_tracking_uri()
        return _load_from_registry()

    model_path = _get_model_path()
    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained model not found at {model_path}. "
            "Train the model before calling /predict."
        )
    return joblib.load(model_path)


def predict(features_dict: dict) -> object:
    if not features_dict:
        raise ValueError("features_dict cannot be empty")

    frame = pd.DataFrame([features_dict])
    model = load_model()
    prediction = model.predict(frame)
    if hasattr(prediction[0], "item"):
        return prediction[0].item()
    return prediction[0]
