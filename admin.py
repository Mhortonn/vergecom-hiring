import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client

# ── CONFIG ──
st.set_page_config(page_title="Vergecom | Admin", page_icon="⚡", layout="wide")

# ── SUPABASE ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── DATA LOAD ──
@st.cache_data(ttl=2)
def load_applicants():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return res.data or []

if "view_id" not in st.session_state:
    st.session_state.view_id = None

data = load_applicants()

# ── HEADER ──
st.title("🚀 Vergecom Hiring Dashboard")
st.write(f"Showing {len(data)} applicants")

# ─────────────────────────
# DETAIL VIEW (THE NEW FAIL-PROOF VERSION)
# ─────────────────────────
if st.session_state.view_id:
    record = next((d for d in data if str(d["id"]) == str(st.session_state.view_id)), None)
    
    if st.button("← BACK TO LIST"):
        st.session_state.view_id = None
        st.rerun()

    if record:
        st.header(f"Details for {record['name']}")
        
        # --- FAIL PROOF DATA BOXES ---
        st.subheader("📍 Coverage Area (Database Data)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("STATE", str(record.get("state", "MISSING")))
        with col2:
            st.metric("COUNTIES", str(record.get("counties", "MISSING")))
        with col3:
            st.metric("RADIUS", f"{record.get('radius', '0')} miles")

        st.markdown("---")
        
        # --- CONTACT & EXP ---
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Phone:** {record.get('phone')}")
            st.info(f"**Email:** {record.get('email')}")
        with c2:
            st.success(f"**Experience:** {record.get('experience')}")
            st.success(f"**Types:** {record.get('exp_types')}")

        # Notes Section
        new_notes = st.text_area("Hiring Notes", value=record.get("notes", ""))
        if st.button("Save Notes"):
            supabase.table("applicants").update({"notes": new_notes}).eq("id", record["id"]).execute()
            st.cache_data.clear()
            st.success("Saved!")

    st.stop()

# ─────────────────────────
# LIST VIEW
# ─────────────────────────
if not data:
    st.warning("No applicants found in database.")
else:
    # Create a simple table view so you can see everything at once
    df = pd.DataFrame(data)
    # Reorder columns to show your important ones first
    cols = ["name", "state", "counties", "radius", "phone", "status"]
    available_cols = [c for c in cols if c in df.columns]
    
    st.dataframe(df[available_cols], use_container_width=True)

    st.write("### Click to View Full Profile")
    for app in data:
        # Create a button for each person
        label = f"View {app['name']} | {app.get('state', 'No State')} | {app.get('phone')}"
        if st.button(label, key=f"list_{app['id']}"):
            st.session_state.view_id = app["id"]
            st.rerun()
