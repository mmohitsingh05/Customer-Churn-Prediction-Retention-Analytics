# Phase 1 — Data Generation, Cleaning & EDA

Linked from: [`../AGENTS.md`](../AGENTS.md) · Schema reference: [`data-model.md`](data-model.md)

## Goal

End of this phase: `data/raw/customer_churn.csv`, `data/processed/customer_churn_clean.csv`, a working `notebooks/01_customer_churn_eda.ipynb`, and a set of churn KPIs + initial business findings.

## 1. Folder Scaffold

Create the full directory tree from `AGENTS.md` §3 if it doesn't exist (empty `sql/`, `ml/`, `powerbi/`, `reports/`, `screenshots/` are fine at this stage).

## 2. Environment

```bash
python -m venv .venv
pip install pandas numpy matplotlib seaborn jupyter openpyxl scikit-learn
pip freeze > requirements.txt
```

## 3. `python/generate_dataset.py`

Implement exactly per [`data-model.md`](data-model.md) §1 (N=5000, seed=42, all 11 raw columns, churn probability formula). Script must:
- Print `Dataset created successfully!`, row count, column count, and save path on success
- Write to `data/raw/customer_churn.csv`
- Be re-runnable/idempotent (overwrites cleanly)

## 4. Notebook: `notebooks/01_customer_churn_eda.ipynb`

Build cells in this order (each is a checkpoint — verify output before moving to the next):

1. Imports: `pandas`, `numpy`, `matplotlib.pyplot`, `seaborn`
2. Load `../data/raw/customer_churn.csv`, `df.head()`
3. `df.shape` → expect `(5000, 11)`
4. `df.columns`, `df.info()`, `df.isnull().sum()` → expect all zero
5. `df["customer_id"].duplicated().sum()` and `df.duplicated().sum()` → expect 0 both
6. `df.describe()` and `df.describe(include="object")`
7. Churn distribution: `value_counts()`, `value_counts(normalize=True)*100`, and a clean `churn_rate` print
8. KPI block: total/churned/retained customers, churn rate, retention rate
9. Revenue at risk: `sum(monthly_charges)` where `churn == "Yes"`
10. Average monthly charges overall vs. by churn (`groupby("churn")`)
11. Churn by contract type — crosstab + `groupby` churn rate + bar chart (`sns.barplot`)
12. Churn by age group — create `age_group` bins per data-model.md, bar chart
13. Support calls vs churn — line chart (`sns.lineplot`)
14. Tenure vs churn — create `tenure_group` bins, analysis
15. Monthly charges vs churn — boxplot (`sns.boxplot`)
16. Support calls distribution by churn — histogram (`sns.histplot`, `multiple="dodge"`)
17. Correlation matrix on numeric columns + heatmap (`sns.heatmap`, `annot=True`, `cmap="coolwarm"`)
18. Add `churn_numeric` column, recompute correlation including it, sort by correlation to `churn_numeric`
19. Rule-based `risk_score` + `risk_level` (exact logic in data-model.md §2) — **label clearly as rule-based, not ML, in a markdown cell**
20. High-risk customer view (`risk_level == "High"`, sorted/selected columns)
21. Save `data/processed/customer_churn_clean.csv`
22. Final markdown cell: **Initial Business Findings** (6 bullet points — contract risk, support-call risk, tenure risk, revenue monitoring, risk scoring value, note that ML is needed next)

## 5. Business-Question Framing (apply to every analysis block)

```
Business Question → Analytical Question → Metric → Analysis → Visualization → Business Insight
```
Example: "Why are customers leaving?" → "What's the churn rate by contract type?" → Churn % → groupby/crosstab → bar chart → "Month-to-month customers churn more."

Every chart in the notebook should have a 1–2 line markdown interpretation directly below it, not just raw output.

## 6. Explicit Guardrails

- Do **not** build any ML model in this phase — that's Phase 2.
- Do **not** call `risk_score`/`risk_level` a "prediction" or "model" anywhere (code comments, markdown cells, print statements).
- `df.isnull().sum().sum()` and duplicate checks must genuinely pass — if the generator ever produces nulls/dupes, fix the generator, don't silently drop rows without noting it.

## 7. Definition of Done for Phase 1

- [ ] `python/generate_dataset.py` runs and produces `data/raw/customer_churn.csv` (5000 rows, 11 cols)
- [ ] `notebooks/01_customer_churn_eda.ipynb` runs top-to-bottom with no errors
- [ ] All 8+ visualizations listed above are present with markdown interpretations
- [ ] `data/processed/customer_churn_clean.csv` saved with all engineered columns from data-model.md §2
- [ ] Final "Initial Business Findings" markdown cell present
- [ ] `docs/tasks.md` Phase 1 checkboxes updated
