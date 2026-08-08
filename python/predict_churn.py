"""
predict_churn.py — Score customers and generate ML predictions.

Usage:
    python predict_churn.py

Input:  data/processed/customer_churn_clean.csv, ml/churn_model.pkl
Output: data/processed/customer_churn_ml_predictions.csv
"""

import os
import pandas as pd
import numpy as np
import joblib


def load_model(path: str):
    """Load trained model."""
    model = joblib.load(path)
    print(f"Model loaded: {path}")
    return model


def load_clean_data(path: str) -> pd.DataFrame:
    """Load cleaned dataset."""
    df = pd.read_csv(path)
    print(f"Data loaded: {path} ({df.shape[0]} rows)")
    return df


def generate_predictions(df: pd.DataFrame, model) -> pd.DataFrame:
    """Generate churn predictions for all customers."""
    numeric_features = ["age", "tenure", "monthly_charges", "support_calls"]
    categorical_features = ["contract_type", "gender", "internet_service", "payment_method"]

    X = df[numeric_features + categorical_features]

    # Predict probabilities
    churn_probability = model.predict_proba(X)[:, 1]

    # Add prediction columns
    df["churn_probability"] = churn_probability
    df["churn_probability_pct"] = np.round(churn_probability * 100, 2)

    # ML risk levels
    def assign_ml_risk_level(prob):
        if prob >= 0.70:
            return "High"
        elif prob >= 0.40:
            return "Medium"
        else:
            return "Low"

    df["ml_risk_level"] = df["churn_probability"].apply(assign_ml_risk_level)

    # Revenue exposure
    df["expected_revenue_risk"] = np.round(df["churn_probability"] * df["monthly_charges"], 2)

    print(f"\nPredictions generated:")
    print(f"  High Risk: {(df['ml_risk_level'] == 'High').sum()}")
    print(f"  Medium Risk: {(df['ml_risk_level'] == 'Medium').sum()}")
    print(f"  Low Risk: {(df['ml_risk_level'] == 'Low').sum()}")
    print(f"  Total expected revenue risk: ${df['expected_revenue_risk'].sum():,.2f}")

    return df


def save_predictions(df: pd.DataFrame, path: str) -> None:
    """Save final predictions dataset."""
    output_cols = [
        "customer_id", "age", "gender", "tenure", "monthly_charges",
        "contract_type", "support_calls", "internet_service", "payment_method",
        "total_charges", "churn",
        "churn_probability", "churn_probability_pct",
        "ml_risk_level", "expected_revenue_risk"
    ]

    df_output = df[output_cols].copy()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df_output.to_csv(path, index=False)
    print(f"Saved: {path} ({df_output.shape[0]} rows, {df_output.shape[1]} columns)")


def main():
    clean_path = os.path.join("data", "processed", "customer_churn_clean.csv")
    model_path = os.path.join("ml", "churn_model.pkl")
    output_path = os.path.join("data", "processed", "customer_churn_ml_predictions.csv")

    print("=== Churn Prediction Pipeline ===\n")

    model = load_model(model_path)
    df = load_clean_data(clean_path)
    df = generate_predictions(df, model)
    save_predictions(df, output_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
