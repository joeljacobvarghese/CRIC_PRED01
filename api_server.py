from fastapi import FastAPI
from pydantic import BaseModel, Field
from joblib import load
import numpy as np

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    runs: int = Field(..., example=100)
    wickets: int = Field(..., example=2)
    overs: float = Field(..., example=10.5)
    second_innings: bool = Field(..., example=False)
    chasing_score: int = Field(-1, example=250)

# Load models for both innings
models_first_innings = {
    'linear': load('models/linear_regression_model_First.joblib'),
    'poly': load('models/polynomial_regression_model_First.joblib'),
    'svr': load('models/svr_model_First.joblib'),
}

models_second_innings = {
    'linear': load('models/linear_regression_model_Second.joblib'),
    'poly': load('models/polynomial_regression_model_Second.joblib'),
    'svr': load('models/svr_model_Second.joblib'),
}

@app.post("/predict/")
async def make_prediction(request: PredictionRequest):
    # Determine which set of models to use based on the innings
    models = models_second_innings if request.second_innings else models_first_innings

    # Prepare features
    features = np.array([
        [request.runs, request.overs, request.wickets] + ([request.chasing_score] if request.second_innings else [])
    ])

   
    linear_pred = models['linear'].predict(features)[0]
    poly_pred = models['poly'].predict(features)[0]
    svr_pred = models['svr'].predict(features)[0]

    
    aggregate_pred = np.mean([linear_pred, poly_pred, svr_pred])

    
    return {
        "linear_regression_prediction": linear_pred,
        "polynomial_regression_prediction": poly_pred,
        "svr_prediction": svr_pred,
        "aggregate_prediction": aggregate_pred
    }
