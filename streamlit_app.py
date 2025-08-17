
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Automobile Checklist", page_icon="🚗", layout="wide")

DATA_FILE = Path("checklist_data.xlsx")

USERS = {
    "admin":   {"password": "admin123", "department": "HR"},
    "leader1": {"password": "pass456",  "department": "Assembly"},
    "store01": {"password": "store789", "department": "Store"},
    "maint01": {"password": "mnt456",   "department": "Maintenance"},
    "wip01":   {"password": "wip456",   "department": "WIP"},
    "disp01":  {"password": "dsp456",   "department": "Dispatch"},
}

if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None

st.markdown("<h1>🚗 Automobile Checklist</h1>", unsafe_allow_html=True)
st.caption("Streamlit version • Login → Checklist → Excel save → Analytics")

with st.form("login_form", clear_on_submit=False):
    st.write("### Login")
    username = st.text_input("Username")
    department = st.selectbox("Department", ["", "HR", "Assembly", "Maintenance", "Store", "WIP", "Dispatch"])
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    user = USERS.get(username)
    if user and user["password"] == password and user["department"] == department:
        st.session_state.auth = True
        st.session_state.user = {"username": username, "department": department}
        st.success("Login successful. Use the left sidebar to open **Checklist** or **Analytics**.")
    else:
        st.error("Invalid username, password, or department.")

st.sidebar.header("Navigation")
st.sidebar.page_link("streamlit_app.py", label="🏠 Home / Login")
st.sidebar.page_link("pages/1_Checklist.py", label="📝 Checklist")
st.sidebar.page_link("pages/2_Analytics.py", label="📊 Analytics")

st.divider()
exists = DATA_FILE.exists()
st.write("**Data file**:", "✅ Present" if exists else "❌ Not yet created")
if exists:
    try:
        df = pd.read_excel(DATA_FILE)
        st.write("Rows:", len(df))
        st.download_button("⬇️ Download Excel", data=DATA_FILE.read_bytes(), file_name="checklist_data.xlsx")
    except Exception as e:
        st.warning(f"Could not read Excel yet: {e}")
