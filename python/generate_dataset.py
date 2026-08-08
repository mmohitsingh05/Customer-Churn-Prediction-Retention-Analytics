import numpy as np
import pandas as pd
import os

np.random.seed(42)

N = 5000

customer_ids = [f"CUST-{str(i).zfill(5)}" for i in range(1, N + 1)]
age = np.random.randint(18, 76, N)
gender = np.random.choice(["Male", "Female"], N)
tenure = np.random.randint(1, 73, N)
monthly_charges = np.round(np.random.uniform(20, 150, N), 2)
contract_type = np.random.choice(
    ["Month-to-month", "One year", "Two year"], N, p=[0.55, 0.25, 0.20]
)
support_calls = np.random.poisson(2.5, N)
internet_service = np.random.choice(
    ["DSL", "Fiber optic", "No"], N, p=[0.30, 0.55, 0.15]
)
payment_method = np.random.choice(
    ["Credit card", "Bank transfer", "Electronic check", "Mailed check"], N
)
total_charges = np.round(monthly_charges * tenure, 2)

churn_prob = (
    0.08
    + support_calls * 0.035
    + np.where(contract_type == "Month-to-month", 0.18, 0)
    + np.where(tenure < 12, 0.15, 0)
    + np.where(monthly_charges > 100, 0.08, 0)
    + np.where(age > 60, 0.04, 0)
)
churn_prob = np.clip(churn_prob, 0.02, 0.90)

churn = np.where(np.random.random(N) < churn_prob, "Yes", "No")

df = pd.DataFrame({
    "customer_id": customer_ids,
    "age": age,
    "gender": gender,
    "tenure": tenure,
    "monthly_charges": monthly_charges,
    "contract_type": contract_type,
    "support_calls": support_calls,
    "internet_service": internet_service,
    "payment_method": payment_method,
    "total_charges": total_charges,
    "churn": churn,
})

output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "customer_churn.csv")
df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Saved to: {output_path}")
print(f"\nChurn distribution:\n{df['churn'].value_counts()}")
print(f"\nChurn rate: {(df['churn'] == 'Yes').mean() * 100:.2f}%")
