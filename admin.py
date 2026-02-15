import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (Enterprise Grade) ──
st.set_page_config(page_title="Vergecom | Operations Center", page_icon="🏢", layout="wide")

# ── CORPORATE STYLE SHEET (Refined SaaS UI) ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background */
    .stApp {
        background-color: #F1F5F9;
    }

    /* Professional Metric Tiles */
    .metric-tile {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        text-align: left;
    }
    .metric-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
    }

    /* Corporate Table Header */
    .table-header {
        background-color: #F8FAFC;
        padding: 10px 15px;
        border-radius: 8px 8px 0 0;
        border: 1px solid #E2E8F0;
        border-bottom: none;
    }

    /* Status Badge Colors */
    .status-badge {
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-new { background-color: #DBEAFE; color: #1E40AF; }
    .status-reviewed { background-color: #F3E8FF; color: #6B21A8; }
    .status-active { background-color: #DCFCE7; color: #166534; }

    /* Hide standard Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SUPABASE INTEGRATION ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data(ttl=5)
def fetch_master_data():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

df = fetch_master_data()

# ── HEADER & KPI STRIP ──
st.markdown(f"### 🏢 Vergecom Tech Operations Manager")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f'<div class="metric-tile"><div class="metric-label">Total Technicians</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)
with kpi2:
    new_leads = len(df[df['status'] == 'NEW']) if 'status' in df.columns else 0
    st.markdown(f'<div class="metric-tile"><div class="metric-label">Unassigned Leads</div><div class="metric-value" style="color:#2563EB;">{new_leads}</div></div>', unsafe_allow_html=True)
with kpi3:
    fl_count = len(df[df['state'] == 'Florida']) if 'state' in df.columns else 0
    st.markdown(f'<div class="metric-tile"><div class="metric-label">FL Region Load</div><div class="metric-value">{fl_count}</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="metric-tile"><div class="metric-label">System Date</div><div class="metric-value" style="font-size:1.1rem; padding-top:10px;">{datetime.now().strftime("%m/%d/%Y")}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── SEARCH & FILTER CONTROLS ──
col_search, col_filter, col_export = st.columns([2, 1, 1])
with col_search:
    query = st.text_input("Search Registry", placeholder="Search by name, phone, or county...", label_visibility="collapsed")
with col_filter:
    status_filter = st.selectbox("Order Status", ["All States", "NEW", "REVIEWED", "CONTACTED", "HIRED"], label_visibility="collapsed")
with col_export:
    if not df.empty:
        st.download_button("📤 Export CSV", df.to_csv(index=False).encode('utf-8'), "vergecom_techs.csv", "text/csv", use_container_width=True)

# ── DATA GRID (The "DSI Style" Table) ──
if not df.empty:
    # Filter the dataframe based on search
    filtered_df = df.copy()
    if query:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(query, case=False, na=False) |
            filtered_df['phone'].str.contains(query, case=False, na=False) |
            filtered_df['counties'].str.contains(query, case=False, na=False)
        ]
    
    # Selecting columns to display similar to your provided DSI screenshot
    display_cols = ['name', 'phone', 'state', 'counties', 'radius', 'experience', 'status', 'created_at']
    available_cols = [c for c in display_cols if c in filtered_df.columns]
    
    # Create the modern interactive table
    st.dataframe(
        filtered_df[available_cols],
        use_container_width=True,
        column_config={
            "name": "Technician Name",
            "phone": "Contact Info",
            "state": "State",
            "counties": "Operating Counties",
            "radius": st.column_config.NumberColumn("Radius (mi)", format="%d"),
            "status": "Current Status",
            "created_at": st.column_config.DatetimeColumn("Registered", format="MM/DD/YYYY"),
        },
        hide_index=True
    )

    # ── ACTION PANEL (Split View) ──
    st.markdown("#### Registry Details & Record Updates")
    selected_name = st.selectbox("Select technician to modify record:", filtered_df['name'].unique())
    
    if selected_name:
        record = filtered_df[filtered_df['name'] == selected_name].iloc[0]
        c1, c2, c3 = st.columns([1, 1, 1.5])
        
        with c1:
            st.info(f"**Technician:** {record['name']}\n\n**Email:** {record['email']}\n\n**Phone:** {record['phone']}")
        with c2:
            st.success(f"**Territory:** {record['state']}\n\n**Counties:** {record['counties']}\n\n**Coverage:** {record['radius']} mi")
        with c3:
            new_status = st.selectbox("Assign Pipeline Stage", ["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], 
                                      index=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"].index(record.get('status', 'NEW')))
            new_notes = st.text_area("Operations Notes", value=record.get('notes', ''))
            
            if st.button("💾 Synchronize Record Changes", type="primary", use_container_width=True):
                supabase.table("applicants").update({"status": new_status, "notes": new_notes}).eq("id", record["id"]).execute()
                st.cache_data.clear()
                st.rerun()

else:
    st.warning("No technician records found in the Supabase Cloud database.")
