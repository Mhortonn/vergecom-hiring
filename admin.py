import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (MAX WIDGET DENSITY) ──
st.set_page_config(page_title="Vergecom | Ops Control", page_icon="⚙️", layout="wide")

# ── DSI CORPORATE STYLING (Blue Header & Sharp Grid) ──
st.markdown("""
<style>
    html, body, [class*="st-"] { font-family: 'Segoe UI', Arial, sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    /* DSI Corporate Blue Header */
    .portal-header {
        background-color: #00539B;
        color: white;
        padding: 12px 24px;
        margin-bottom: 15px;
        border-radius: 2px;
        font-weight: 700;
        font-size: 22px;
        display: flex;
        justify-content: space-between;
    }
    
    /* Remove padding to fit more data */
    .block-container { padding-top: 1rem !important; }
</style>
<div class="portal-header">
    <span>Assign Technician - Vergecom Operations</span>
    <span style="font-size: 14px; font-weight: 400;">{date}</span>
</div>
""".replace("{date}", datetime.now().strftime("%A, %B %d, %Y")), unsafe_allow_html=True)

# ── SUPABASE AUTH ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── DATA RECOVERY (FAIL-SAFE) ──
@st.cache_data(ttl=2)
def get_master_data():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    if not res.data: return pd.DataFrame()
    
    df = pd.DataFrame(res.data)
    # FIX: Ensure radius is always a number and handle NULLs to prevent st.data_editor crash
    if 'radius' in df.columns:
        df['radius'] = pd.to_numeric(df['radius'], errors='coerce').fillna(0).astype(int)
    return df

df = get_master_data()

# ── 1-CLICK TOP FILTERS ──
with st.container():
    f1, f2, f3, f4 = st.columns([2, 1, 1, 0.8])
    with f1: s_name = st.text_input("Technician / County Search", placeholder="Filter registry...")
    with f2: s_state = st.selectbox("State", ["All"] + sorted(df['state'].unique().tolist()) if not df.empty else ["All"])
    with f3: s_status = st.selectbox("Assignment Status", ["All", "NEW", "REVIEWED", "HIRED", "REJECTED"])
    with f4: st.write(""); st.button("Apply Filters", use_container_width=True)

# ── FULL TEXT DISPLAY GRID (NO CLICKS NEEDED) ──
if not df.empty:
    # Filter Logic
    f_df = df.copy()
    if s_name: f_df = f_df[f_df['name'].str.contains(s_name, case=False) | f_df['counties'].str.contains(s_name, case=False)]
    if s_state != "All": f_df = f_df[f_df['state'] == s_state]
    if s_status != "All": f_df = f_df[f_df['status'] == s_status]

    st.write(f"**Technicians in Pipeline:** {len(f_df)}")

    # ── THE DATA EDITOR (EVERYTHING DISPLAYED AT ONCE) ──
    # User can edit 'Status' and 'Admin Notes' directly in the table
    edited_data = st.data_editor(
        f_df[['id', 'name', 'phone', 'email', 'state', 'counties', 'radius', 'experience', 'status', 'notes', 'created_at']],
        use_container_width=True,
        height=550,
        hide_index=True,
        column_config={
            "id": None, # Keep hidden
            "name": st.column_config.TextColumn("Technician Name", width="medium"),
            "phone": st.column_config.TextColumn("Contact Info", width="small"),
            "email": st.column_config.TextColumn("Email Address", width="medium"),
            "state": "Region",
            "counties": st.column_config.TextColumn("Assigned Counties", width="large"),
            "radius": st.column_config.NumberColumn("Radius (mi)", format="%d"),
            "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True),
            "notes": st.column_config.TextColumn("Operational Notes (Editable)", width="large"),
            "created_at": st.column_config.DatetimeColumn("Registered", format="MM/DD/YY"),
        }
    )

    # ── FINAL ACTION: THE SYNC BUTTON ──
    if st.button("💾 SYNC SYSTEM CHANGES", type="primary", use_container_width=True):
        # Only update if something actually changed
        for index, row in edited_data.iterrows():
            orig = df[df['id'] == row['id']].iloc[0]
            if row['status'] != orig['status'] or row['notes'] != orig['notes']:
                supabase.table("applicants").update({
                    "status": row['status'],
                    "notes": row['notes']
                }).eq("id", row['id']).execute()
        
        st.success("Operational Record Synchronized.")
        st.cache_data.clear()
        st.rerun()

else:
    st.error("Registry Empty: Unable to reach technician database.")
