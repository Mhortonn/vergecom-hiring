import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client

# ── CONFIG ──
st.set_page_config(page_title="Vergecom | Hiring", page_icon="⚡", layout="wide")

# ── SUPABASE ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing Supabase credentials")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── CONSTANTS ──
STATUS_LIST = ["NEW", "REVIEWED", "CONTACTED", "INTERVIEW", "HIRED", "REJECTED"]
STATUS_COLORS = {
    "NEW": "blue",
    "REVIEWED": "purple",
    "CONTACTED": "amber",
    "INTERVIEW": "cyan",
    "HIRED": "green",
    "REJECTED": "red",
}

# ── STYLES (FULL FIX) ──
st.markdown("""
<style>
:root {
    --blue:#2563EB; --blue-bg:#EFF6FF;
    --green:#059669; --green-bg:#ECFDF5;
    --red:#DC2626; --red-bg:#FEF2F2;

    --amber:#F59E0B; --amber-bg:#FFFBEB;
    --purple:#8B5CF6; --purple-bg:#F5F3FF;
    --cyan:#06B6D4; --cyan-bg:#ECFEFF;

    --border:#E5E7EB;
    --text-1:#111827;
    --text-2:#4B5563;
    --text-3:#9CA3AF;
}

.stApp { background:#FAFBFC; }
.block-container { max-width:1200px; padding-bottom:4rem; }

.applicant-card {
    background:white;
    border:1px solid var(--border);
    border-radius:12px;
    padding:1rem;
    margin-bottom:.5rem;
    display:grid;
    grid-template-columns:2fr 1fr 1fr 1.5fr 1fr 1fr;
    gap:.75rem;
}
.applicant-card:hover {
    border-color:var(--blue);
    box-shadow:0 0 0 1px var(--blue);
}

.s-badge {
    font-size:.6rem;
    font-weight:600;
    padding:.25rem .55rem;
    border-radius:6px;
    display:inline-block;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ──
@st.cache_data(ttl=5)
def load_applicants():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return res.data or []

def update_status(aid, status):
    supabase.table("applicants").update({"status": status}).eq("id", aid).execute()

def update_notes(aid, notes):
    supabase.table("applicants").update({"notes": notes}).eq("id", aid).execute()

def delete_applicant(aid):
    supabase.table("applicants").delete().eq("id", aid).execute()

def badge(status):
    c = STATUS_COLORS.get(status, "blue")
    return f'<span class="s-badge" style="background:var(--{c}-bg);color:var(--{c});">{status}</span>'

if "view_id" not in st.session_state:
    st.session_state.view_id = None

data = load_applicants()

# ── HEADER ──
st.markdown(f"""
<h2>Vergecom Hiring Dashboard</h2>
<p style="color:#6B7280">{len(data)} applicants · {datetime.now().strftime('%B %d, %Y')}</p>
""", unsafe_allow_html=True)

# ─────────────────────────
# DETAIL VIEW
# ─────────────────────────
if st.session_state.view_id:
    record = next((d for d in data if str(d["id"]) == str(st.session_state.view_id)), None)

    if not record:
        st.error("Applicant not found")
        st.stop()

    if st.button("← Back"):
        st.session_state.view_id = None
        st.rerun()

    st.markdown(f"""
    <h3>{record['name']}</h3>
    {badge(record.get("status","NEW"))}
    <p>{record.get("email","—")} · {record.get("phone","—")}</p>
    """, unsafe_allow_html=True)

    new_status = st.selectbox("Status", STATUS_LIST, index=STATUS_LIST.index(record.get("status","NEW")))
    if st.button("Save Status", type="primary"):
        update_status(record["id"], new_status)
        st.cache_data.clear()
        st.rerun()

    notes = st.text_area("Notes", record.get("notes",""))
    if st.button("Save Notes"):
        update_notes(record["id"], notes)
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    confirm = st.checkbox("I understand this cannot be undone")
    if confirm and st.button("🗑 Delete Applicant", type="primary"):
        delete_applicant(record["id"])
        st.cache_data.clear()
        st.session_state.view_id = None
        st.rerun()

    st.stop()

# ─────────────────────────
# LIST VIEW
# ─────────────────────────
for app in data:
    st.markdown(f"""
    <div class="applicant-card">
        <div>
            <b>{app.get("name","—")}</b><br>
            <span style="color:#9CA3AF">{app.get("email","")}</span>
        </div>
        <div>{app.get("state","—")}</div>
        <div>{app.get("phone","—")}</div>
        <div>{app.get("experience","—")}</div>
        <div>{badge(app.get("status","NEW"))}</div>
        <div>{app.get("created_at","")[:10]}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View", key=str(app["id"])):
        st.session_state.view_id = app["id"]
        st.rerun()
