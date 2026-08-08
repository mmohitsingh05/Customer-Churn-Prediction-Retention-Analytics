import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/customer_churn_ml_predictions.csv")
    df["age_group"] = pd.cut(df["age"], bins=[0,25,35,45,55,65,100], labels=["18-25","26-35","36-45","46-55","56-65","66+"])
    df["tenure_group"] = pd.cut(df["tenure"], bins=[0,6,12,24,48,72], labels=["0-6 Months","7-12 Months","13-24 Months","25-48 Months","49-72 Months"])
    df["charge_group"] = pd.cut(df["monthly_charges"], bins=[0,50,100,125,200], labels=["Under 50","50-99","100-124","125+"])
    df["churn_flag"] = (df["churn"] == "Yes").astype(int)
    df["high_risk_flag"] = (df["ml_risk_level"] == "High").astype(int)
    df["retention_segment"] = np.where(
        (df["ml_risk_level"] == "High") & (df["monthly_charges"] >= 100), "High Risk - High Value",
        np.where(df["ml_risk_level"] == "High", "High Risk - Standard Value",
        np.where(df["ml_risk_level"] == "Medium", "Medium Risk", "Low Risk"))
    )
    return df

df = load_data()

total_customers = len(df)
churned = (df["churn"] == "Yes").sum()
retained = (df["churn"] == "No").sum()
churn_rate = churned / total_customers
retention_rate = retained / total_customers
monthly_revenue = df["monthly_charges"].sum()
churned_revenue = df.loc[df["churn"] == "Yes", "monthly_charges"].sum()
high_risk_count = (df["ml_risk_level"] == "High").sum()
high_risk_revenue = df.loc[df["ml_risk_level"] == "High", "monthly_charges"].sum()
expected_revenue_risk = df["expected_revenue_risk"].sum()
avg_churn_prob = df["churn_probability"].mean()

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Churn Overview", "Churn Drivers", "Customer Risk", "Retention Strategy"])

