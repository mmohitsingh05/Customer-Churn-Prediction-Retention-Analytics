# Phase 2 — PostgreSQL, SQL Business Analysis, Statistics & Machine Learning

Linked from: [`../AGENTS.md`](../AGENTS.md) · Schema reference: [`data-model.md`](data-model.md)
Prerequisite: Phase 1 complete (`data/processed/customer_churn_clean.csv` exists)

## Goal

End of this phase: a populated PostgreSQL `customers` table, 15+ business SQL queries, statistical/probability analysis in Python, two trained & evaluated ML models, and `data/processed/customer_churn_ml_predictions.csv` + `ml/churn_model.pkl`.

## PART A — PostgreSQL

1. `CREATE DATABASE churn_analytics;`
2. `sql/01_create_tables.sql` → exact `customers` DDL from [`data-model.md`](data-model.md) §4
3. Load `data/processed/customer_churn_clean.csv` into `customers` via `COPY ... CSV HEADER` or pgAdmin Import/Export (raw-column subset only — engineered columns like `age_group` stay Python-side)
4. Verify: `SELECT COUNT(*) FROM customers;` → 5000; check `information_schema.columns`

## PART B — SQL Business Analysis (`sql/02_business_analysis.sql`)

Implement all of the following (exact patterns from project chat 2, §6–18):

1. Total customers
2. Churned customers count
3. Churn rate (%)
4. Retention rate (%)
5. Revenue lost due to churn (`SUM(monthly_charges) WHERE churn='Yes'`)
6. Average monthly charges
7. Churn by contract type (count + rate, `GROUP BY`, sorted desc)
8. Churn by gender (note: if difference is small, do not force a gender-based recommendation)
9. Churn by support_calls (`GROUP BY support_calls`)
10. Churn by tenure group (`CASE WHEN` bucket, matches Python `tenure_group` bins)
11. Top 20 high-value churned customers (`ORDER BY monthly_charges DESC`)
12. Revenue at risk by contract type

## PART C — High-Risk Segment Query (`sql/03_customer_risk.sql`)

Business-rule (not ML) high-risk segment:
```sql
SELECT customer_id, age, tenure, monthly_charges, contract_type, support_calls, churn
FROM customers
WHERE contract_type = 'Month-to-month' AND support_calls >= 5 AND tenure <= 12
ORDER BY monthly_charges DESC;
```
Label this clearly as a "high-risk business segment," not a model output.

## PART D — Python ↔ PostgreSQL

`python/database.py` — SQLAlchemy engine using `psycopg2`. **In Phase 2 this may still use plain variables; Phase 4 replaces these with `.env`/`python-dotenv`.** Never leave a real password committed.

## PART E — Statistics (in `notebooks/02_churn_ml.ipynb`, before modeling)

1. Mean vs. median of `monthly_charges` (check for skew)
2. Standard deviation of `monthly_charges`
3. Overall churn probability = `df["churn"].eq("Yes").mean()`
4. Conditional probabilities: churn probability given `contract_type == "Month-to-month"`; churn probability given `support_calls >= 5`

## PART F — Machine Learning

Follow [`data-model.md`](data-model.md) §5 exactly for features/target/split.

1. `notebooks/02_churn_ml.ipynb`: load `customer_churn_clean.csv`, build `churn_target`
2. `ColumnTransformer` — OneHotEncoder on categoricals, passthrough on numerics
3. `train_test_split(test_size=0.20, random_state=42, stratify=y)`
4. **Model 1 — Logistic Regression** (`max_iter=1000`) inside a `Pipeline` with the preprocessor
5. **Model 2 — Random Forest** (`n_estimators=300, max_depth=10, random_state=42, class_weight="balanced"`) inside a `Pipeline`
6. Evaluate both on the test set: Accuracy, Precision, Recall, F1, ROC-AUC, `classification_report`, confusion matrix (`ConfusionMatrixDisplay`)
7. Build a `model_comparison` DataFrame side by side
8. **Model selection rule:** prioritize Recall + ROC-AUC + F1 over raw Accuracy (missing a real churner = missed retention opportunity / false negative cost). Document the actual selected model and *why* in a markdown cell, referencing the real numbers produced.
9. Refit the selected model (`best_model`) on the **full** dataset (X, y) purely to generate deployable per-customer scores — but always report evaluation metrics from the held-out **test set**, never from this full-data refit.
10. Generate `churn_probability`, `churn_probability_pct`
11. `ml_risk_level`: High ≥0.70, Medium 0.40–0.69, Low <0.40
12. `expected_revenue_risk = churn_probability * monthly_charges`
13. `retention_priority_score = churn_probability * monthly_charges` (same formula, used for sorting/prioritization — call out in markdown why probability × value beats probability alone, using the "Customer A vs Customer B" example)
14. Save final dataset: `data/processed/customer_churn_ml_predictions.csv` with exact columns from [`data-model.md`](data-model.md) §3
15. `pip install joblib`; `joblib.dump(best_model, "../ml/churn_model.pkl")`
16. Save real metrics to `ml/model_metrics.json` (schema in phase-4 doc §"ML Model Metrics") — **use the actual numbers from step 6, never placeholders**

## Guardrails

- Do not report "Model achieved X% accuracy" anywhere without it being the real, current test-set number.
- Do not conflate the Phase 1 rule-based `risk_level` with the Phase 2 ML `ml_risk_level` — they must coexist as separate concepts if both are referenced.
- `expected_revenue_risk` narrative must say "model-estimated exposure," not "confirmed lost revenue."

## Definition of Done for Phase 2

- [ ] `churn_analytics` DB exists with populated `customers` table (5000 rows)
- [ ] `sql/01_create_tables.sql`, `sql/02_business_analysis.sql`, `sql/03_customer_risk.sql` all present and runnable
- [ ] `python/database.py` connects successfully
- [ ] `notebooks/02_churn_ml.ipynb` runs top-to-bottom, both models trained & evaluated
- [ ] `data/processed/customer_churn_ml_predictions.csv` saved with correct schema
- [ ] `ml/churn_model.pkl` saved
- [ ] Real metrics captured (will be persisted to `ml/model_metrics.json` in Phase 4)
- [ ] `docs/tasks.md` Phase 2 checkboxes updated
