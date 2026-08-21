import joblib
import pandas as pd
import shap
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "customer_churn_xgb_pipeline.pkl"
)

model = joblib.load(MODEL_PATH)

preprocessor = model.named_steps["preprocessor"]
xgb_model = model.named_steps["model"]

explainer = shap.TreeExplainer(xgb_model)

feature_names = preprocessor.get_feature_names_out()


def predict_churn(customer_data: dict):

    df = pd.DataFrame([customer_data])

    probability = model.predict_proba(df)[0][1]

    prediction = int(probability >= 0.50)

    if probability >= 0.70:
        risk = "High"
    elif probability >= 0.40:
        risk = "Medium"
    else:
        risk = "Low"

    processed_data = preprocessor.transform(df)

    shap_values = explainer.shap_values(processed_data)

    customer_shap = shap_values[0]

    impacts = pd.DataFrame({
        "feature": feature_names,
        "impact": customer_shap
    })

    impacts["absolute_impact"] = impacts["impact"].abs()

    top_features = (
        impacts
        .sort_values("absolute_impact", ascending=False)
        .head(5)
        [["feature", "impact"]]
        .to_dict(orient="records")
    )

    return {
        "churn_probability": round(float(probability), 4),
        "prediction": prediction,
        "risk_level": risk,
        "top_features": top_features
    }