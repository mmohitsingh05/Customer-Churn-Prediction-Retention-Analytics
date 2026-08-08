# DAX Calculated Columns — Power BI

> Copy-paste these into Power BI Desktop: Modeling → New Column

## 1. Age Group

```dax
Age Group =
SWITCH(TRUE(),
    Customers[age] <= 25, "18-25",
    Customers[age] <= 35, "26-35",
    Customers[age] <= 45, "36-45",
    Customers[age] <= 55, "46-55",
    Customers[age] <= 65, "56-65",
    "66+")
```

## 2. Tenure Group

```dax
Tenure Group =
SWITCH(TRUE(),
    Customers[tenure] <= 6, "0-6 Months",
    Customers[tenure] <= 12, "7-12 Months",
    Customers[tenure] <= 24, "13-24 Months",
    Customers[tenure] <= 48, "25-48 Months",
    "49-72 Months")
```

## 3. Charge Group

```dax
Charge Group =
SWITCH(TRUE(),
    Customers[monthly_charges] < 50, "Under 50",
    Customers[monthly_charges] < 100, "50-99",
    Customers[monthly_charges] < 125, "100-124",
    "125+")
```

## 4. Churn Flag

```dax
Churn Flag = IF(Customers[churn] = "Yes", 1, 0)
```

## 5. High Risk Flag

```dax
High Risk Flag = IF(Customers[ml_risk_level] = "High", 1, 0)
```

## 6. Retention Segment

```dax
Retention Segment =
SWITCH(TRUE(),
    Customers[ml_risk_level] = "High" && Customers[monthly_charges] >= 100, "High Risk - High Value",
    Customers[ml_risk_level] = "High", "High Risk - Standard Value",
    Customers[ml_risk_level] = "Medium", "Medium Risk",
    "Low Risk")
```
