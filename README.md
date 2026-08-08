# Customer Churn Prediction & Retention Analytics

## Overview

An end-to-end customer churn analytics and machine-learning solution designed to identify churn drivers, predict high-risk customers, quantify revenue exposure, and support data-driven retention strategies.

---

## Business Problem

Customer churn directly impacts recurring revenue. This project answers:

- Who is likely to churn?
- Why are customers leaving?
- How much revenue is exposed?
- Which customers should the company prioritize?
- What retention strategies should management implement?

---

## Objectives

- Calculate customer churn and retention rates
- Identify major churn drivers
- Analyze customer behavior using SQL and Python
- Build a machine-learning churn prediction model
- Estimate customer-level churn probability
- Identify high-risk customers
- Quantify revenue exposure
- Build an interactive Power BI dashboard
- Provide actionable retention recommendations

---

## Tech Stack

Python · Pandas · NumPy · Matplotlib · Seaborn · Scikit-learn · PostgreSQL · SQL · Power BI · Git · GitHub

---

## Project Architecture

```
Customer Data
    ↓
Python Data Cleaning
    ↓
EDA & Statistical Analysis
    ↓
PostgreSQL SQL Analysis
    ↓
Machine Learning
    ↓
Churn Probability
    ↓
Risk Segmentation
    ↓
Power BI Dashboard
    ↓
Retention Strategy
```

---

## Dataset

Synthetic customer dataset (5,000 rows) containing demographics, subscription info, support interactions, billing data, and churn status.

**Features:** `customer_id`, `age`, `gender`, `tenure`, `monthly_charges`, `contract_type`, `support_calls`, `internet_service`, `payment_method`, `total_charges`, `churn`

---

## Data Analysis

- **Churn Rate:** 33.46%
- **Retention Rate:** 66.54%
- **Revenue at Risk:** $147,335/month
- **High-Risk Customers:** 420 (8.4%)

### Key SQL Insights:
| Segment | Churn Rate |
|---------|------------|
| Month-to-month | 41.25% |
| 0-6 month tenure | 48.65% |
| 5+ support calls | 40-50% |
| Fiber optic users | 38%+ |

---

## Machine Learning

Models evaluated: **Logistic Regression** and **Random Forest**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Random Forest | 0.592 | 0.412 | 0.510 | 0.456 | 0.607 |

The final model (Random Forest) was selected based on the business objective of identifying customers with elevated churn risk (Recall + ROC-AUC prioritized over raw Accuracy).

### Why Random Forest?
- **Recall: 51.0%** — catches 51% of actual churners (minimizes missed retention opportunities)
- **ROC-AUC: 60.7%** — better discrimination between churners and non-churners
- **Class-weighted** — handles imbalanced churn classes

---

## Customer Risk

Each customer receives a predicted churn probability, classified into:

- **High Risk** (≥70%): 420 customers (8.4%)
- **Medium Risk** (40–69%): 2,771 customers (55.4%)
- **Low Risk** (<40%): 1,809 customers (36.2%)

**Model-estimated revenue exposure:** $202,866

Retention priority combines predicted churn probability with monthly revenue exposure.

---

## Power BI Dashboard

### Page 1 — Churn Overview
Total customers, churned customers, churn rate, retention rate, revenue exposure, high-risk customers.

### Page 2 — Churn Drivers
Contract type, age group, tenure, support calls, monthly charges, internet service, payment method.

### Page 3 — Customer Risk
Customer churn probability, risk classification, revenue exposure, retention priority.

### Page 4 — Retention Strategy
Business recommendations based on customer risk and revenue exposure.

### Dashboard Preview

<!-- Add screenshots after Power BI Desktop build -->
<!-- ### Churn Overview
![Churn Overview](screenshots/overview.png)

### Churn Drivers
![Churn Drivers](screenshots/churn_drivers.png)

### Customer Risk
![Customer Risk](screenshots/customer_risk.png)

### Retention Strategy
![Retention Strategy](screenshots/retention_strategy.png) -->

---

## Key Business Insights

- **Month-to-month customers** churn at 41.25% — nearly double the rate of long-term contracts.
- **Short-tenure customers** (0-6 months) churn at 48.65% — the critical retention window.
- **Frequent support interactions** (5+ calls) are associated with 40-50% churn rates.
- **High-value, high-risk customers** represent the greatest retention opportunity.
- **Retention resources** should be prioritized using both churn probability and financial exposure.

---

## Business Recommendations

1. **Target high-risk, high-value customers first** — personal retention calls, loyalty discounts, contract upgrade offers.
2. **Introduce incentives for longer-term contracts** — month-to-month customers churn at 2x the rate.
3. **Proactively address repeated support issues** — 5+ calls is a critical churn signal.
4. **Monitor new customers during first 12 months** — early lifecycle has highest churn.
5. **Use predictive risk scores to personalize campaigns** — probability × value prioritization ensures maximum ROI.

---

## Project Structure

```
customer-churn-retention-analytics/
├── data/
│   ├── raw/customer_churn.csv
│   └── processed/
│       ├── customer_churn_clean.csv
│       └── customer_churn_ml_predictions.csv
├── notebooks/
│   ├── 01_customer_churn_eda.ipynb
│   └── 02_churn_ml.ipynb
├── python/
│   ├── generate_dataset.py
│   ├── data_cleaning.py
│   ├── database.py
│   ├── train_model.py
│   └── predict_churn.py
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_business_analysis.sql
│   └── 03_customer_risk.sql
├── ml/
│   ├── churn_model.pkl
│   └── model_metrics.json
├── powerbi/
│   ├── dax_calculated_columns.md
│   ├── dax_measures.md
│   └── build_guide.md
├── reports/
│   └── business_insights.md
├── screenshots/
├── docs/
├── app.py
├── requirements.txt
├── .gitignore
├── .env
├── AGENTS.md
└── README.md
```

---

## How to Run

### Environment Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Generate Dataset
```bash
python python/generate_dataset.py
```

### Run EDA
```bash
jupyter notebook notebooks/01_customer_churn_eda.ipynb
```

### Train Model
```bash
python python/train_model.py
```

### Generate Predictions
```bash
python python/predict_churn.py
```

### Run Streamlit Dashboard
```bash
streamlit run app.py
```

---

## Resume Bullet

> **Customer Churn Prediction & Retention Analytics** — Python | PostgreSQL | SQL | Scikit-learn | Power BI | Pandas
> - Developed an end-to-end customer churn analytics solution using Python, PostgreSQL, Machine Learning, and Power BI to identify churn drivers and support data-driven retention decisions.
> - Performed data cleaning, exploratory analysis, statistical analysis, and SQL-based customer segmentation across contract type, tenure, support interactions, and billing behavior.
> - Built and evaluated Logistic Regression and Random Forest churn models using Precision, Recall, F1-score, and ROC-AUC, generating customer-level churn probabilities and risk classifications.
> - Quantified revenue exposure by combining predicted churn probability with monthly customer charges and prioritized high-risk, high-value customers for retention campaigns.
> - Designed a 4-page Power BI dashboard covering churn overview, churn drivers, customer risk, revenue exposure, and actionable retention strategies.

---

## Disclaimer

This project uses synthetic data for educational and portfolio purposes.
