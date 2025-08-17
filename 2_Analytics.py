
import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

DATA_FILE = Path("checklist_data.xlsx")

if "auth" not in st.session_state or not st.session_state.auth:
    st.error("Please login first on the Home page.")
    st.stop()

st.title("📊 Analytics Dashboard")

if not DATA_FILE.exists():
    st.info("No data yet. Submit at least one checklist entry.")
    st.stop()

df = pd.read_excel(DATA_FILE)
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

with st.expander("Filters"):
    dept = st.multiselect("Department", sorted(df["department"].dropna().unique().tolist()))
    daterange = st.date_input("Date range", [])
    if dept:
        df = df[df["department"].isin(dept)]
    if len(daterange) == 2:
        start, end = daterange
        if "date" in df.columns:
            df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]

st.subheader("Submissions Over Time")
if "date" in df.columns and df["date"].notna().any():
    by_date = df.dropna(subset=["date"]).groupby(df["date"].dt.date).size()
else:
    by_date = df.groupby(df["timestamp"].dt.date).size() if "timestamp" in df.columns else pd.Series(dtype=int)

fig1, ax1 = plt.subplots()
by_date.sort_index().plot(kind="line", marker="o", ax=ax1)
ax1.set_xlabel("Date"); ax1.set_ylabel("Submissions"); ax1.set_title("Submissions Over Time")
st.pyplot(fig1)

st.subheader("Submissions by Department")
by_dept = df["department"].value_counts().sort_index() if "department" in df.columns else pd.Series(dtype=int)
fig2, ax2 = plt.subplots()
by_dept.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Department"); ax2.set_ylabel("Submissions"); ax2.set_title("Submissions by Department")
st.pyplot(fig2)

st.subheader("Yes/No Count per Question")
yes_counts, no_counts, labels = [], [], []
for i in range(1, 23):
    q = f"q{i}"
    if q in df.columns:
        yes_counts.append((df[q] == "Yes").sum())
        no_counts.append((df[q] == "No").sum())
        labels.append(str(i))
x = np.arange(len(labels))
fig3, ax3 = plt.subplots(figsize=(8,4))
ax3.bar(x, yes_counts, label="Yes")
ax3.bar(x, no_counts, bottom=yes_counts, label="No")
ax3.set_xticks(x, labels)
ax3.set_xlabel("Question #"); ax3.set_ylabel("Count"); ax3.set_title("Yes/No per Question"); ax3.legend()
st.pyplot(fig3)

st.subheader("No Rate per Question (%)")
no_rate = [(n / (y+n) * 100 if (y+n) else 0.0) for y, n in zip(yes_counts, no_counts)]
fig4, ax4 = plt.subplots(figsize=(8,4))
ax4.bar(x, no_rate)
ax4.set_xticks(x, labels)
ax4.set_xlabel("Question #"); ax4.set_ylabel("No Rate (%)"); ax4.set_title("No Rate per Question (%)")
st.pyplot(fig4)

st.divider()
st.write("### Raw Data")
st.dataframe(df, use_container_width=True)
