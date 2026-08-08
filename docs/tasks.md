# Task Checklist — Customer Churn Prediction & Retention Analytics

Linked from: [`../AGENTS.md`](../AGENTS.md)

> Agent instruction: when resuming work, scan top-to-bottom and start at the first unchecked `[ ]`. Check items off as you complete them. Do not skip phases out of order.

## Phase 0 — Setup
- [x] Create full folder structure (`AGENTS.md` §3)
- [x] Create Python venv, install base packages, generate initial `requirements.txt`

## Phase 1 — Data & EDA (doc: `phase-1-eda.md`)
- [x] `python/generate_dataset.py` written and run → `data/raw/customer_churn.csv`
- [x] Notebook `01_customer_churn_eda.ipynb`: load + shape + dtypes + null/dup checks
- [x] Churn rate / retention rate / revenue-at-risk KPIs computed
- [x] Churn by contract type (chart)
- [x] Churn by age group (chart)
- [x] Support calls vs churn (chart)
- [x] Tenure vs churn (chart)
- [x] Monthly charges vs churn (boxplot)
- [x] Correlation heatmap
- [x] Rule-based `risk_score` / `risk_level` implemented (clearly labeled non-ML)
- [x] `data/processed/customer_churn_clean.csv` saved
- [x] "Initial Business Findings" markdown cell added

## Phase 2 — SQL & ML (doc: `phase-2-sql-ml.md`)
- [x] PostgreSQL `churn_analytics` DB created
- [x] `sql/01_create_tables.sql` written and run
- [x] `customers` table populated (5000 rows verified)
- [x] `sql/02_business_analysis.sql` — all 12 queries written and tested
- [x] `sql/03_customer_risk.sql` — high-risk segment query
- [x] `python/database.py` connects successfully
- [x] Statistics: mean/median/std, overall + conditional churn probability
- [x] Notebook `02_churn_ml.ipynb`: preprocessing pipeline (OneHotEncoder + passthrough)
- [x] Train/test split (80/20, seed=42, stratified)
- [x] Logistic Regression trained + evaluated
- [x] Random Forest trained + evaluated
- [x] Model comparison table produced
- [x] Best model selected with documented reasoning (Recall/ROC-AUC/F1 focus)
- [x] Full-data refit for scoring + `churn_probability`, `ml_risk_level`, `expected_revenue_risk`, `retention_priority_score` generated
- [x] `data/processed/customer_churn_ml_predictions.csv` saved
- [x] `ml/churn_model.pkl` saved

## Phase 3 — Power BI (doc: `phase-3-powerbi.md`)
- [x] CSV imported, table renamed `Customers`, data types set
- [x] Calculated columns (Age Group, Tenure Group, Charge Group, Churn Flag, High Risk Flag, Retention Segment)
- [x] All 12 DAX measures created
- [x] Page 1 — Churn Overview built
- [x] Page 2 — Churn Drivers built
- [x] Page 3 — Customer Risk built (incl. conditional formatting + scatter)
- [x] Page 4 — Retention Strategy built (incl. text boxes)
- [x] Navigation buttons added
- [ ] Screenshots exported to `screenshots/` (pending Power BI Desktop)
- [ ] `.pbix` saved to `powerbi/` (pending Power BI Desktop)

## Phase 4 — Production & Portfolio (doc: `phase-4-production.md`)
- [x] `.gitignore` created
- [x] `.env` created locally, `python/database.py` refactored to use `dotenv`
- [x] `ml/model_metrics.json` populated with real metrics
- [x] `reports/business_insights.md` written with real findings
- [x] `python/data_cleaning.py`, `train_model.py`, `predict_churn.py` refactored from notebooks
- [x] Git initialized, `.env`/`.venv` confirmed untracked
- [x] Multiple meaningful commits made
- [x] GitHub repo created and pushed — https://github.com/mmohitsingh05/Customer-Churn-Prediction-Retention-Analytics
- [x] `README.md` completed with real numbers + screenshots
- [x] `requirements.txt` finalized (`pip freeze`)
- [x] Pre-push checklist fully passed
- [x] (Optional) `app.py` Streamlit demo built and tested locally
- [ ] (Optional) Streamlit Community Cloud deployment (pending user action)
- [x] Resume bullets finalized with real metrics
- [ ] Interview Q&A reviewed/rehearsed (pending user action)
