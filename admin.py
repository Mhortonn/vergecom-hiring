import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ── PAGE CONFIG (WIDE FOR DATA DENSITY) ──
st.set_page_config(page_title="Vergecom | Ops", page_icon="⚙️", layout="wide")

# ── DSI CORPORATE STYLING ──
st.markdown("""
<style>
    /* Use standard corporate sans-serif */
    html, body, [class*="st-"] { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .stApp { background-color: #F0F2F6; }
    
    /* Header Bar */
    .dsi-header {
        background-color: #00539B;
        color: white;
        padding: 10px 20px;
        margin-bottom: 20px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 20px;
    }

    /* Make the table look like a professional portal */
    div[data-testid="stDataFrame"] {
        background-color: white;
        border: 1px solid #C0C0C0;
        border-radius: 0px;
    }
</style>
<div class="dsi-header">Assign Technician - Contractor Portal</div>
""", unsafe_allow_html=True)

# ── SUPABASE AUTH ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── DATA FETCHING ──
@st.cache_data(ttl=2)
def get_ops_data():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

df = get_ops_data()

# ── FILTERS (DSI STYLE TOP BAR) ──
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1: search_name = st.text_input("Technician Name", placeholder="Search...")
    with c2: search_state = st.selectbox("State", ["All States"] + (sorted(df['state'].unique().tolist()) if not df.empty else []))
    with c3: search_status = st.selectbox("Order Status", ["All", "NEW", "REVIEWED", "HIRED"])
    with c4: st.write(""); st.button("Apply Filters", use_container_width=True)

st.markdown("---")

# ── MASTER DATA GRID (EVERYTHING DISPLAYED) ──
if not df.empty:
    # Filter Logic
    f_df = df.copy()
    if search_name:
        f_df = f_df[f_df['name'].str.contains(search_name, case=False, na=False)]
    if search_state != "All States":
        f_df = f_df[f_df['state'] == search_state]
    if search_status != "All":
        f_df = f_df[f_df['status'] == search_status]

    # Organize columns exactly like DSI screenshot
    # Info is displayed across the screen so no clicks are needed to see data
    display_df = f_df[['id', 'name', 'phone', 'state', 'counties', 'radius', 'experience', 'status', 'notes', 'created_at']]

    st.write(f"**Records Found:** {len(display_df)}")
    
    # ── THE DATA EDITOR (Click cells to change info instantly) ──
    edited_df = st.data_editor(
        display_df,
        use_container_width=True,
        height=600,
        hide_index=True,
        column_config={
            "id": None, # Hide ID from display
            "name": st.column_config.TextColumn("Technician Name", width="medium", required=True),
            "phone": "Contact Number",
            "state": "State",
            "counties": st.column_config.TextColumn("Operating Counties", width="large"),
            "radius": st.column_config.NumberColumn("Radius (mi)", format="%d"),
            "experience": "Exp Level",
            "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"]),
            "notes": st.column_config.TextColumn("Admin Notes", width="large"),
            "created_at": st.column_config.DatetimeColumn("Registration Date", format="MM/DD/YY"),
        }
    )

    # ── SYNC BUTTON (CLICK #2) ──
    # User clicks 'Apply Filters' then 'Sync'—that is it.
    col_sync, col_spacer = st.columns([1, 3])
    with col_sync:
        if st.button("💾 SYNC CHANGES TO DATABASE", type="primary", use_container_width=True):
            # Identify what changed
            for index, row in edited_df.iterrows():
                original_row = df[df['id'] == row['id']].iloc[0]
                # If status or notes changed, update Supabase
                if row['status'] != original_row['status'] or row['notes'] != original_row['notes']:
                    supabase.table("applicants").update({
                        "status": row['status'],
                        "notes": row['notes']
                    }).eq("id", row['id']).execute()
            
            st.success("System Synchronized.")
            st.cache_data.clear()
            st.rerun()

else:
    st.error("No data found in Supabase. Ensure your table columns match exactly.")
