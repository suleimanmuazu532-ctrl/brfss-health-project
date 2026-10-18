import pandas as pd
import streamlit as st

st.title("Diabetes and Income: BRFSS 2025")
st.caption("Survey sample rates, not weighted to the US population. Shows association, not cause.")

@st.cache_data
def load_data():
    return pd.read_csv("data/brfss_clean.csv.gz")

df = load_data()

income_order = ["<$10k", "$10-15k", "$15-20k", "$20-25k", "$25-35k",
                "$35-50k", "$50-75k", "$75-100k", "$100-150k", "$150-200k", "$200k+"]

# Filters in the sidebar
age_choice = st.sidebar.selectbox("Age band", ["All", "18-44", "45-64", "65+"])
sex_choice = st.sidebar.selectbox("Sex", ["All", "Female", "Male"])

filtered = df.copy()
if age_choice != "All":
    filtered = filtered[filtered["age_band"] == age_choice]
if sex_choice != "All":
    filtered = filtered[filtered["sex"] == sex_choice]

st.write("People in this view:", len(filtered))

# Diabetes rate by income
rates = (filtered.groupby("income")["has_diabetes"]
         .mean().mul(100).round(1)
         .reindex(income_order))

st.subheader("Diabetes rate by income")
st.bar_chart(rates)
st.caption("Percent of people with diabetes in each income group.")
