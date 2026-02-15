import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── CONFIG ──
st.set_page_config(page_title="Vergecom | Master Control", page_icon="🏢", layout="wide")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ── STYLING ──
st.markdown("""
<style>
    html, body, [class*="st-"] { font-family: 'Segoe UI', Arial, sans-serif; }
    .stApp { background-color: #F8FAFC; }
    .portal-header { background-color: #00539B; color: white; padding: 14px 24px; font-weight: 700; font-size: 24px; border-radius: 2px; display: flex; justify-content: space-between; align-items: center; }
</style>
<div class="portal-header">
    <span>Vergecom Master Console</span>
    <span style="font-size: 14px; font-weight: 400;">SYSTEM ACTIVE</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["👥 Applicant Registry", "🛠️ Website Maintenance"])

# ── TAB 1: REGISTRY MAINTENANCE (THE GRID) ──
with tab1:
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    
    if not df.empty:
        # Data Cleaning for Stability
        if 'radius' in df.columns:
            df['radius'] = pd.to_numeric(df['radius'], errors='coerce').fillna(0).astype(int)
        
        existing_cols = [c for c in ['id', 'name', 'phone', 'email', 'state', 'counties', 'radius', 'status', 'notes', 'created_at'] if c in df.columns]
        
        # High Density Editor
        edited_df = st.data_editor(
            df[existing_cols], 
            use_container_width=True, 
            height=500, 
            hide_index=True,
            column_config={"id": None, "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True)}
        )
        
        if st.button("💾 SYNC REGISTRY CHANGES", type="primary"):
            for index, row in edited_df.iterrows():
                orig = df[df['id'] == row['id']].iloc[0]
                if row['status'] != orig['status'] or row['notes'] != orig['notes']:
                    supabase.table("applicants").update({"status": row['status'], "notes": row['notes']}).eq("id", row['id']).execute()
            st.success("Registry Synchronized.")
            st.rerun()

# ── TAB 2: WEBSITE MAINTENANCE (DYNAMIC CONTENT) ──
with tab2:
    st.subheader("Edit Website Job Description & Hero Text")
    
    # Fetch current live site settings
    res_set = supabase.table("site_settings").select("*").eq("id", 1).single().execute()
    curr = res_set.data
    
    with st.form("site_editor"):
        new_title = st.text_input("Main Website Title", value=curr['hero_title'])
        new_desc = st.text_area("Job Description / Intro Text", value=curr['job_desc'], height=200)
        new_reqs = st.text_area("Minimum Requirements (Text)", value=curr['requirements'], height=150)
        
        if st.form_submit_button("🚀 PUBLISH UPDATES TO MAIN SITE"):
            supabase.table("site_settings").update({
                "hero_title": new_title,
                "job_desc": new_desc,
                "requirements": new_reqs,
                "last_updated": datetime.now().isoformat()
            }).eq("id", 1).execute()
            st.success("Website Content Updated Live.")
            st.cache_data.clear()
