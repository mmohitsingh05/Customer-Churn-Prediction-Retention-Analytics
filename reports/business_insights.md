# Business Insights — Customer Churn Prediction & Retention Analytics

> Generated from analysis of 5,000 synthetic telecom customers
> Model: Random Forest (Recall: 51.0%, ROC-AUC: 60.7%)

---

## Executive Summary

Customer churn is a significant business concern, with **33.46%** of customers churning and **$147,335/month** in revenue at risk. Our ML model identifies **420 high-risk customers** representing **$202,866 in model-estimated revenue exposure**. Month-to-month contracts, high support calls, and short tenure are the strongest churn predictors.

---

## Key Findings

### 1. Contract Risk
- **Month-to-month customers** churn at **41.25%**, nearly double the rate of One year (24.74%) and Two year (22.34%) contracts.
- Month-to-month customers represent **55.7%** of all customers but **68.6%** of churned customers.
- **Action:** Incentivize longer-term contracts with discounts; prioritize month-to-month customers for retention outreach.

### 2. Support Interaction Risk
- Customers with **5+ support calls** show churn rates of **40-50%**, compared to **22%** for zero-call customers.
- There is a clear positive correlation between support call frequency and churn probability.
- **Action:** Proactively address repeated support issues; implement root-cause analysis for customers with 3+ calls.

### 3. Tenure Risk
- **0-6 month tenure** customers churn at **48.65%** — the highest rate of any segment.
- Churn rates decline significantly after 12 months, stabilizing around 30% for long-tenured customers.
- **Action:** Implement onboarding campaigns for new customers; monitor first 12 months closely.

### 4. Revenue Exposure
- Total monthly revenue at risk from churned customers: **$147,335**.
- ML-estimated revenue exposure across all customers: **$202,866**.
- High-risk customers represent **$47,124/month** in revenue.
- **Action:** Prioritize retention spending on high-value, high-risk customers.

### 5. Customer Risk Segmentation
- **High Risk:** 420 customers (8.4%) — highest churn probability, urgent retention needed
- **Medium Risk:** 2,771 customers (55.4%) — moderate risk, automated campaigns effective
- **Low Risk:** 1,809 customers (36.2%) — stable, focus on loyalty and upsell

### 6. ML Model Performance
- Random Forest selected over Logistic Regression based on **Recall (51.0%)** and **ROC-AUC (60.7%)**.
- Model correctly identifies 51% of actual churners — prioritizing recall to minimize missed retention opportunities.
- Feature importance confirms: **support_calls**, **contract_type**, **tenure**, **monthly_charges** are top predictors.

---

## Recommendations

1. **Target High Risk-High Value customers first** — Personal retention calls, loyalty discounts, contract upgrade offers, and dedicated support for the 210 customers in this segment.

2. **Introduce longer-term contract incentives** — Offer 10-15% discounts for annual contracts; month-to-month customers churn at 2x the rate.

3. **Proactively address repeated support issues** — Customers with 5+ calls show 40-50% churn rates; implement escalation protocols and root-cause analysis.

4. **Monitor new customers during first 12 months** — The 0-12 month window has the highest churn; deploy onboarding emails, check-in calls, and early satisfaction surveys.

5. **Use ML risk scores to personalize campaigns** — Probability × value prioritization ensures maximum ROI on retention spend; don't rely on probability alone.

6. **Implement early warning system** — Use the trained model to score new customers weekly and trigger automated retention workflows for those crossing the 0.40 probability threshold.

---

## Data Sources

- **Dataset:** Synthetic telecom customer data (5,000 rows, 11 features)
- **SQL Analysis:** 12 business queries against PostgreSQL `churn_analytics` database
- **ML Model:** Random Forest (300 estimators, max_depth=10, class_weight=balanced)
- **Dashboard:** Power BI 4-page dashboard + Streamlit interactive preview

---

*This report uses synthetic data for educational and portfolio purposes.*
