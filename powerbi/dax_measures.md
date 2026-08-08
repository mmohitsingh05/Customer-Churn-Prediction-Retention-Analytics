# DAX Measures — Power BI

> Copy-paste these into Power BI Desktop: Modeling → New Measure

## 1. Total Customers

```dax
Total Customers = COUNTROWS(Customers)
```

## 2. Churned Customers

```dax
Churned Customers = CALCULATE([Total Customers], Customers[churn] = "Yes")
```

## 3. Retained Customers

```dax
Retained Customers = CALCULATE([Total Customers], Customers[churn] = "No")
```

## 4. Churn Rate

```dax
Churn Rate = DIVIDE([Churned Customers], [Total Customers], 0)
```
> Format as **Percentage**

## 5. Retention Rate

```dax
Retention Rate = DIVIDE([Retained Customers], [Total Customers], 0)
```
> Format as **Percentage**

## 6. Monthly Revenue

```dax
Monthly Revenue = SUM(Customers[monthly_charges])
```
> Format as **Currency**

## 7. Churned Monthly Revenue

```dax
Churned Monthly Revenue = CALCULATE([Monthly Revenue], Customers[churn] = "Yes")
```
> Format as **Currency**

## 8. High Risk Customers

```dax
High Risk Customers = CALCULATE([Total Customers], Customers[ml_risk_level] = "High")
```

## 9. High Risk Revenue

```dax
High Risk Revenue = CALCULATE([Monthly Revenue], Customers[ml_risk_level] = "High")
```
> Format as **Currency**

## 10. Expected Revenue Risk

```dax
Expected Revenue Risk = SUM(Customers[expected_revenue_risk])
```
> Format as **Currency**

## 11. Average Churn Probability

```dax
Average Churn Probability = AVERAGE(Customers[churn_probability])
```
> Format as **Percentage**

## 12. Average Monthly Charges

```dax
Average Monthly Charges = AVERAGE(Customers[monthly_charges])
```
> Format as **Currency**