if page == "Churn Overview":
    st.title("Customer Churn & Retention Analytics")
    st.caption("Customer behavior, churn drivers, revenue exposure & retention opportunities")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Customers", f"{total_customers:,}")
    c2.metric("Churned", f"{churned:,}")
    c3.metric("Churn Rate", f"{churn_rate*100:.1f}%")
    c4.metric("Retention Rate", f"{retention_rate*100:.1f}%")
    c5.metric("Revenue at Risk", f"${expected_revenue_risk:,.0f}")
    c6.metric("High Risk", f"{high_risk_count:,}")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        contract_churn = df.groupby("contract_type")["churn_flag"].mean().sort_values(ascending=False) * 100
        fig = px.bar(x=contract_churn.index, y=contract_churn.values, title="Churn Rate by Contract Type",
                     labels={"x":"Contract Type","y":"Churn Rate (%)"}, color=contract_churn.index,
                     color_discrete_map={"Month-to-month":"#e74c3c","One year":"#f39c12","Two year":"#27ae60"})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        age_churn = df.groupby("age_group", observed=True)["churn_flag"].mean() * 100
        fig = px.bar(x=age_churn.index, y=age_churn.values, title="Churn Rate by Age Group",
                     labels={"x":"Age Group","y":"Churn Rate (%)"}, color_discrete_sequence=["#3498db"])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        tenure_churn = df.groupby("tenure_group", observed=True)["churn_flag"].mean() * 100
        fig = px.line(x=tenure_churn.index, y=tenure_churn.values, title="Churn Rate by Tenure Group",
                      labels={"x":"Tenure Group","y":"Churn Rate (%)"}, markers=True)
        fig.update_traces(line_color="#2ecc71", line_width=3)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        risk_counts = df["ml_risk_level"].value_counts()
        fig = px.pie(values=risk_counts.values, names=risk_counts.index, title="Revenue Exposure by Risk Level",
                     color=risk_counts.index, color_discrete_map={"High":"#e74c3c","Medium":"#f39c12","Low":"#27ae60"},
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

elif page == "Churn Drivers":
    st.title("Churn Drivers")
    st.caption("Why is churn happening?")

    col1, col2, col3 = st.columns(3)
    with col1:
        contract_type = st.selectbox("Contract Type", ["All"] + sorted(df["contract_type"].unique()))
    with col2:
        internet_svc = st.selectbox("Internet Service", ["All"] + sorted(df["internet_service"].unique()))
    with col3:
        payment = st.selectbox("Payment Method", ["All"] + sorted(df["payment_method"].unique()))

    filtered = df.copy()
    if contract_type != "All":
        filtered = filtered[filtered["contract_type"] == contract_type]
    if internet_svc != "All":
        filtered = filtered[filtered["internet_service"] == internet_svc]
    if payment != "All":
        filtered = filtered[filtered["payment_method"] == payment]

    st.caption(f"Showing {len(filtered):,} customers")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        contract_churn = filtered.groupby("contract_type")["churn_flag"].mean().sort_values(ascending=False) * 100
        fig = px.bar(x=contract_churn.index, y=contract_churn.values, title="Contract Type vs Churn Rate",
                     color=contract_churn.index, color_discrete_map={"Month-to-month":"#e74c3c","One year":"#f39c12","Two year":"#27ae60"})
        fig.update_layout(showlegend=False, xaxis_title="Contract Type", yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        support_churn = filtered.groupby("support_calls")["churn_flag"].mean() * 100
        fig = px.line(x=support_churn.index, y=support_churn.values, title="Support Calls vs Churn Rate",
                      markers=True, labels={"x":"Support Calls","y":"Churn Rate (%)"})
        fig.update_traces(line_color="#e74c3c", line_width=3)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        tenure_churn = filtered.groupby("tenure_group", observed=True)["churn_flag"].mean() * 100
        fig = px.bar(x=tenure_churn.index, y=tenure_churn.values, title="Tenure Group vs Churn Rate",
                     color_discrete_sequence=["#2ecc71"])
        fig.update_layout(xaxis_title="Tenure Group", yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        charge_churn = filtered.groupby("charge_group", observed=True)["churn_flag"].mean() * 100
        fig = px.bar(x=charge_churn.index, y=charge_churn.values, title="Charge Group vs Churn Rate",
                     color_discrete_sequence=["#9b59b6"])
        fig.update_layout(xaxis_title="Charge Group", yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        internet_churn = filtered.groupby("internet_service")["churn_flag"].mean().sort_values(ascending=True) * 100
        fig = px.bar(x=internet_churn.values, y=internet_churn.index, title="Internet Service vs Churn Rate",
                     orientation="h", color_discrete_sequence=["#3498db"])
        fig.update_layout(xaxis_title="Churn Rate (%)", yaxis_title="Internet Service")
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        payment_churn = filtered.groupby("payment_method")["churn_flag"].mean().sort_values(ascending=True) * 100
        fig = px.bar(x=payment_churn.values, y=payment_churn.index, title="Payment Method vs Churn Rate",
                     orientation="h", color_discrete_sequence=["#1abc9c"])
        fig.update_layout(xaxis_title="Churn Rate (%)", yaxis_title="Payment Method")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Customer Risk":
    st.title("Customer Risk")
    st.caption("Who is at risk?")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("High Risk Customers", f"{high_risk_count:,}")
    c2.metric("Avg Churn Probability", f"{avg_churn_prob*100:.1f}%")
    c3.metric("High Risk Revenue", f"${high_risk_revenue:,.0f}")
    c4.metric("Expected Revenue Risk", f"${expected_revenue_risk:,.0f}")

    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        risk_filter = st.selectbox("Filter by Risk Level", ["All", "High", "Medium", "Low"])
        filtered = df if risk_filter == "All" else df[df["ml_risk_level"] == risk_filter]

        risk_counts = filtered["ml_risk_level"].value_counts()
        fig = px.pie(values=risk_counts.values, names=risk_counts.index, title="Risk Level Distribution",
                     color=risk_counts.index, color_discrete_map={"High":"#e74c3c","Medium":"#f39c12","Low":"#27ae60"},
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df["prob_bin"] = pd.cut(df["churn_probability"], bins=np.arange(0, 1.1, 0.1))
        prob_dist = df.groupby("prob_bin", observed=True).size()
        fig = px.bar(x=prob_dist.index.astype(str), y=prob_dist.values, title="Churn Probability Distribution",
                     labels={"x":"Churn Probability","y":"Count"}, color_discrete_sequence=["#e74c3c"])
        fig.update_layout(xaxis_title="Churn Probability", yaxis_title="Number of Customers")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Risk Table")
    display_cols = ["customer_id","age","tenure","contract_type","support_calls","monthly_charges","churn_probability_pct","ml_risk_level","expected_revenue_risk"]
    table_df = filtered[display_cols].sort_values("expected_revenue_risk", ascending=False).head(100)

    def color_risk(val):
        if val == "High": return "background-color: #ffcccc"
        elif val == "Medium": return "background-color: #fff3cd"
        else: return "background-color: #d4edda"

    st.dataframe(table_df.style.applymap(color_risk, subset=["ml_risk_level"]).format({
        "monthly_charges": "${:.2f}", "churn_probability_pct": "{:.1f}%", "expected_revenue_risk": "${:.2f}"
    }), use_container_width=True, height=400)

    st.divider()
    fig = px.scatter(filtered, x="monthly_charges", y="churn_probability", color="ml_risk_level",
                     size="expected_revenue_risk", title="Revenue vs Churn Probability",
                     color_discrete_map={"High":"#e74c3c","Medium":"#f39c12","Low":"#27ae60"},
                     labels={"monthly_charges":"Monthly Charges ($)","churn_probability":"Churn Probability"})
    st.plotly_chart(fig, use_container_width=True)

elif page == "Retention Strategy":
    st.title("Retention Strategy")
    st.caption("What should we do?")

    seg_counts = df["retention_segment"].value_counts()
    fig = px.bar(x=seg_counts.index, y=seg_counts.values, title="Customer Segments",
                 color=seg_counts.index, color_discrete_map={
                     "High Risk - High Value":"#c0392b","High Risk - Standard Value":"#e74c3c",
                     "Medium Risk":"#f39c12","Low Risk":"#27ae60"})
    fig.update_layout(showlegend=False, xaxis_title="Retention Segment", yaxis_title="Customer Count")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recommended Retention Actions")
        st.markdown("""
        1. **Target High Risk-High Value customers first** — personal retention calls, loyalty discounts, contract upgrade offers, dedicated support

        2. **Introduce longer-term contract incentives** — Month-to-month customers churn at ~2x the rate; offer discounts for annual contracts

        3. **Proactively address repeated support issues** — Customers with 5+ support calls show significantly elevated churn; resolve root causes

        4. **Monitor new customers during first 12 months** — 0-6 month tenure has highest churn; implement onboarding campaigns

        5. **Use ML risk scores to personalize campaigns** — Probability × value prioritization ensures maximum ROI on retention spend
        """)

    with col2:
        st.subheader("Key Management Insight")
        st.info("""
        Our ML model identifies customers at risk of churning, combining predicted probability with revenue exposure.

        **High Risk-High Value** customers represent the greatest retention opportunity — proactive intervention here delivers maximum ROI.

        Month-to-month contracts and high support calls are the strongest churn indicators. Retention resources should be prioritized using both churn probability and financial exposure, not probability alone.
        """)

    st.divider()
    st.subheader("Segment Strategy Reference")

    strategy_data = pd.DataFrame({
        "Segment": ["High Risk - High Value", "High Risk - Standard Value", "Medium Risk", "Low Risk"],
        "Priority": ["★★★★★", "★★★★", "★★★", "★"],
        "Actions": [
            "Personal retention call, loyalty discount, contract upgrade, dedicated support",
            "Retention call, discount offer, contract incentive",
            "Automated campaign, satisfaction survey, targeted email",
            "Normal engagement, loyalty program, upsell/cross-sell"
        ]
    })
    st.dataframe(strategy_data, use_container_width=True, hide_index=True)
