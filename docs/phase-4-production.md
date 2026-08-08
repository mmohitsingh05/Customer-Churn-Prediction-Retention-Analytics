# Phase 4 — Production, Security, GitHub & Portfolio Packaging

Linked from: [`../AGENTS.md`](../AGENTS.md)
Prerequisite: Phases 1–3 complete

## Goal

Turn the working project into a secure, documented, portfolio-ready GitHub repository with resume/interview material.

## 1. Finalize Folder Structure

Confirm the structure matches `AGENTS.md` §3, plus these Phase-4 additions:
- `python/data_cleaning.py`, `python/train_model.py`, `python/predict_churn.py` (refactor notebook logic into reusable scripts)
- `ml/model_metrics.json`
- `reports/business_insights.md`
- `screenshots/*.png` (from Phase 3)
- `app.py` (optional Streamlit demo)

## 2. Security

1. Create `.gitignore` (see [`../.gitignore`](../.gitignore) template in this pack) — must exclude `.venv/`, `.env`, `__pycache__/`, `.ipynb_checkpoints/`, `*.pem`, `*.key`, OS/IDE junk.
2. `pip install python-dotenv`
3. Create local-only `.env`:
   ```env
   DB_USER=postgres
   DB_PASSWORD=YOUR_PASSWORD
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=churn_analytics
   ```
4. Rewrite `python/database.py` to load credentials via `os.getenv()` + `load_dotenv()` — no hardcoded secrets.

## 3. ML Model Metrics File

`ml/model_metrics.json` — populate with the **real** numbers from Phase 2 step 6/8:

```json
{
    "model": "Random Forest",
    "accuracy": 0.0,
    "precision": 0.0,
    "recall": 0.0,
    "f1_score": 0.0,
    "roc_auc": 0.0
}
```

Never copy example numbers from this spec pack into the repo — always the actual run's output.

## 4. `reports/business_insights.md`

Structure: Executive Summary → Key Findings (Contract Risk, Support Interaction, Tenure, Revenue Exposure, Customer Risk) → Recommendations (5 numbered items). Use the template embedded in this repo's `reports/business_insights.md` (create if missing) and fill in with real, current numbers once available — do not leave placeholder metrics in the committed version.

## 5. Git & GitHub

```bash
git init
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
git add .
git status   # confirm .env and .venv/ are NOT staged
git commit -m "Initial customer churn analytics project"
```

