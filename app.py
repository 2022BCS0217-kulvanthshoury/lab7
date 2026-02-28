from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -------- Input schema --------
class InputData(BaseModel):
    features: List[float]

# -------- Health check --------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------- Prediction endpoint --------
@app.post("/predict")
def predict(data: InputData):
    if len(data.features) == 0:
        raise HTTPException(status_code=400, detail="Features cannot be empty")

    # Dummy model: sum of features
    prediction = sum(data.features)

    return {
        "prediction": prediction
    }