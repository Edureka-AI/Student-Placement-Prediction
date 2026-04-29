from pathlib import Path
import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.models.predict_model import predict

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"

# Create logs folder
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/predictions.log",
    level=logging.INFO
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class InputData(BaseModel):
    data: dict

@app.get("/")
def serve_ui():
    return FileResponse("src/frontend/index.html")

@app.get("/health")
def health_check():
    return {"message": "ML API running"}


@app.post("/predict")
def get_prediction(input: InputData):
    try:
        result = predict(input.data)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logging.info("prediction_request=%s prediction=%s", input.data, result)
    return {"prediction": result}
