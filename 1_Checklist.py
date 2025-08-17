
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Checklist", page_icon="📝", layout="wide")

DATA_FILE = Path("checklist_data.xlsx")

QUESTIONS = [
    "Identification tag available in all part in assembly",
    "NG, rework, customer return, recovery or hold components in lock and key area",
    "Rework part 100% recheck on Leak and Light test",
    "Clean WIP bins, FG boxes, chutters in one line.",
    "AMC, Poka-yoke check sheet,  production report, LPA, report updated signed by TL",
    "Random check for confirmation, SPPS & AMC is set against the nominal value and not utilizing the tolerance",
    "Rework quarantine area physical parts matching with register and empro records",
    "Cleanliness, no leaks, dust, fallen parts, on assembly line.",
    "Parts not lying in non intended areas, storage in pre marked areas only",
    "ensure all material handover to store team through Empro after setup change.",
    "Burst testing is done till the part breaks and the data is recorded accordingly",
    "Safety PPE, Electronics PPE adherence",
    "No entry points on the line except the ESD tripod ESD Tripod wrist bend and foot strip in working.",
    "All FG boxes are carried to despatch area after sealing",
    "all incomplete boxes/trolleys of FW checked parts are sealed and handed over to Despatch at the shift or week end.",
    "All station in one line and place with marking.",
    "Dustbin with categorise identification and place marking.",
    "Final station customer compliant OPL display, Data Entry online, Defect record , poison test record.",
    "Axillarys on line dust free, identification, validation and close , place marking.",
    "Chutter rack in one line with 5T and flag identification. No broken and No dust.",
    "Gluing m/c All symbolic identification as per AMC and wire harness routing, No glue spread on floor and dust free entire unit.",
    "Single Pease flow follow"
]

if "auth" not in st.session_state or not st.session_state.auth:
    st.error("Please login first on the Home page.")
    st.stop()

st.title("📝 Checklist Form")

with st.form("pre_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        date = st.date_input("Date")
        machine = st.text_input("Line/Machine")
    with c2:
        leader = st.text_input("Line Leader")
        shift = st.text_input("Shift Incharge")
    with c3:
        process = st.text_input("Process")
        auditor = st.text_input("Auditor")

    st.write("### Questions")
    responses = {}
    remarks = {}
    for i, q in enumerate(QUESTIONS, start=1):
        st.write(f"**{i}. {q}**")
        responses[f"q{i}"] = st.radio(f"Q{i}", ["Yes", "No"], horizontal=True, label_visibility="collapsed", key=f"q{i}")
        remarks[f"r{i}"] = st.text_input("Remarks (required if No)", key=f"r{i}")
        st.divider()

    submitted = st.form_submit_button("Submit")

if submitted:
    for i in range(1, len(QUESTIONS)+1):
        if responses[f"q{i}"] == "No" and not remarks[f"r{i}"]:
            st.error(f"Remarks required for Question {i} because response is 'No'.")
            st.stop()

    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": st.session_state.user["username"],
        "department": st.session_state.user["department"],
        "date": str(date),
        "line_machine": machine,
        "line_leader": leader,
        "shift_incharge": shift,
        "process": process,
        "auditor": auditor,
    }
    for i in range(1, len(QUESTIONS)+1):
        payload[f"q{i}"] = responses[f"q{i}"]
        payload[f"r{i}"] = remarks[f"r{i}"]

    df_new = pd.DataFrame([payload])
    if DATA_FILE.exists():
        try:
            df_old = pd.read_excel(DATA_FILE)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        except Exception:
            df_all = df_new
    else:
        df_all = df_new
    df_all.to_excel(DATA_FILE, index=False)
    st.success("Checklist submitted and saved to Excel.")
    st.balloons()
