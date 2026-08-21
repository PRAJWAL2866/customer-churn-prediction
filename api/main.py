from fastapi import FastAPI
from schema import CustomerData
from predictor import predict_churn

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Explainable customer churn prediction using XGBoost and SHAP",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is running!"
    }


@app.post("/predict")
def predict(data: CustomerData):
    return predict_churn(data.model_dump())