# Power BI Desktop — Build Guide

> Step-by-step instructions to build the 4-page Customer Churn dashboard.
> Source CSV: `data/processed/customer_churn_ml_predictions.csv`

---

## Step 1: Import Data

1. Open **Power BI Desktop**
2. **Get Data** → **Text/CSV**
3. Navigate to `data/processed/customer_churn_ml_predictions.csv`
4. Click **Load** (not Transform — data is already clean)
5. In the **Fields** panel, rename the table from `customer_churn_ml_predictions` to **`Customers`**
   - Right-click the table name → Rename

### Set Data Types
- `customer_id`: Text
- `age`: Whole Number
- `gender`: Text
- `tenure`: Whole Number
- `monthly_charges`: Decimal Number → format as Currency ($)
- `contract_type`: Text
- `support_calls`: Whole Number
- `internet_service`: Text
- `payment_method`: Text
- `total_charges`: Decimal Number → format as Currency ($)
- `churn`: Text
- `churn_probability`: Decimal Number → format as Percentage (%)
- `churn_probability_pct`: Decimal Number
- `ml_risk_level`: Text
- `expected_revenue_risk`: Decimal Number → format as Currency ($)

---

## Step 2: Create Calculated Columns

Go to **Modeling** → **New Column** and paste each DAX formula.

See: `powerbi/dax_calculated_columns.md`

Create all 6 columns:
1. `Age Group`
2. `Tenure Group`
3. `Charge Group`
4. `Churn Flag`
5. `High Risk Flag`
6. `Retention Segment`

---

## Step 3: Create Measures

Go to **Modeling** → **New Measure** and paste each DAX formula.

See: `powerbi/dax_measures.md`

Create all 12 measures and format them:
- `Churn Rate`, `Retention Rate`, `Average Churn Probability` → **Percentage**
- Revenue measures → **Currency**

---

## Step 4: Build Page 1 — Churn Overview

**5-second takeaway: "How bad is churn?"**

1. Rename page tab to **"Churn Overview"**
2. Add title: "Customer Churn & Retention Analytics"
3. Add subtitle: "Customer behavior, churn drivers, revenue exposure & retention opportunities"

### KPI Cards (top row):
| Card | Measure |
|------|---------|
| Total Customers | `Total Customers` |
| Churned Customers | `Churned Customers` |
| Churn Rate | `Churn Rate` |
| Retention Rate | `Retention Rate` |
| Revenue at Risk | `Expected Revenue Risk` |
| High Risk Customers | `High Risk Customers` |

### Charts:
| Chart Type | Axis | Values |
|------------|------|--------|
| Clustered Column | `contract_type` | `Churn Rate` |
| Clustered Column | `Age Group` | `Churn Rate` |
| Line | `Tenure Group` | `Churn Rate` |
| Donut | `ml_risk_level` | `Monthly Revenue` |

---

## Step 5: Build Page 2 — Churn Drivers

**5-second takeaway: "Why is churn happening?"**

1. Add new page → rename to **"Churn Drivers"**

### Charts:
| Chart Type | Axis/Legend | Values |
|------------|-------------|--------|
| Clustered Column | `contract_type` | `Churn Rate` |
| Line | `support_calls` | `Churn Rate` |
| Column | `Tenure Group` | `Churn Rate` |
| Column | `Charge Group` | `Churn Rate` |
| Bar | `internet_service` | `Churn Rate` |
| Bar | `payment_method` | `Churn Rate` |

### Slicers (left side or top):
- `contract_type`
- `gender`
- `internet_service`
- `payment_method`
- `Age Group`
- `Tenure Group`

---

## Step 6: Build Page 3 — Customer Risk

**5-second takeaway: "Who is at risk?"**

1. Add new page → rename to **"Customer Risk"**

### KPI Cards (top row):
| Card | Measure |
|------|---------|
| High Risk Customers | `High Risk Customers` |
| Avg Churn Probability | `Average Churn Probability` |
| High Risk Revenue | `High Risk Revenue` |
| Expected Revenue Risk | `Expected Revenue Risk` |

