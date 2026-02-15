import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (Enterprise Wide View) ──
st.set_page_config(page_title="Vergecom | Management Console", page_icon="🏢", layout="wide")

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
    
    /* Make the grid look like a professional ERP system */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
    }
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
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    if not res.data: return pd.DataFrame()
    
    df = pd.DataFrame(res.data)
    
    # CRITICAL: Clean Radius to prevent StreamlitAPIException
    if 'radius' in df.columns:
        df['radius'] = pd.to_numeric(df['radius'], errors='coerce').fillna(0).astype(int)
    
    # CRITICAL: Clean Dates
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    
    # Force everything else to string to ensure display
    for col in df.columns:
        if col not in ['radius', 'created_at']:
            df[col] = df[col].fillna("—").astype(str)
            
    return df

df = get_sanitized_data()

# ── 1-CLICK TOP FILTERS ──
with st.container():
    c1, c2, c3, c4 = st.columns([2, 1, 1, 0.8])
    with c1: q = st.text_input("Master Search", placeholder="Search Name, Phone, or Territory...")
    with c2: s_state = st.selectbox("State", ["All States"] + (sorted(df['state'].unique().tolist()) if not df.empty else []))
    with c3: s_status = st.selectbox("Pipeline Stage", ["All", "NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"])
    with c4: st.write(""); st.button("Apply Filters", use_container_width=True)

# ── FULL TEXT SYSTEM GRID (ALL DATA VISIBLE) ──
if not df.empty:
    f_df = df.copy()
    if q:
        f_df = f_df[f_df.apply(lambda row: row.astype(str).str.contains(q, case=False).any(), axis=1)]
    if s_state != "All States":
        f_df = f_df[f_df['state'] == s_state]
    if s_status != "All":
        f_df = f_df[f_df['status'] == s_status]

    st.write(f"**Technicians Loaded:** {len(f_df)}")
    
    # THE MASTER GRID: EVERY TAB FIELD INTEGRATED
    edited_df = st.data_editor(
        f_df[[
            'id', 'name', 'phone', 'state', 'counties', 'radius', 
            'experience', 'exp_types', 'vehicle', 'ladder', 
            'tools', 'insurance', 'status', 'notes', 'created_at'
        ]],
        use_container_width=True,
        height=600,
        hide_index=True,
        column_config={
            "id": None, 
            "name": st.column_config.TextColumn("Name", width="medium"),
            "phone": "Contact",
            "state": "State",
            "counties": st.column_config.TextColumn("Counties Covered", width="medium"),
            "radius": st.column_config.NumberColumn("Radius", format="%d mi"),
            "experience": "Years",
            "exp_types": st.column_config.TextColumn("Skills (Starlink/TV/Cable)", width="medium"),
            "vehicle": "Truck?",
            "ladder": "Ladder?",
            "tools": "Tools?",
            "insurance": "Insured?",
            "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True),
            "notes": st.column_config.TextColumn("Operational Notes (Edit Here)", width="large"),
            "created_at": st.column_config.DatetimeColumn("Joined", format="MM/DD/YY"),
        }
    )

    # ── FINAL ACTION: DATABASE SYNC ──
    if st.button("💾 SYNCHRONIZE MASTER REGISTRY", type="primary", use_container_width=True):
        updated_count = 0
        for index, row in edited_df.iterrows():
            orig = df[df['id'] == row['id']].iloc[0]
            # Only update if Status or Notes were touched
            if row['status'] != orig['status'] or row['notes'] != orig['notes']:
                supabase.table("applicants").update({
                    "status": row['status'],
                    "notes": row['notes']
                }).eq("id", row['id']).execute()
                updated_count += 1
        
        st.success(f"System Synchronized. {updated_count} records updated.")
        st.cache_data.clear()
        st.rerun()

    # Image Preview logic (No clicking names, just select name from dropdown to see photos)
    st.markdown("---")
    st.markdown("#### 🖼️ Technician Asset Verification")
    preview_name = st.selectbox("Select technician to verify install photos:", f_df['name'].unique())
    if preview_name:
        assets = f_df[f_df['name'] == preview_name].iloc[0]
        p1, p2 = assets.get("photo1_url"), assets.get("photo2_url")
        if (p1 and p1 != "—") or (p2 and p2 != "—"):
            i1, i2 = st.columns(2)
            if p1 and p1 != "—": i1.image(p1, caption="Asset Photo 1", use_container_width=True)
            if p2 and p2 != "—": i2.image(p2, caption="Asset Photo 2", use_container_width=True)
        else:
            st.info("No photo assets uploaded for this technician.")

else:
    st.error("Registry Offline: No data returned from Supabase.")
