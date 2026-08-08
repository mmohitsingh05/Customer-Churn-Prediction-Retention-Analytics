# Phase 3 — Power BI Dashboard

Linked from: [`../AGENTS.md`](../AGENTS.md) · Schema reference: [`data-model.md`](data-model.md)
Prerequisite: Phase 2 complete (`data/processed/customer_churn_ml_predictions.csv` exists)

> Note for AI agents: Power BI Desktop is a GUI Windows/Mac application and `.pbix` is a binary format — an agent generally cannot author it directly via code. This doc is the **spec Mohit (the human) follows inside Power BI Desktop**, and the agent's job is to (a) make sure the source CSV is 100% ready and correctly typed, (b) produce all DAX code as ready-to-paste snippets, and (c) keep this doc in sync as the single source of truth for what the dashboard must contain.

## Goal

`powerbi/Customer_Churn_Retention_Analytics.pbix` with 4 pages, fed by `customer_churn_ml_predictions.csv`, matching the spec below.

## 1. Import & Setup

- Get Data → Text/CSV → `data/processed/customer_churn_ml_predictions.csv`
- Rename table to `Customers`
- Set data types per [`data-model.md`](data-model.md): whole numbers, decimals, text as documented
- Format `churn_probability` as Percentage; `monthly_charges` and `expected_revenue_risk` as Currency

## 2. Calculated Columns (DAX)

```DAX
Age Group =
SWITCH(TRUE(),
    Customers[age] <= 25, "18-25",
    Customers[age] <= 35, "26-35",
    Customers[age] <= 45, "36-45",
    Customers[age] <= 55, "46-55",
    Customers[age] <= 65, "56-65",
    "66+")

Tenure Group =
SWITCH(TRUE(),
    Customers[tenure] <= 6, "0-6 Months",
    Customers[tenure] <= 12, "7-12 Months",
    Customers[tenure] <= 24, "13-24 Months",
    Customers[tenure] <= 48, "25-48 Months",
    "49-72 Months")

Charge Group =
SWITCH(TRUE(),
    Customers[monthly_charges] < 50, "Under 50",
    Customers[monthly_charges] < 100, "50-99",
    Customers[monthly_charges] < 125, "100-124",
    "125+")

Churn Flag = IF(Customers[churn] = "Yes", 1, 0)
High Risk Flag = IF(Customers[ml_risk_level] = "High", 1, 0)

Retention Segment =
SWITCH(TRUE(),
    Customers[ml_risk_level] = "High" && Customers[monthly_charges] >= 100, "High Risk - High Value",
    Customers[ml_risk_level] = "High", "High Risk - Standard Value",
    Customers[ml_risk_level] = "Medium", "Medium Risk",
    "Low Risk")
```

## 3. DAX Measures

```DAX
Total Customers = COUNTROWS(Customers)
Churned Customers = CALCULATE([Total Customers], Customers[churn] = "Yes")
Retained Customers = CALCULATE([Total Customers], Customers[churn] = "No")
Churn Rate = DIVIDE([Churned Customers], [Total Customers], 0)
Retention Rate = DIVIDE([Retained Customers], [Total Customers], 0)
Monthly Revenue = SUM(Customers[monthly_charges])
Churned Monthly Revenue = CALCULATE([Monthly Revenue], Customers[churn] = "Yes")
High Risk Customers = CALCULATE([Total Customers], Customers[ml_risk_level] = "High")
High Risk Revenue = CALCULATE([Monthly Revenue], Customers[ml_risk_level] = "High")
Expected Revenue Risk = SUM(Customers[expected_revenue_risk])
Average Churn Probability = AVERAGE(Customers[churn_probability])
Average Monthly Charges = AVERAGE(Customers[monthly_charges])
```

Format `Churn Rate`, `Retention Rate`, `Average Churn Probability` as Percentage. Format revenue measures as Currency.

## 4. Page 1 — Churn Overview

**5-second takeaway: "How bad is churn?"**

- Title: "Customer Churn & Retention Analytics" / Subtitle: "Customer behavior, churn drivers, revenue exposure & retention opportunities"
- 6 KPI cards: Total Customers, Churned Customers, Churn Rate, Retention Rate, Revenue at Risk (`Expected Revenue Risk`), High Risk Customers
- Clustered column: `contract_type` vs `Churn Rate`
- Column: `Age Group` vs `Churn Rate` (sorted 18-25 → 66+)
- Line: `Tenure Group` vs `Churn Rate`
- Donut: legend `ml_risk_level`, values `monthly_charges` (revenue exposure by risk)

## 5. Page 2 — Churn Drivers

**5-second takeaway: "Why is churn happening?"**

- Contract type vs Churn Rate (larger version)
- Line: `support_calls` vs Churn Rate
- `Tenure Group` vs Churn Rate
- `Charge Group` vs Churn Rate
- Bar: `internet_service` vs Churn Rate
- Bar: `payment_method` vs Churn Rate
- Slicers: Contract Type, Gender, Internet Service, Payment Method, Age Group, Tenure Group

## 6. Page 3 — Customer Risk

**5-second takeaway: "Who is at risk?"**

- KPI cards: High Risk Customers, Average Churn Probability, High Risk Revenue, Expected Revenue Risk
- Donut: `ml_risk_level` distribution (customer count)
- Binned histogram-style chart: `churn_probability_pct` in 10% bins
- Table: `customer_id, age, tenure, contract_type, support_calls, monthly_charges, churn_probability_pct, ml_risk_level, expected_revenue_risk`, sorted by `expected_revenue_risk` desc, with conditional formatting on `ml_risk_level` (High=red family, Medium=amber, Low=green)
- Slicer: `ml_risk_level`
- Scatter: X=`monthly_charges`, Y=`churn_probability`, legend=`ml_risk_level`, size=`expected_revenue_risk`

## 7. Page 4 — Retention Strategy

**5-second takeaway: "What should we do?"**

- Chart: `Retention Segment` (High Risk-High Value / High Risk-Standard Value / Medium Risk / Low Risk) vs Total Customers
- Text box "Recommended Retention Actions" — the 6-point list from `reports/business_insights.md`
- Text box "Key Management Insight" — executive summary paragraph
- Segment strategy reference (not necessarily on-canvas, but should inform the text box copy):
  - High Risk–High Value: ★★★★★ — personal retention call, loyalty discount, contract upgrade offer, dedicated support
  - Medium Risk: ★★★ — automated campaign, satisfaction survey, targeted email, contract incentive
  - Low Risk: ★ — normal engagement, loyalty program, upsell/cross-sell

## 8. Navigation & Polish

- Page navigator buttons (Overview / Drivers / Customer Risk / Retention Strategy)
- Optional bookmark-based "Reset Filters" button
- Canvas size 16:9 on all pages
- Color discipline: neutral background + one primary brand color + risk colors (red/amber/green family) only — no rainbow charts

## Definition of Done for Phase 3

- [ ] All 4 pages built matching sections 4–7
- [ ] All DAX measures/columns from sections 2–3 created and correctly formatted
- [ ] Navigation buttons work across all 4 pages
- [ ] Conditional formatting applied to the risk table on Page 3
- [ ] Screenshots exported to `screenshots/overview.png`, `churn_drivers.png`, `customer_risk.png`, `retention_strategy.png` (for README + Phase 4)
- [ ] `.pbix` saved to `powerbi/Customer_Churn_Retention_Analytics.pbix`
- [ ] `docs/tasks.md` Phase 3 checkboxes updated