### Charts:
| Chart Type | Details |
|------------|---------|
| Donut | Legend: `ml_risk_level`, Values: customer count |
| Histogram-style | `churn_probability_pct` binned in 10% increments |
| Scatter | X: `monthly_charges`, Y: `churn_probability`, Legend: `ml_risk_level`, Size: `expected_revenue_risk` |

### Table:
Columns: `customer_id`, `age`, `tenure`, `contract_type`, `support_calls`, `monthly_charges`, `churn_probability_pct`, `ml_risk_level`, `expected_revenue_risk`

Sort by: `expected_revenue_risk` descending

**Conditional Formatting:**
- Select `ml_risk_level` column → Format by rules:
  - "High" → Red background
  - "Medium" → Amber/Yellow background
  - "Low" → Green background

### Slicer:
- `ml_risk_level`

---

## Step 7: Build Page 4 — Retention Strategy

**5-second takeaway: "What should we do?"**

1. Add new page → rename to **"Retention Strategy"**

### Chart:
| Chart Type | Axis | Values |
|------------|------|--------|
| Clustered Column | `Retention Segment` | `Total Customers` |

### Text Box — "Recommended Retention Actions":
1. **Target High Risk-High Value customers first** — personal retention calls, loyalty discounts
2. **Introduce longer-term contract incentives** — Month-to-month customers churn 2x more
3. **Proactively address repeated support issues** — 5+ calls = critical churn signal
4. **Monitor new customers during first 12 months** — 0-6 month tenure has highest churn
5. **Use ML risk scores to personalize campaigns** — probability × value prioritization

### Text Box — "Key Management Insight":
> Our ML model identifies customers at risk of churning, combining predicted probability with revenue exposure. High Risk-High Value customers represent the greatest retention opportunity — proactive intervention here delivers maximum ROI. Month-to-month contracts and high support calls are the strongest churn indicators.

---

## Step 8: Navigation & Polish

### Navigation Buttons:
Insert → Buttons → Blank (or use Icon buttons)
- Button 1: "Overview" → Action: Page navigation → Churn Overview
- Button 2: "Drivers" → Action: Page navigation → Churn Drivers
- Button 3: "Risk" → Action: Page navigation → Customer Risk
- Button 4: "Strategy" → Action: Page navigation → Retention Strategy

Place at the top of each page.

### Color Discipline:
- Background: White/Light gray
- Primary brand: Blue (#3498db)
- Risk colors: Red (#e74c3c) = High, Amber (#f39c12) = Medium, Green (#27ae60) = Low
- No rainbow charts

### Canvas Size:
- All pages: 16:9 (default)

---

## Step 9: Export & Save

1. **Save** → `powerbi/Customer_Churn_Retention_Analytics.pbix`
2. **Export screenshots** for each page:
   - File → Export → Export to file → PNG
   - Save as:
     - `screenshots/overview.png`
     - `screenshots/churn_drivers.png`
     - `screenshots/customer_risk.png`
     - `screenshots/retention_strategy.png`

---

## Bin Boundaries Reference (must match Python)

| Bin | Python (Phase 1) | Power BI DAX |
|-----|------------------|--------------|
| Age 18-25 | `age <= 25` | `age <= 25` |
| Age 26-35 | `age <= 35` | `age <= 35` |
| Age 36-45 | `age <= 45` | `age <= 45` |
| Age 46-55 | `age <= 55` | `age <= 55` |
| Age 56-65 | `age <= 65` | `age <= 65` |
| Age 66+ | `> 65` | `> 65` |
| Tenure 0-6 | `tenure <= 6` | `tenure <= 6` |
| Tenure 7-12 | `tenure <= 12` | `tenure <= 12` |
| Tenure 13-24 | `tenure <= 24` | `tenure <= 24` |
| Tenure 25-48 | `tenure <= 48` | `tenure <= 48` |
| Tenure 49-72 | `> 48` | `> 48` |
