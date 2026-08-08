"""
train_model.py — Train and evaluate churn prediction models.

Usage:
    python train_model.py

Input:  data/processed/customer_churn_clean.csv
Output: ml/churn_model.pkl, ml/model_metrics.json
"""

import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report
)


def load_clean_data(path: str) -> pd.DataFrame:
    """Load cleaned dataset."""
    df = pd.read_csv(path)
    print(f"Loaded: {path} ({df.shape[0]} rows)")
    return df


def prepare_features(df: pd.DataFrame):
    """Define features, target, and train/test split."""
    df["churn_target"] = (df["churn"] == "Yes").astype(int)

    numeric_features = ["age", "tenure", "monthly_charges", "support_calls"]
    categorical_features = ["contract_type", "gender", "internet_service", "payment_method"]

    X = df[numeric_features + categorical_features]
    y = df["churn_target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Train: {X_train.shape[0]} samples, Test: {X_test.shape[0]} samples")
    print(f"Train churn rate: {y_train.mean()*100:.2f}%, Test churn rate: {y_test.mean()*100:.2f}%")

    return X_train, X_test, y_train, y_test, numeric_features, categorical_features


def build_preprocessor(numeric_features, categorical_features):
    """Build sklearn preprocessing pipeline."""
    return ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), categorical_features)
        ]
    )


def evaluate_model(name, pipeline, X_test, y_test):
    """Evaluate model and return metrics dict."""
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_prob)
    }

    print(f"\n=== {name} ===")
    for m, v in metrics.items():
        print(f"  {m}: {v:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["No Churn", "Churn"]))

    return metrics


def select_best_model(lr_metrics, rf_metrics):
    """Select best model based on Recall + ROC-AUC priority."""
    print("\n=== Model Selection ===")
    if rf_metrics["Recall"] >= lr_metrics["Recall"] and rf_metrics["ROC-AUC"] >= lr_metrics["ROC-AUC"]:
        return "Random Forest", rf_metrics
    elif lr_metrics["Recall"] > rf_metrics["Recall"]:
        return "Logistic Regression", lr_metrics
    else:
        return "Random Forest", rf_metrics


def train_and_evaluate():
    """Main training pipeline."""
    clean_path = os.path.join("data", "processed", "customer_churn_clean.csv")
    model_path = os.path.join("ml", "churn_model.pkl")
    metrics_path = os.path.join("ml", "model_metrics.json")

    print("=== Churn Model Training Pipeline ===\n")

    # Load data
    df = load_clean_data(clean_path)

    # Prepare features
    X_train, X_test, y_train, y_test, num_feats, cat_feats = prepare_features(df)

    # Build preprocessor
    preprocessor = build_preprocessor(num_feats, cat_feats)

    # Train Logistic Regression
    lr_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42))
    ])
    lr_pipeline.fit(X_train, y_train)
    lr_metrics = evaluate_model("Logistic Regression", lr_pipeline, X_test, y_test)

    # Train Random Forest
    rf_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=300, max_depth=10, random_state=42, class_weight="balanced"
        ))
    ])
    rf_pipeline.fit(X_train, y_train)
    rf_metrics = evaluate_model("Random Forest", rf_pipeline, X_test, y_test)

    # Select best model
    best_name, best_metrics = select_best_model(lr_metrics, rf_metrics)

    if best_name == "Random Forest":
        best_pipeline = rf_pipeline
    else:
        best_pipeline = lr_pipeline

    # Refit on full data for deployment
    X_full = df[num_feats + cat_feats]
    y_full = (df["churn"] == "Yes").astype(int)
    best_pipeline.fit(X_full, y_full)

    # Save model
    os.makedirs("ml", exist_ok=True)
    joblib.dump(best_pipeline, model_path)
    print(f"\nModel saved: {model_path}")

    # Save metrics
    model_metrics = {
        "model": best_name,
        "accuracy": round(best_metrics["Accuracy"], 4),
        "precision": round(best_metrics["Precision"], 4),
        "recall": round(best_metrics["Recall"], 4),
        "f1_score": round(best_metrics["F1 Score"], 4),
        "roc_auc": round(best_metrics["ROC-AUC"], 4)
    }
    with open(metrics_path, "w") as f:
        json.dump(model_metrics, f, indent=4)
    print(f"Metrics saved: {metrics_path}")
    print(json.dumps(model_metrics, indent=4))

    return best_pipeline, model_metrics


if __name__ == "__main__":
    train_and_evaluate()
