# AGENTS.md — Customer Churn Prediction & Retention Analytics

> This file is the single entry point for any AI coding agent (Claude Code, Cursor, Copilot Workspace, etc.) working on this repository. Read this fully before writing any code. Linked docs in `docs/` contain the detailed spec for each phase — read the relevant doc before starting that phase's tasks.

## 0. Project Identity

- **Name:** Customer Churn Prediction & Retention Analytics
- **Owner:** Mohit
- **Positioning:** Senior-level, portfolio/job-ready Data Analyst project (Telecom / SaaS / Subscription business scenario)
- **Type:** End-to-end analytics + ML + BI solution, NOT a toy notebook project
- **Data:** Synthetic but realistic (generated via seeded script, 5,000 rows) — no copyright/privacy risk, freely usable
- **Final outputs required:** cleaned datasets, EDA, SQL analysis, ML churn-prediction model, Power BI dashboard, GitHub portfolio repo, resume/interview material

## 1. The Business Problem (never lose sight of this)

The company wants 4 questions answered:

1. **Who is churning?** (churn probability per customer)
2. **Why are they churning?** (churn drivers)
3. **How much revenue is at risk?** (revenue exposure)
4. **Who should be prioritized for retention?** (retention priority score)

Every technical task in this repo exists to answer one of these 4 questions. If a task doesn't serve one of them, question it before building it.

## 2. Tech Stack

| Layer | Tool |
|---|---|
| Data generation / cleaning / EDA | Python, Pandas, NumPy |
| Visualization (notebook) | Matplotlib, Seaborn |
| Analysis notebooks | Jupyter |
| Relational DB + business SQL | PostgreSQL |
| Python↔DB | SQLAlchemy, psycopg2-binary |
| ML | scikit-learn (Logistic Regression + Random Forest) |
| Model persistence | joblib |
| BI Dashboard | Power BI Desktop (.pbix) + DAX |
| Optional live demo | Streamlit |
| Secrets | python-dotenv (`.env`, never committed) |
| Version control | Git + GitHub |

**Cost constraint: ₹0.** Do not introduce paid services, paid hosting, or paid APIs anywhere in this project.

## 3. Repository Structure (target — create if missing)

```
Customer-Churn-Retention-Analytics/
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
│   └── Customer_Churn_Retention_Analytics.pbix
├── reports/
│   └── business_insights.md
├── screenshots/
│   ├── overview.png
│   ├── churn_drivers.png
│   ├── customer_risk.png
│   └── retention_strategy.png
├── app.py                  (optional Streamlit demo)
├── requirements.txt
├── .env                    (NEVER commit — local only)
├── .gitignore
├── README.md
└── AGENTS.md
```

## 4. Build Order (phases — do NOT skip ahead)

| Phase | Deliverable | Detail doc |
|---|---|---|
| 1 | Dataset generation + cleaning + Python EDA | [`docs/phase-1-eda.md`](docs/phase-1-eda.md) |
| 2 | PostgreSQL + SQL analysis + Statistics + ML (Logistic Regression & Random Forest) | [`docs/phase-2-sql-ml.md`](docs/phase-2-sql-ml.md) |
| 3 | Power BI 4-page dashboard (DAX, visuals, slicers) | [`docs/phase-3-powerbi.md`](docs/phase-3-powerbi.md) |
| 4 | Production hardening, Git/GitHub, README, portfolio packaging, optional Streamlit deploy | [`docs/phase-4-production.md`](docs/phase-4-production.md) |

Supporting references:
- Full data dictionary & schema → [`docs/data-model.md`](docs/data-model.md)
- Flat, checkable task list for agents → [`docs/tasks.md`](docs/tasks.md)

Each phase depends on the previous phase's output file(s) — do not regenerate earlier artifacts unless explicitly asked; extend them.

## 5. Non-Negotiable Rules

1. **Terminology discipline:**
   - The rule-based score built in Phase 1 (`risk_score` / `risk_level`) is a **"Rule-based Customer Risk Score"**, NOT a churn prediction model. Never call it ML.
   - The actual ML model (Phase 2, Logistic Regression / Random Forest) is the **"Machine Learning Churn Prediction Model"**.
   - `expected_revenue_risk` = model-estimated exposure, not "revenue lost." Never relabel it as guaranteed lost revenue.
2. **Never fabricate metrics.** Accuracy/Precision/Recall/F1/ROC-AUC in README, resume text, or reports must come from the actual `ml/model_metrics.json` output of a real run — never copy example numbers from the spec docs.
3. **Never commit secrets.** `.env`, DB passwords, API keys must never reach Git. `.gitignore` must be created before the first commit.
4. **Model selection is not accuracy-only.** For churn, prioritize Recall + ROC-AUC + F1 alongside Precision, because missing an actual churner (false negative) costs a real retention opportunity.
5. **Correlation ≠ Causation.** Any narrative text (reports, README, dashboard captions) describing feature relationships (e.g., support calls vs. churn) must be phrased as association, not causation.
6. **Reproducibility.** All random generation/splitting must use `random_state=42` / `np.random.seed(42)` consistently so results are reproducible across the whole pipeline.
7. **Business framing over raw stats.** Every chart/metric produced should be paired with a one-line business interpretation (see Section 35 pattern in phase-1 doc: Business Question → Analytical Question → Metric → Finding → Action).

## 6. Environment Setup (run once)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install pandas numpy matplotlib seaborn jupyter openpyxl scikit-learn \
            psycopg2-binary sqlalchemy python-dotenv joblib streamlit
pip freeze > requirements.txt
```

PostgreSQL: create database `churn_analytics` locally before running any `sql/*.sql` file.

## 7. Definition of Done (whole project)

- [ ] `data/processed/customer_churn_ml_predictions.csv` exists with all required columns (see data-model.md)
- [ ] Both notebooks run top-to-bottom without errors
- [ ] `sql/*.sql` files run cleanly against a populated `customers` table
- [ ] `ml/model_metrics.json` reflects real, current test-set metrics for the selected model
- [ ] `powerbi/Customer_Churn_Retention_Analytics.pbix` has all 4 pages described in phase-3 doc
- [ ] `README.md` follows the template in phase-4 doc, with real numbers (no placeholders)
- [ ] `.gitignore` excludes `.venv/`, `.env`, `__pycache__/`, `.ipynb_checkpoints/`, secrets
- [ ] Git history has multiple meaningful commits (not one giant commit)
- [ ] `reports/business_insights.md` exists with real findings
- [ ] No hardcoded passwords/keys anywhere in tracked files

## 8. Agent Working Style for This Repo

- Work phase by phase. Before starting a phase, open its doc in `docs/`.
- When a doc gives exact code (e.g., dataset generator script, DAX measures, SQL queries), use it as the authoritative implementation — don't silently redesign it unless asked.
- When asked to "continue the project," check `docs/tasks.md`, find the first unchecked box, and resume from there.
- Always update `docs/tasks.md` checkboxes after completing each task.
- If PostgreSQL or Power BI Desktop is not available in the current environment, still generate all SQL/DAX/config files correctly — they should be ready to run the moment those tools are available.
