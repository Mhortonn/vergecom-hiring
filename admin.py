import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (Enterprise Wide View) ──
st.set_page_config(page_title="Vergecom | Master Control", page_icon="🏢", layout="wide")

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
    <span>Master Registry - Vergecom Operations Console</span>
    <span style="font-size: 14px; font-weight: 400;">{date}</span>
</div>
""".replace("{date}", datetime.now().strftime("%A, %B %d, %Y")), unsafe_allow_html=True)

# ── SUPABASE AUTH ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── DATA FETCHING & SANITIZATION ──
@st.cache_data(ttl=2)
def get_ops_data():
    try:
        res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
        if not res.data: return pd.DataFrame()
        
        temp_df = pd.DataFrame(res.data)
        # Normalize columns to lowercase to find 'email', 'phone', etc.
        temp_df.columns = [c.lower() for c in temp_df.columns]
        
        # Clean numeric columns to stop StreamlitAPIException crashes
        if 'radius' in temp_df.columns:
            temp_df['radius'] = pd.to_numeric(temp_df['radius'], errors='coerce').fillna(0).astype(int)
        
        # Standardize strings
        for col in temp_df.columns:
            if col not in ['radius', 'created_at']:
                temp_df[col] = temp_df[col].fillna("—").astype(str)
        return temp_df
    except Exception:
        return pd.DataFrame()

df = get_ops_data()

# ── FILTERS ──
with st.container():
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: q = st.text_input("Search Database", placeholder="Search Name, Phone, Email, or Territory...", label_visibility="collapsed")
    with c2: s_state = st.selectbox("State Filter", ["All States"] + (sorted(df['state'].unique().tolist()) if not df.empty else []), label_visibility="collapsed")
    with c3: s_status = st.selectbox("Status Filter", ["All", "NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], label_visibility="collapsed")

# ────────────────────────────────────────────────────────
#  THE "EDIT EVERYTHING" MASTER GRID
# ────────────────────────────────────────────────────────
if not df.empty:
    f_df = df.copy()
    
    # Filter Logic
    if q:
        f_df = f_df[f_df.apply(lambda row: row.astype(str).str.contains(q, case=False).any(), axis=1)]
    if s_state != "All States":
        f_df = f_df[f_df['state'] == s_state]
    if s_status != "All":
        f_df = f_df[f_df['status'] == s_status]

    st.write(f"**Records Found:** {len(f_df)} (Double-click any cell to change it)")

    # Define all possible application fields
    all_fields = [
        'id', 'name', 'phone', 'email', 'state', 'counties', 'radius', 
        'experience', 'exp_types', 'vehicle', 'ladder', 'tools', 
        'insurance', 'status', 'notes', 'created_at'
    ]
    
    # Filter to only existing columns
    display_cols = [c for c in all_fields if c in f_df.columns]

    # Render the Interactive Data Editor
    # This allows editing Name, Phone, Email, Radius, Counties, Skills, etc.
    edited_df = st.data_editor(
        f_df[display_cols],
        use_container_width=True,
        height=600,
        hide_index=True,
        column_config={
            "id": None, # Non-editable ID
            "name": st.column_config.TextColumn("Full Name", width="medium"),
            "phone": st.column_config.TextColumn("Phone No.", width="small"),
            "email": st.column_config.TextColumn("Email", width="medium"),
            "state": st.column_config.TextColumn("State", width="small"),
            "counties": st.column_config.TextColumn("Territory/Counties", width="large"),
            "radius": st.column_config.NumberColumn("Radius (mi)", format="%d"),
            "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True),
            "notes": st.column_config.TextColumn("Admin Notes", width="large"),
            "exp_types": "Skills/Types",
            "created_at": st.column_config.DatetimeColumn("Date Joined", format="MM/DD/YY"),
        }
    )

    # ── BUTTON 2: SYNC EVERYTHING ──
    if st.button("💾 SAVE ALL CHANGES TO SYSTEM", type="primary", use_container_width=True):
        updated_count = 0
        for index, row in edited_df.iterrows():
            # Find the original record in the DB to check for differences
            original = df[df['id'] == row['id']].iloc[0]
            
            # Detect changes across ALL editable fields
            if not row.equals(original):
                # Build the update dictionary dynamically
                update_data = {col: row[col] for col in display_cols if col not in ['id', 'created_at']}
                
                # Push update to Supabase
                supabase.table("applicants").update(update_data).eq("id", row['id']).execute()
                updated_count += 1
        
        if updated_count > 0:
            st.success(f"Successfully Synchronized {updated_count} technician records.")
            st.cache_data.clear()
            st.rerun()
        else:
            st.info("No changes detected in the registry.")

else:
    st.error("Registry Offline: Could not retrieve technician database.")
