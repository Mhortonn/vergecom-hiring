import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG ──
st.set_page_config(page_title="Vergecom | Management", page_icon="🏢", layout="wide")

# ── THE CORPORATE STYLE SHEET ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    /* Professional Card styling */
    .corp-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }

    /* Header Labels */
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    /* Profile Detail Styling */
    .detail-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 20px;
    }

    .data-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #F1F5F9;
    }

    .data-label {
        font-weight: 500;
        color: #64748B;
        font-size: 0.85rem;
    }

    .data-value {
        font-weight: 600;
        color: #1E293B;
        font-size: 0.85rem;
        text-align: right;
    }

    /* Sidebar Button styling */
    div[data-testid="stVerticalBlock"] > div:has(button) {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── SUPABASE AUTH ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── DATA FETCHING ──
@st.cache_data(ttl=5)
def get_data():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

df = get_data()

# ── SIDEBAR NAVIGATION ──
with st.sidebar:
    st.image("https://via.placeholder.com/150x40?text=VERGECOM", width=150) # Replace with your logo URL
    st.markdown("---")
    st.markdown("**CORE MANAGEMENT**")
    
    if st.button("↻ Refresh System Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("Vergecom Operations v2.1")

# ── TOP KPI ROW ──
if not df.empty:
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="corp-card"><div class="stat-label">Total Pipeline</div><div style="font-size:24px; font-weight:700;">{len(df)}</div></div>', unsafe_allow_html=True)
    with kpi2:
        fl_count = len(df[df['state'] == 'Florida']) if 'state' in df.columns else 0
        st.markdown(f'<div class="corp-card"><div class="stat-label">Florida Active</div><div style="font-size:24px; font-weight:700; color:#2563EB;">{fl_count}</div></div>', unsafe_allow_html=True)
    with kpi3:
        new_leads = len(df[df['status'] == 'NEW']) if 'status' in df.columns else 0
        st.markdown(f'<div class="corp-card"><div class="stat-label">New Review</div><div style="font-size:24px; font-weight:700; color:#059669;">{new_leads}</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="corp-card"><div class="stat-label">System Status</div><div style="font-size:24px; font-weight:700; color:#64748B;">Online</div></div>', unsafe_allow_html=True)

# ── MAIN SYSTEM INTERFACE ──
col_list, col_detail = st.columns([1, 1.5], gap="large")

# Left Column: Search & List
with col_list:
    st.markdown("#### Talent Pipeline")
    search = st.text_input("Filter by name or phone...", label_visibility="collapsed", placeholder="🔍 Search database...")
    
    if not df.empty:
        # Filter logic
        display_df = df.copy()
        if search:
            display_df = display_df[display_df['name'].str.contains(search, case=False, na=False)]
        
        for _, row in display_df.iterrows():
            with st.container():
                # Clean, clickable list items
                name = row['name']
                state = row.get('state', 'N/A')
                status = row.get('status', 'NEW')
                
                # We use a custom button label for the list
                btn_label = f"{name} • {state} ({status})"
                if st.button(btn_label, key=f"rec_{row['id']}", use_container_width=True):
                    st.session_state.view_id = row['id']
                    st.rerun()

# Right Column: Professional Detail View
with col_detail:
    if "view_id" in st.session_state and st.session_state.view_id:
        record = df[df['id'] == st.session_state.view_id].iloc[0]
        
        st.markdown(f'<div class="detail-header">{record["name"]}</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📋 Profile Info", "📡 Coverage & Experience", "⚙️ Admin Tools"])
        
        with tab1:
            st.markdown('<div class="corp-card">', unsafe_allow_html=True)
            fields = {
                "Phone Number": record.get("phone"),
                "Email Address": record.get("email"),
                "Application Date": record.get("created_at")[:10],
                "Current Status": record.get("status")
            }
            for label, value in fields.items():
                st.markdown(f'<div class="data-row"><div class="data-label">{label}</div><div class="data-value">{value}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="corp-card">', unsafe_allow_html=True)
            st.markdown("**TERRITORY DATA**")
            cov_fields = {
                "Primary State": record.get("state"),
                "Operating Counties": record.get("counties"),
                "Service Radius": f"{record.get('radius')} Miles"
            }
            for label, value in cov_fields.items():
                st.markdown(f'<div class="data-row"><div class="data-label">{label}</div><div class="data-value">{value}</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>**TECHNICAL BACKGROUND**", unsafe_allow_html=True)
            st.info(f"**Experience:** {record.get('experience')}\n\n**Specializations:** {record.get('exp_types')}")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="corp-card">', unsafe_allow_html=True)
            # Status Update
            new_status = st.selectbox("Assign Pipeline Stage", ["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], 
                                      index=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"].index(record.get('status', 'NEW')))
            
            notes = st.text_area("Internal Operations Notes", value=record.get("notes", ""))
            
            if st.button("💾 Synchronize Record Changes", type="primary", use_container_width=True):
                supabase.table("applicants").update({"status": new_status, "notes": notes}).eq("id", record["id"]).execute()
                st.cache_data.clear()
                st.success("Database synchronized successfully.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.checkbox("Enable Danger Zone"):
                if st.button("🗑 Permanently Remove Applicant"):
                    supabase.table("applicants").delete().eq("id", record["id"]).execute()
                    st.session_state.view_id = None
                    st.cache_data.clear()
                    st.rerun()

    else:
        st.markdown("""
        <div style="text-align: center; padding: 100px; color: #94A3B8; border: 2px dashed #E2E8F0; border-radius: 12px;">
            <div style="font-size: 40px; margin-bottom: 20px;">🏢</div>
            <h4>Vergecom Talent Management</h4>
            <p>Select an applicant from the pipeline on the left to view detailed diagnostics and technical qualifications.</p>
        </div>
        """, unsafe_allow_html=True)
