import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (Max Density View) ──
st.set_page_config(page_title="Vergecom | Ops Control", page_icon="⚙️", layout="wide")

# ── DSI CORPORATE STYLING ──
st.markdown("""
<style>
    html, body, [class*="st-"] { font-family: 'Segoe UI', Arial, sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    .portal-header {
        background-color: #00539B;
        color: white;
        padding: 14px 24px;
        margin-bottom: 15px;
        border-radius: 2px;
        font-weight: 700;
        font-size: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .block-container { padding-top: 1rem !important; }
</style>
<div class="portal-header">
    <span>Assign Technician - Vergecom Contractor Portal</span>
    <span style="font-size: 14px; font-weight: 400;">{date}</span>
</div>
""".replace("{date}", datetime.now().strftime("%A, %B %d, %Y")), unsafe_allow_html=True)

# ── SUPABASE AUTH ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── DATA FETCHING WITH TYPE-CLEANING (CRITICAL FIX) ──
@st.cache_data(ttl=2)
def get_ops_data():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    if not res.data: return pd.DataFrame()
    
    df = pd.DataFrame(res.data)
    
    # 1. FIX RADIUS: Force to numeric and turn NULLs into 0
    # This specifically stops the StreamlitAPIException crash
    if 'radius' in df.columns:
        df['radius'] = pd.to_numeric(df['radius'], errors='coerce').fillna(0).astype(int)
    
    # 2. FIX DATES: Force to standardized datetime format
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    
    # 3. FIX TEXT: Force empty fields to a clean "N/A" string
    cols_to_clean = ['state', 'counties', 'status', 'notes', 'experience', 'phone']
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].fillna("Not Provided").astype(str)
            
    return df

df = get_ops_data()

# ── SEARCH FILTERS (TOP BAR) ──
with st.container():
    c1, c2, c3, c4 = st.columns([2, 1, 1, 0.8])
    with c1: search_name = st.text_input("Registry Search", placeholder="Name, Phone, or County...")
    with c2: search_state = st.selectbox("Filter State", ["All States"] + (sorted(df['state'].unique().tolist()) if not df.empty else []))
    with c3: search_status = st.selectbox("Pipeline Status", ["All", "NEW", "REVIEWED", "HIRED", "REJECTED"])
    with c4: st.write(""); st.button("Apply Changes", use_container_width=True)

# ── THE MASTER DATA GRID (DSI SYSTEMS STYLE) ──
if not df.empty:
    f_df = df.copy()
    if search_name:
        f_df = f_df[f_df['name'].str.contains(search_name, case=False) | 
                    f_df['counties'].str.contains(search_name, case=False)]
    if search_state != "All States":
        f_df = f_df[f_df['state'] == search_state]
    if search_status != "All":
        f_df = f_df[f_df['status'] == search_status]

    # Render exactly 10 columns with all text info visible instantly
    edited_df = st.data_editor(
        f_df[['id', 'name', 'phone', 'state', 'counties', 'radius', 'experience', 'status', 'notes', 'created_at']],
        use_container_width=True,
        height=550,
        hide_index=True,
        column_config={
            "id": None, # Hide database ID
            "name": st.column_config.TextColumn("Technician Name", width="medium"),
            "phone": "Contact No.",
            "state": "Region",
            "counties": st.column_config.TextColumn("Assigned Territory", width="large"),
            "radius": st.column_config.NumberColumn("Radius (mi)", format="%d"),
            "experience": "Exp Level",
            "status": st.column_config.SelectboxColumn("Portal Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True),
            "notes": st.column_config.TextColumn("Operational Notes (Type to Edit)", width="large"),
            "created_at": st.column_config.DatetimeColumn("Joined", format="MM/DD/YY"),
        }
    )

    # ── SYNC ACTION (THE 2ND BUTTON) ──
    if st.button("💾 SYNCHRONIZE DATABASE CHANGES", type="primary", use_container_width=True):
        for index, row in edited_df.iterrows():
            # Only push updates if Status or Notes were changed in the grid
            original_row = df[df['id'] == row['id']].iloc[0]
            if row['status'] != original_row['status'] or row['notes'] != original_row['notes']:
                supabase.table("applicants").update({
                    "status": row['status'],
                    "notes": row['notes']
                }).eq("id", row['id']).execute()
        
        st.success("Operational Pipeline Updated.")
        st.cache_data.clear()
        st.rerun()
else:
    st.warning("Database Connection Active: No technician records found.")
