import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (Enterprise Grade) ──
st.set_page_config(page_title="Vergecom | Ops Control", page_icon="⚙️", layout="wide")

# ── DSI CORPORATE STYLING ──
st.markdown("""
<style>
    html, body, [class*="st-"] { font-family: 'Segoe UI', Arial, sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
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

# ── DATA FETCHING WITH TYPE-CLEANING (CRITICAL FIX) ──
@st.cache_data(ttl=2)
def get_ops_data():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    if not res.data: return pd.DataFrame()
    
    df = pd.DataFrame(res.data)
    
    # FIX: Force 'radius' to be numeric and fill empty values with 0
    # This prevents the StreamlitAPIException type mismatch error
    if 'radius' in df.columns:
        df['radius'] = pd.to_numeric(df['radius'], errors='coerce').fillna(0).astype(int)
    
    # Ensure other columns are strings to prevent display issues
    cols_to_str = ['state', 'counties', 'status', 'notes']
    for col in cols_to_str:
        if col in df.columns:
            df[col] = df[col].fillna("Not Provided").astype(str)
            
    return df

df = get_ops_data()

# ── FILTERS (DSI STYLE) ──
with st.container():
    c1, c2, c3, c4 = st.columns([2, 1, 1, 0.8])
    with c1: search_name = st.text_input("Search Registry", placeholder="Name, Phone, or County...")
    with c2: search_state = st.selectbox("State Filter", ["All States"] + (sorted(df['state'].unique().tolist()) if not df.empty else []))
    with c3: search_status = st.selectbox("Assignment Status", ["All", "NEW", "REVIEWED", "HIRED", "REJECTED"])
    with c4: st.write(""); st.button("Apply Filters", use_container_width=True)

# ── MASTER DATA GRID (NO CLICKS NEEDED) ──
if not df.empty:
    f_df = df.copy()
    if search_name:
        f_df = f_df[f_df['name'].str.contains(search_name, case=False, na=False) | 
                    f_df['counties'].str.contains(search_name, case=False, na=False)]
    if search_state != "All States":
        f_df = f_df[f_df['state'] == search_state]
    if search_status != "All":
        f_df = f_df[f_df['status'] == search_status]

    st.write(f"**Records Found:** {len(f_df)}")
    
    # THE DATA EDITOR (Click cells to edit instantly)
    # This renders all info in one big corporate-style table
    edited_df = st.data_editor(
        f_df[['id', 'name', 'phone', 'state', 'counties', 'radius', 'experience', 'status', 'notes', 'created_at']],
        use_container_width=True,
        height=550,
        hide_index=True,
        column_config={
            "id": None, # Hide ID
            "name": st.column_config.TextColumn("Technician Name", width="medium"),
            "phone": "Contact Info",
            "state": "Region",
            "counties": st.column_config.TextColumn("Assigned Counties", width="large"),
            "radius": st.column_config.NumberColumn("Radius (mi)", format="%d"),
            "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True),
            "notes": st.column_config.TextColumn("Admin Notes (Editable)", width="large"),
            "created_at": st.column_config.DatetimeColumn("Registered", format="MM/DD/YY"),
        }
    )

    # ── SYNC BUTTON (CLICK #2) ──
    if st.button("💾 SYNC SYSTEM CHANGES", type="primary", use_container_width=True):
        # Update only the edited rows
        for index, row in edited_df.iterrows():
            # Get original version to check for changes
            original_row = df[df['id'] == row['id']].iloc[0]
            if row['status'] != original_row['status'] or row['notes'] != original_row['notes']:
                supabase.table("applicants").update({
                    "status": row['status'],
                    "notes": row['notes']
                }).eq("id", row['id']).execute()
        
        st.success("System Synchronized.")
        st.cache_data.clear()
        st.rerun()
else:
    st.error("No data found in Supabase. Check your connection.")
