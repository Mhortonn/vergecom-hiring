import streamlit as st
import pandas as pd
import textwrap  # <--- THIS IS THE MAGIC FIX
from datetime import datetime, timedelta

# ── Config ──
st.set_page_config(page_title="Vergecom | Hiring", page_icon="⚡", layout="wide")

# ── Supabase ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing Supabase credentials. Check .streamlit/secrets.toml")
    st.stop()

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Constants ──
STATUS_LIST = ["NEW", "REVIEWED", "CONTACTED", "INTERVIEW", "HIRED", "REJECTED"]
STATUS_COLORS = {
    "NEW": "blue", "REVIEWED": "purple", "CONTACTED": "amber",
    "INTERVIEW": "cyan", "HIRED": "green", "REJECTED": "red",
}

# ── Styles ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        --bg: #FAFBFC;
        --bg-white: #FFFFFF;
        --border: #E5E7EB;
        --accent: #2563EB;
        --text-1: #111827;
        --text-2: #4B5563;
        --text-3: #9CA3AF;
        --blue: #2563EB; --blue-bg: #EFF6FF;
        --green: #059669; --green-bg: #ECFDF5;
        --red: #DC2626; --red-bg: #FEF2F2;
        --amber: #D97706; --amber-bg: #FFFBEB;
        --purple: #7C3AED; --purple-bg: #F5F3FF;
        --cyan: #0891B2; --cyan-bg: #ECFEFF;
    }

    .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif !important; }
    .block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1200px !important; }

    /* Card & Grid Styles */
    .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 1rem 0 1.5rem; }
    .info-box { background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; }
    .info-box-title { font-family: 'IBM Plex Mono', monospace; font-weight: 600; color: var(--accent); margin-bottom: 12px; font-size: 0.75rem; letter-spacing: 0.05em; text-transform: uppercase; }
    .info-row { margin-bottom: 8px; }
    .info-label { font-size: 0.75rem; color: var(--text-3); }
    .info-value { font-size: 0.9rem; color: var(--text-1); font-weight: 500; }
    
    .ac-tag { background-color: var(--blue-bg); color: var(--blue); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; display: inline-block; margin: 0 4px 4px 0; }
    .s-badge { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; font-weight: 600; padding: 0.25rem 0.55rem; border-radius: 6px; display: inline-block; }

    /* List View Card */
    .applicant-card { background: var(--bg-white); border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.5rem; display: grid; grid-template-columns: 2fr 1fr 1.2fr 1.5fr 1.2fr 0.8fr; align-items: center; gap: 0.75rem; transition: all 0.15s; }
    .applicant-card:hover { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), 0 2px 8px rgba(37,99,235,0.06); }
    
    /* Text Helpers */
    .ac-name { font-size: 0.9rem; font-weight: 600; color: var(--text-1); }
    .ac-email { font-size: 0.75rem; color: var(--text-3); margin-top: 0.1rem; }
    .ac-phone { font-size: 0.82rem; color: var(--text-2); font-family: 'IBM Plex Mono', monospace; }
    
    /* Equipment Pills */
    .equip-pill { font-size: 0.65rem; font-weight: 500; padding: 0.2rem 0.45rem; border-radius: 4px; margin-right: 4px; }
    .equip-yes { background: var(--green-bg); color: var(--green); }
    .equip-no { background: var(--red-bg); color: var(--red); }

    /* Header & Tabs */
    .list-header { display: grid; grid-template-columns: 2fr 1fr 1.2fr 1.5fr 1.2fr 0.8fr; gap: 0.75rem; padding: 0.6rem 1.25rem; margin-bottom: 0.25rem; }
    .list-header-cell { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; font-weight: 600; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.06em; }
    .stTabs [data-baseweb="tab-list"] { gap: 0; background: var(--bg-white); border: 1px solid var(--border); border-radius: 10px; padding: 0.2rem; }
    .stTabs [data-baseweb="tab"] { font-size: 0.78rem; font-weight: 500; color: var(--text-3); border-radius: 8px; padding: 0.45rem 0.9rem; }
    .stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }
    div.stButton > button { font-weight: 600 !important; font-size: 0.82rem !important; border-radius: 8px !important; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ── DATA ──
@st.cache_data(ttl=5)
def load_applicants():
    # We select '*' to get ALL columns
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return res.data or []

def update_status(aid, s):
    supabase.table("applicants").update({"status": s}).eq("id", aid).execute()

def update_notes(aid, n):
    supabase.table("applicants").update({"notes": n}).eq("id", aid).execute()

def delete_applicant(aid):
    supabase.table("applicants").delete().eq("id", aid).execute()

if "view_id" not in st.session_state:
    st.session_state.view_id = None

# Sidebar
with st.sidebar:
    st.header("Admin Controls")
    if st.button("↻ Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # DEBUG MODE (Only check this if you have issues)
    show_debug = st.checkbox("Show Raw Data (Debug)")

data = load_applicants()

# ── HEADER ──
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;padding-bottom:1.5rem;border-bottom:1px solid #E5E7EB;">
    <div>
        <span style="font-size:1.25rem;font-weight:700;color:#111827;">Verge<span style="color:#2563EB;">com</span></span>
        <span style="margin:0 10px;color:#E5E7EB;">|</span>
        <span style="font-family:'IBM Plex Mono';font-size:0.65rem;font-weight:500;color:#9CA3AF;letter-spacing:0.08em;">HIRING DASHBOARD</span>
    </div>
    <div style="font-size:0.8rem;color:#9CA3AF;">{datetime.now().strftime("%B %d, %Y")} · {len(data)} applicants</div>
</div>
""", unsafe_allow_html=True)

# ── HELPERS ──
def badge(status):
    c = STATUS_COLORS.get(status, "blue")
    return f'<span class="s-badge" style="background:var(--{c}-bg);color:var(--{c});">{status}</span>'

def equip_html(rec):
    html = ""
    for k, l in [("vehicle","Vehicle"), ("ladder","Ladder"), ("insurance","Insured")]:
        is_yes = rec.get(k) == "Yes"
        cls = "equip-yes" if is_yes else "equip-no"
        sym = "✓" if is_yes else "✗"
        html += f'<span class="equip-pill {cls}">{sym} {l}</span>'
    return html

# ═══════════════════════════════════
#  DETAIL VIEW
# ═══════════════════════════════════
if st.session_state.view_id:
    record = next((r for r in data if str(r["id"]) == str(st.session_state.view_id)), None)

    if st.button("← Back to all applicants"):
        st.session_state.view_id = None
        st.rerun()

    if not record:
        st.error("Applicant not found")
        st.stop()

    if show_debug:
        st.warning("DEBUG MODE: Raw Database Record")
        st.json(record)

    # Exp Tags
    exp_tags = " ".join([f'<span class="ac-tag">{t.strip()}</span>' for t in record.get("exp_types","").split(",") if t.strip()]) if record.get("exp_types") != "None selected" else '<span style="color:#9CA3AF;font-size:0.8rem;">None</span>'
    
    # Data Extraction
    r_state = record.get('state') if record.get('state') else "Not Provided"
    r_radius = f"{record.get('radius')} mi" if record.get('radius') else ""
    r_counties = record.get('counties') if record.get('counties') else "Not Provided"

    # !!! CRITICAL FIX: textwrap.dedent() removes the indentation that was breaking the HTML !!!
    html_card = textwrap.dedent(f"""
    <div style="background:white;border:1px solid #E5E7EB;border-radius:14px;padding:1.75rem;margin-bottom:1rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:1.5rem;padding-bottom:1.25rem;border-bottom:1px solid #F0F1F3;">
            <div>
                <div style="font-size:1.5rem;font-weight:700;color:#111827;">{record['name']}</div>
                <div style="font-size:0.78rem;color:#9CA3AF;margin-top:0.25rem;">Applied {record.get('created_at','—')[:10]}</div>
            </div>
            <div>{badge(record.get('status','NEW'))}</div>
        </div>

        <div class="info-grid">
            
            <div class="info-box">
                <div class="info-box-title">Contact</div>
                <div class="info-row"><div class="info-label">Phone</div><div class="info-value">{record.get('phone','—')}</div></div>
                <div class="info-row"><div class="info-label">Email</div><div class="info-value">{record.get('email','—')}</div></div>
            </div>

            <div class="info-box">
                <div class="info-box-title">Coverage Area</div>
                <div class="info-row">
                    <div class="info-label">State / Radius</div>
                    <div class="info-value">{r_state} <span style="color:#9CA3AF;font-size:0.75rem;margin-left:5px;">{r_radius}</span></div>
                </div>
                <div class="info-row">
                    <div class="info-label">Counties</div>
                    <div class="info-value" style="font-size:0.8rem;line-height:1.4;">{r_counties}</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-title">Experience</div>
                <div class="info-row"><div class="info-label">Years</div><div class="info-value">{record.get('experience','—')}</div></div>
                <div class="info-row"><div class="info-label">Types</div><div style="margin-top:4px;">{exp_tags}</div></div>
            </div>

            <div class="info-box">
                <div class="info-box-title">Equipment</div>
                <div style="margin-top:8px;">{equip_html(record)}</div>
            </div>
        </div>
    </div>
    """)

    # Render
    st.markdown(html_card, unsafe_allow_html=True)

    # Photos
    p1, p2 = record.get("photo1_url"), record.get("photo2_url")
    if p1 or p2:
        st.markdown('<div class="info-box-title" style="margin:1rem 0 0.5rem;">PHOTOS</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if p1: c1.image(p1, use_container_width=True)
        if p2: c2.image(p2, use_container_width=True)

    # Actions
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        new_status = st.selectbox("Update Status", STATUS_LIST, index=STATUS_LIST.index(record.get("status","NEW")))
        if st.button("Save Status", type="primary", use_container_width=True):
            update_status(record["id"], new_status)
            st.cache_data.clear()
            st.rerun()
    with c2:
        notes = st.text_area("Notes", record.get("notes","") or "", height=100)
        if st.button("Save Notes", use_container_width=True):
            update_notes(record["id"], notes)
            st.cache_data.clear()
            st.success("Saved")

    st.markdown("---")
    if st.button("🗑 Delete Applicant"):
        delete_applicant(record["id"])
        st.cache_data.clear()
        st.session_state.view_id = None
        st.rerun()

    st.stop()

# ═══════════════════════════════════
#  LIST VIEW
# ═══════════════════════════════════

# KPIs
new_c = sum(1 for d in data if d.get("status")=="NEW")
tot_c = len(data)
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi"><div class="kpi-label">Total</div><div class="kpi-num">{tot_c}</div></div>
    <div class="kpi"><div class="kpi-label">New</div><div class="kpi-num">{new_c}</div></div>
    <div class="kpi"><div class="kpi-label">Contacted</div><div class="kpi-num">{sum(1 for d in data if d.get("status")=="CONTACTED")}</div></div>
</div>
""", unsafe_allow_html=True)

# Filters
c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
with c1: search = st.text_input("Search", placeholder="Name or Phone...", label_visibility="collapsed")
with c2: status_f = st.multiselect("Status", STATUS_LIST, placeholder="Status", label_visibility="collapsed")
with c3: state_f = st.multiselect("State", sorted(list(set(d.get("state","") for d in data if d.get("state")))), placeholder="State", label_visibility="collapsed")
with c4:
    if data: st.download_button("Export CSV", pd.DataFrame(data).to_csv(index=False), "applicants.csv", "text/csv", use_container_width=True)

# Apply Filters
filtered = data
if search: filtered = [d for d in filtered if search.lower() in d.get("name","").lower()]
if status_f: filtered = [d for d in filtered if d.get("status") in status_f]
if state_f: filtered = [d for d in filtered if d.get("state") in state_f]

# Tabs
tabs = st.tabs([f"All ({len(filtered)})", "New", "Contacted", "Interview", "Hired", "Rejected"])
cat_list = [None, "NEW", "CONTACTED", "INTERVIEW", "HIRED", "REJECTED"]

for i, tab in enumerate(tabs):
    with tab:
        cat_data = filtered if cat_list[i] is None else [d for d in filtered if d.get("status") == cat_list[i]]
        
        if not cat_data:
            st.info("No applicants found.")
        else:
            st.markdown("""
            <div class="list-header">
                <div class="list-header-cell">Applicant</div>
                <div class="list-header-cell">Location</div>
                <div class="list-header-cell">Phone</div>
                <div class="list-header-cell">Experience</div>
                <div class="list-header-cell">Equipment</div>
                <div class="list-header-cell">Date</div>
            </div>
            """, unsafe_allow_html=True)

            for app in cat_data:
                # Truncate tags for list view
                exp_short = ""
                if app.get("exp_types") and app.get("exp_types") != "None selected":
                    tags = app.get("exp_types").split(",")
                    exp_short = "".join([f'<span class="ac-tag">{t.strip()}</span>' for t in tags[:2]])
                
                # HTML Card
                html_list = textwrap.dedent(f"""
                <div class="applicant-card">
                    <div>
                        <div class="ac-name">{app.get("name","—")}</div>
                        <div class="ac-email">{app.get("email","")} &nbsp;{badge(app.get("status","NEW"))}</div>
                    </div>
                    <div>
                        <div style="font-weight:500;font-size:0.8rem;color:#111827;">{app.get("state","—")}</div>
                        <div style="font-size:0.7rem;color:#9CA3AF;">{app.get("radius","—")} mi</div>
                    </div>
                    <div class="ac-phone">{app.get("phone","—")}</div>
                    <div>
                        <div class="ac-exp">{app.get("experience","—")}</div>
                        <div style="margin-top:2px;">{exp_short}</div>
                    </div>
                    <div style="display:flex;">{equip_html(app)}</div>
                    <div style="font-family:'IBM Plex Mono';font-size:0.7rem;color:#9CA3AF;">{app.get("created_at","")[:10]}</div>
                </div>
                """)
                st.markdown(html_list, unsafe_allow_html=True)

                if st.button("View", key=f"btn_{cat_list[i] or 'all'}_{app['id']}", use_container_width=True):
                    st.session_state.view_id = app["id"]
                    st.rerun()
