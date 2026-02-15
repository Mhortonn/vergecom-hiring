import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (Max Density View) ──
st.set_page_config(page_title="Vergecom | Ops Control", page_icon="🏢", layout="wide")

# ── DSI CORPORATE STYLING (FIXED SYNTAX) ──
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
    <span>Assign Technician - Vergecom Operational Console</span>
    <span style="font-size: 14px; font-weight: 400;">{date}</span>
</div>
""".replace("{date}", datetime.now().strftime("%A, %B %d, %Y")), unsafe_allow_html=True)

# ── SUPABASE AUTH ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── DATA FETCHING & SANITIZATION ──
@st.cache_data(ttl=2)
def get_sanitized_data():
    try:
        res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
        if not res.data: return pd.DataFrame()
        
        temp_df = pd.DataFrame(res.data)

        # 1. STANDARDIZE COLUMN NAMES (Ensures 'email' is found)
        temp_df.columns = [c.lower() for c in temp_df.columns]
        
        # 2. FIX RADIUS: Force to numeric to stop StreamlitAPIException
        if 'radius' in temp_df.columns:
            temp_df['radius'] = pd.to_numeric(temp_df['radius'], errors='coerce').fillna(0).astype(int)
        
        # 3. FIX DATES: Force standardized format
        if 'created_at' in temp_df.columns:
            temp_df['created_at'] = pd.to_datetime(temp_df['created_at'], errors='coerce')
        
        # 4. CLEAN NULLS: Force everything else to string for stable display
        for col in temp_df.columns:
            if col not in ['radius', 'created_at']:
                temp_df[col] = temp_df[col].fillna("—").astype(str)
        return temp_df
    except Exception:
        return pd.DataFrame()

df = get_sanitized_data()

# ── 1-CLICK TOP FILTERS ──
with st.container():
    c1, c2, c3, c4 = st.columns([2, 1, 1, 0.8])
    with c1: q = st.text_input("Master Search", placeholder="Search Name, Phone, or Territory...", label_visibility="collapsed")
    
    states = sorted(df['state'].unique().tolist()) if not df.empty and 'state' in df.columns else []
    with c2: s_state = st.selectbox("State Filter", ["All States"] + states, label_visibility="collapsed")
    with c3: s_status = st.selectbox("Pipeline Stage", ["All", "NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], label_visibility="collapsed")
    with c4: st.button("Apply Filters", use_container_width=True)

# ── THE MASTER DATA GRID (DSI SYSTEMS STYLE) ──

if not df.empty:
    f_df = df.copy()
    
    # Apply Filters
    if q:
        f_df = f_df[f_df.apply(lambda row: row.astype(str).str.contains(q, case=False).any(), axis=1)]
    if s_state != "All States" and 'state' in f_df.columns:
        f_df = f_df[f_df['state'] == s_state]
    if s_status != "All" and 'status' in f_df.columns:
        f_df = f_df[f_df['status'] == s_status]

    # ALL FIELDS FROM APPLICATION (Displayed as Columns)
    all_requested_cols = [
        'id', 'name', 'phone', 'email', 'state', 'counties', 'radius', 
        'experience', 'exp_types', 'vehicle', 'ladder', 
        'tools', 'insurance', 'status', 'notes', 'created_at'
    ]

    # Only select columns that actually exist in your Supabase table
    existing_cols = [col for col in all_requested_cols if col in f_df.columns]

    st.write(f"**Technicians Loaded:** {len(f_df)}")

    # THE MASTER GRID: EDITABLE AND NO EXTRA CLICKS REQUIRED
    edited_df = st.data_editor(
        f_df[existing_cols], 
        use_container_width=True,
        height=600,
        hide_index=True,
        column_config={
            "id": None, 
            "name": st.column_config.TextColumn("Technician Name", width="medium"),
            "phone": "Contact No.",
            "email": st.column_config.TextColumn("Email Address", width="medium"),
            "state": "State",
            "counties": st.column_config.TextColumn("Territory", width="medium"),
            "radius": st.column_config.NumberColumn("Radius", format="%d mi"),
            "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True),
            "notes": st.column_config.TextColumn("Internal Notes (Editable)", width="large"),
            "created_at": st.column_config.DatetimeColumn("Joined", format="MM/DD/YY"),
        }
    )

    # ── DATABASE SYNC ──
    if st.button("💾 SYNCHRONIZE MASTER REGISTRY", type="primary", use_container_width=True):
        for index, row in edited_df.iterrows():
            original_row = df[df['id'] == row['id']].iloc[0]
            if row['status'] != original_row['status'] or row['notes'] != original_row['notes']:
                supabase.table("applicants").update({
                    "status": row['status'],
                    "notes": row['notes']
                }).eq("id", row['id']).execute()
        
        st.success("Record Synchronized Successfully.")
        st.cache_data.clear()
        st.rerun()

    # Asset Verification section
    st.markdown("---")
    preview_name = st.selectbox("Select technician to view assets:", f_df['name'].unique())
    if preview_name:
        assets = f_df[f_df['name'] == preview_name].iloc[0]
        p1, p2 = assets.get("photo1_url"), assets.get("photo2_url")
        if (p1 and p1 != "—") or (p2 and p2 != "—"):
            i1, i2 = st.columns(2)
            if p1 and p1 != "—": i1.image(p1, caption="Asset 1", use_container_width=True)
            if p2 and p2 != "—": i2.image(p2, caption="Asset 2", use_container_width=True)
else:
    st.error("Registry Offline or Data Missing.")