Then create GitHub repo `customer-churn-retention-analytics` (public, portfolio project), and:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git branch -M main
git push -u origin main
```

### Commit history should tell a story — use separate commits, e.g.:
1. "Add customer churn dataset and EDA"
2. "Add PostgreSQL analysis queries"
3. "Add churn prediction models"
4. "Add Power BI dashboard"
5. "Add project documentation and business insights"

## 6. README.md

Use [`../README.md`](../README.md) template in this pack as the base. Must include: Overview, Business Problem, Objectives, Tech Stack, Architecture diagram (ASCII is fine), Dataset description, Data Analysis summary, ML section (models + metrics — real numbers), Customer Risk section, Power BI dashboard section (all 4 pages) with embedded screenshots, Key Business Insights, Business Recommendations, Project Structure, Disclaimer (synthetic data, educational/portfolio purpose).

## 7. Optional Live Demo — Streamlit

`app.py`: loads `ml/churn_model.pkl`, exposes number inputs (age, tenure, monthly_charges, support_calls) and selectboxes (contract_type, gender, internet_service, payment_method), predicts on button click via `model.predict_proba(input_data)[0][1]`, displays as a percentage metric.

```bash
pip install streamlit
streamlit run app.py
```

Deployment option (₹0): Streamlit Community Cloud, connected to the GitHub repo. Never upload `.env` or DB credentials to a public deployment — this app is self-contained (loads a local `.pkl`, no DB dependency), which makes it safe to deploy as-is.

**Reality check:** Power BI Desktop dashboards cannot be hosted on free web hosting directly — the portfolio strategy is GitHub + `.pbix` file + dashboard screenshots + README, not a live Power BI Service link (that requires licensing/account setup out of scope for ₹0).

## 8. `requirements.txt`

```
pandas
numpy
matplotlib
seaborn
scikit-learn
jupyter
openpyxl
psycopg2-binary
sqlalchemy
python-dotenv
joblib
streamlit
```

Regenerate exact pinned versions with `pip freeze > requirements.txt` before final commit.

## 9. Pre-Push Checklist

**Python:** dataset loads · no missing values · no duplicate IDs · EDA runs · charts generate · model trains · metrics generate · predictions generate

**PostgreSQL:** DB exists · `customers` table exists · data imported · churn/revenue/risk queries all work

**ML:** train/test split · both models trained · Precision/Recall/F1/ROC-AUC/Confusion Matrix produced · churn probability + risk categories generated

**Power BI:** all 4 pages · DAX measures · slicers · navigation · conditional formatting · risk table

**GitHub:** README · `.gitignore` · `requirements.txt` · source code · SQL · ML model · `.pbix` · screenshots · business insights · **no passwords/keys/`.env` committed**

## 10. Resume & Interview Material

### Resume bullet template (fill in real metrics before using)

> **Customer Churn Prediction & Retention Analytics** — Python | PostgreSQL | SQL | Scikit-learn | Power BI | Pandas
> - Developed an end-to-end customer churn analytics solution using Python, PostgreSQL, Machine Learning, and Power BI to identify churn drivers and support data-driven retention decisions.
> - Performed data cleaning, exploratory analysis, statistical analysis, and SQL-based customer segmentation across contract type, tenure, support interactions, and billing behavior.
> - Built and evaluated Logistic Regression and Random Forest churn models using Precision, Recall, F1-score, and ROC-AUC, generating customer-level churn probabilities and risk classifications.
> - Quantified revenue exposure by combining predicted churn probability with monthly customer charges and prioritized high-risk, high-value customers for retention campaigns.
> - Designed a 4-page Power BI dashboard covering churn overview, churn drivers, customer risk, revenue exposure, and actionable retention strategies.

### Interview Q&A cheat-sheet

- **"Tell me about your churn project"** → business problem → Python/SQL analysis → LR vs RF comparison → churn probability → risk tiers → revenue exposure → 4-page Power BI dashboard → emphasize: *prediction converted into an actionable retention strategy, not just a model.*
- **"Why Random Forest?"** → compared LR (interpretable baseline) vs RF (captures non-linear interactions) using Precision/Recall/F1/ROC-AUC; leaned on Recall given the business cost of missed churners, without ignoring the other metrics.
- **"Why Recall specifically?"** → false negatives = missed retention opportunities; balanced against Precision so the retention team isn't flooded with false alerts.
- **"Correlation = causation?"** → No — e.g., support calls correlating with churn shows association, not proof of cause; would investigate underlying customer experience before acting on it.
- **"What's next?"** → validate on real historical data, add model explainability (e.g., feature importance/SHAP), run controlled retention experiments and measure actual impact on churn/LTV.

## Definition of Done for Phase 4

- [ ] `.gitignore` created before first commit; `.env` never staged
- [ ] `python/database.py` uses `dotenv`, no hardcoded secrets
- [ ] `ml/model_metrics.json` has real metrics
- [ ] `reports/business_insights.md` complete with real findings
- [ ] Git repo initialized, multiple meaningful commits, pushed to GitHub
- [ ] `README.md` complete, real numbers, screenshots embedded
- [ ] `requirements.txt` finalized via `pip freeze`
- [ ] Pre-push checklist (§9) fully passed
- [ ] Resume bullets + interview answers filled in with real metrics
- [ ] `docs/tasks.md` Phase 4 checkboxes updated
