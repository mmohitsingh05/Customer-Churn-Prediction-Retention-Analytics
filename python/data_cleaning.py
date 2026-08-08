"""
data_cleaning.py — Clean raw customer data and engineer features.

Usage:
    python data_cleaning.py

Input:  data/raw/customer_churn.csv
Output: data/processed/customer_churn_clean.csv
"""

import os
import pandas as pd
import numpy as np


def load_raw_data(path: str) -> pd.DataFrame:
    """Load raw CSV and perform basic validation."""
    df = pd.read_csv(path)
    print(f"Loaded: {path} ({df.shape[0]} rows, {df.shape[1]} columns)")
    return df


def validate_data(df: pd.DataFrame) -> None:
    """Check data quality: nulls, duplicates."""
    null_count = df.isnull().sum().sum()
    dup_count = df.duplicated().sum()
    dup_ids = df["customer_id"].duplicated().sum()

    print(f"Null values: {null_count}")
    print(f"Duplicate rows: {dup_count}")
    print(f"Duplicate customer_ids: {dup_ids}")

    if null_count > 0:
        raise ValueError(f"Found {null_count} null values — fix generator before proceeding")
    if dup_count > 0:
        raise ValueError(f"Found {dup_count} duplicate rows — fix generator before proceeding")
    if dup_ids > 0:
        raise ValueError(f"Found {dup_ids} duplicate customer_ids — fix generator before proceeding")

    print("Data quality checks passed!")


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add engineered columns for EDA."""
    # Age groups
    bins = [0, 25, 35, 45, 55, 65, 100]
    labels = ["18-25", "26-35", "36-45", "46-55", "56-65", "66+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)

    # Tenure groups
    tenure_bins = [0, 6, 12, 24, 48, 72]
    tenure_labels = ["0-6 Months", "7-12 Months", "13-24 Months", "25-48 Months", "49-72 Months"]
    df["tenure_group"] = pd.cut(df["tenure"], bins=tenure_bins, labels=tenure_labels)

    # Churn numeric
    df["churn_numeric"] = (df["churn"] == "Yes").astype(int)

    # Rule-based risk score (NOT ML)
    def calculate_risk_score(row):
        score = 0
        if row["contract_type"] == "Month-to-month":
            score += 2
        if row["support_calls"] >= 5:
            score += 2
        if row["tenure"] <= 12:
            score += 2
        if row["monthly_charges"] >= 100:
            score += 1
        return score

    df["risk_score"] = df.apply(calculate_risk_score, axis=1)

    # Risk level
    def assign_risk_level(score):
        if score >= 5:
            return "High"
        elif score >= 3:
            return "Medium"
        else:
            return "Low"

    df["risk_level"] = df["risk_score"].apply(assign_risk_level)

    print(f"Engineered features added: age_group, tenure_group, churn_numeric, risk_score, risk_level")
    return df


def save_clean_data(df: pd.DataFrame, path: str) -> None:
    """Save cleaned dataset."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved: {path} ({df.shape[0]} rows, {df.shape[1]} columns)")


def main():
    raw_path = os.path.join("data", "raw", "customer_churn.csv")
    clean_path = os.path.join("data", "processed", "customer_churn_clean.csv")

    print("=== Data Cleaning Pipeline ===\n")
    df = load_raw_data(raw_path)
    validate_data(df)
    df = engineer_features(df)
    save_clean_data(df, clean_path)
    print("\nDone!")


if __name__ == "__main__":
    main()
