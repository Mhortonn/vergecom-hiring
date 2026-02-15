import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ── Config ──
st.set_page_config(page_title="Vergecom | Hiring", page_icon="⚡", layout="wide")

# ── Supabase ──
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials missing. Add them in Settings → Secrets.")
    st.stop()

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Constants ──
STATUS_LIST = ["NEW", "REVIEWED", "CONTACTED", "INTERVIEW", "HIRED", "REJECTED"]
STATUS_COLORS = {
    "NEW": "#3B82F6", "REVIEWED": "#8B5CF6", "CONTACTED": "#F59E0B",
    "INTERVIEW": "#06B6D4", "HIRED": "#22C55E", "REJECTED": "#EF4444",
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
        --green: #059669;
        --green-bg: #ECFDF5;
        --red: #DC2626;
        --red-bg: #FEF2F2;
        --blue: #2563EB;
        --blue-bg: #EFF6FF;
    }

    .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif !important; }
    .block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1200px !important; }

    /* ─── CUSTOM CARD STYLES ─── */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .info-box {
        background-color: #f8f9fa; /* Light Gray Background */
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
    }
    .info-box-title {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        color: var(--accent);
        margin-bottom: 12px;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }
    .info-row {
        margin-bottom: 8px;
    }
    .info-label {
        font-size: 0.75rem;
        color: var(--text-3);
        margin-bottom: 2px;
    }
    .info-value {
        font-size: 0.9rem;
        color: var(--text-1);
        font-weight: 500;
        line-height: 1.4;
    }
    .ac-tag {
        background-color: var(--blue-bg);
        color: var(--blue);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    /* ──────────────────────────────────── */

    /* ── Header ── */
    .dash-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
    .dash-brand { display: flex; align-items: center; gap: 0.75rem; }
    .dash-logo { font-family: 'DM Sans', sans-serif; font-size: 1.25rem; font-weight: 700; color: var(--text-1); }
    .dash-logo span { color: var(--accent); }
    .dash-sep { width: 1px; height: 20px; background: var(--border); }
    .dash-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; font-weight: 500; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.08em; }
    .dash-date { font-size: 0.8rem; color: var(--text-3); }

    /* ── KPIs ── */
    .kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.75rem; margin-bottom: 1.5rem; }
    .kpi { background: var(--bg-white); border: 1px solid var(--border); border-radius: 12px; padding: 1.1rem 1rem; }
    .kpi-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; font-weight: 500; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.35rem; }
    .kpi-num { font-size: 1.75rem; font-weight: 700; color: var(--text-1); line-height: 1; }
    .kpi-sub { font-size: 0.68rem; font-weight: 500; margin-top: 0.2rem; }
    .kpi-sub.green { color: var(--green); }

    /* ── Applicant Card (List View) ── */
    .applicant-card { background: var(--bg-white); border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.5rem; display: grid; grid-template-columns: 2fr 1fr 1.2fr 1.5fr 1.2fr 0.8fr; align-items: center; gap: 0.75rem; transition: all 0.15s; }
    .applicant-card:hover { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), 0 2px 8px rgba(37,99,235,0.06); }
    .ac-name { font-size: 0.9rem; font-weight: 600; color: var(--text-1); }
    .ac-email { font-size: 0.75rem; color: var(--text-3); margin-top: 0.1rem; }
    .ac-location { font-size: 0.8rem; color: var(--text-1); font-weight: 500; }
    .ac-radius { font-size: 0.7rem; color: var(--text-3); }
    .ac-phone { font-size: 0.82rem; color: var(--text-2); font-family: 'IBM Plex Mono', monospace; }
    .ac-exp { font-size: 0.8rem; color: var(--text-2); }
    
    /* Equipment Pills */
    .equip-pill { font-size: 0.65rem; font-weight: 500; padding: 0.2rem 0.45rem; border-radius: 4px; margin-right: 0.25rem; }
    .equip-yes { background: var(--green-bg); color: var(--green); }
    .equip-no { background: var(--red-bg); color: var(--red); }
    
    .ac-date { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: var(--text-3); }
    .s-badge { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; font-weight: 600; padding: 0.25rem 0.55rem; border-radius: 6px; display: inline-block; }

    /* ── Detail View Wrapper ── */
    .detail-card { background: var(--bg-white); border: 1px solid var(--border); border-radius: 14px; padding: 1.75rem; margin-bottom: 1rem; }
    .detail-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; padding-bottom: 1.25rem; border-bottom: 1px solid #F0F1F3; }
    .detail-name { font-size: 1.5rem; font-weight: 700; color: var(--text-1); }
    .detail-applied { font-size: 0.78rem; color: var(--text-3); margin-top: 0.25rem; }

    /* ── List Header ── */
    .list-header { display: grid; grid-template-columns: 2fr 1fr 1.2fr 1.5fr 1.2fr 0.8fr; gap: 0.75rem; padding: 0.6rem 1.25rem; margin-bottom: 0.25rem; }
    .list-header-cell { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; font-weight: 600; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.06em; }

    /* ── Streamlit UI Fixes ── */
    .stTabs [data-baseweb="tab-list"] { gap: 0; background: var(--bg-white); border: 1px solid var(--border); border-radius: 10px; padding: 0.2rem; }
    .stTabs [data-baseweb="tab"] { font-size: 0.78rem; font-weight: 500; color: var(--text-3); border-radius: 8px; padding: 0.45rem 0.9rem; }
    .stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }
    div.stButton > button { font-weight: 600 !important; font-size: 0.82rem !important; border-radius: 8px !important; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ── DATA ──
@st.cache_data(ttl=5) # Fast refresh
def load_applicants():
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

# Sidebar Refresh
with st.sidebar:
    if st.button("↻ Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

data = load_applicants()

# ── HEADER ──
st.markdown(f"""
<div class="dash-header">
    <div class="dash-brand">
        <div class="dash-logo">Verge<span>com</span></div>
        <div class="dash-sep"></div>
        <div class="dash-label">Hiring Dashboard</div>
    </div>
    <div class="dash-date">{datetime.now().strftime("%B %d, %Y")} &middot; {len(data)} applicants</div>
</div>
""", unsafe_allow_html=True)

# ── HELPERS ──
def fmt_date(iso_str):
    try: return datetime.fromisoformat(iso_str.replace("Z", "+00:00")).strftime("%b %d, %Y")
    except: return "—"

def fmt_date_short(iso_str):
    try: return datetime.fromisoformat(iso_str.replace("Z", "+00:00")).strftime("%b %d")
    except: return "—"

def status_badge_html(status):
    c = STATUS_COLORS.get(status, "#3B82F6")
    bg_map = {"NEW": "blue", "REVIEWED": "purple", "CONTACTED": "amber", "INTERVIEW": "cyan", "HIRED": "green", "REJECTED": "red"}
    bg_key = bg_map.get(status, "blue")
    return f'<span class="s-badge" style="background:var(--{bg_key}-bg);color:var(--{bg_key});">{status}</span>'

def equip_html(record):
    items = []
    for key, label in [("vehicle", "Vehicle"), ("ladder", "Ladder"), ("insurance", "Insured")]:
        val = record.get(key, "No")
        cls = "equip-yes" if val == "Yes" else "equip-no"
        sym = "✓" if val == "Yes" else "✗"
        items.append(f'<span class="equip-pill {cls}">{sym} {label}</span>')
    return "".join(items)

# ═══════════════════════════════════
#  DETAIL VIEW
# ═══════════════════════════════════
if st.session_state.view_id is not None:
    # Get the specific applicant record
    record = next((r for r in data if str(r["id"]) == str(st.session_state.view_id)), None)

    if st.button("← Back to all applicants"):
        st.session_state.view_id = None
        st.rerun()

    if not record:
        st.error("Applicant not found.")
        st.stop()

    s = record.get("status", "NEW")
    
    # --- PREPARE DATA FOR HTML ---
    exp_types = record.get("exp_types", "")
    if exp_types and exp_types != "None selected":
        exp_tags_html = " ".join(f'<span class="ac-tag">{t.strip()}</span>' for t in exp_types.split(","))
    else:
        exp_tags_html = '<span style="color:var(--text-3);font-size:0.82rem;">None listed</span>'
    
    equip_badges_html = equip_html(record)
    state = record.get("state", "—")
    counties = record.get("counties", "—")
    radius = record.get("radius", "—")

    # --- HTML CONTENT CONSTRUCTION ---
    html_card = f"""
    <div class="detail-card">
        <div class="detail-top">
            <div>
                <div class="detail-name">{record.get("name", "—")}</div>
                <div class="detail-applied">Applied {fmt_date(record.get("created_at", ""))}</div>
            </div>
            <div>{status_badge_html(s)}</div>
        </div>

        <div class="info-grid">
            <div class="info-box">
                <div class="info-box-title">Contact</div>
                <div class="info-row">
                    <div class="info-label">Phone</div>
                    <div class="info-value">{record.get("phone", "—")}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Email</div>
                    <div class="info-value">{record.get("email") or "—"}</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-title">Coverage Area</div>
                <div class="info-row">
                    <div class="info-label">State / Radius</div>
                    <div class="info-value">{state} &nbsp;<span style="color:var(--text-3);font-size:0.75rem;">({radius} mi)</span></div>
                </div>
                <div class="info-row">
                    <div class="info-label">Counties</div>
                    <div class="info-value" style="font-size:0.8rem;line-height:1.4;">{counties}</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-title">Experience</div>
                <div class="info-row">
                    <div class="info-label">Years</div>
                    <div class="info-value">{record.get("experience", "—")}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Types</div>
                    <div style="margin-top:6px;">{exp_tags_html}</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-title">Equipment</div>
                <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.5rem;">
                    {equip_badges_html}
                </div>
            </div>
        </div>
    </div>
    """

    st.markdown(html_card, unsafe_allow_html=True)

    # --- PHOTOS SECTION ---
    p1 = record.get("photo1_url", "")
    p2 = record.get("photo2_url", "")
    if p1 or p2:
        st.markdown('<div class="sec-title" style="margin-top:1rem;margin-bottom:0.5rem;font-size:0.7rem;font-weight:600;color:#9CA3AF;text-transform:uppercase;">Install Photos</div>', unsafe_allow_html=True)
        pcol1, pcol2 = st.columns(2)
        if p1:
            with pcol1: st.image(p1, use_container_width=True)
        if p2:
            with pcol2: st.image(p2, use_container_width=True)

    # --- ACTIONS SECTION ---
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title" style="margin-bottom:0.5rem;font-size:0.7rem;font-weight:600;color:#9CA3AF;text-transform:uppercase;">Actions</div>', unsafe_allow_html=True)
    
    act_col1, act_col2 = st.columns([1, 2])
    with act_col1:
        current_idx = STATUS_LIST.index(s) if s in STATUS_LIST else 0
        new_status = st.selectbox("Update Status", STATUS_LIST, index=current_idx, key="d_status")
        if st.button("Save Status", type="primary", use_container_width=True):
            update_status(record["id"], new_status)
            st.cache_data.clear()
            st.success("Updated!")
            st.rerun()

    with act_col2:
        current_notes = record.get("notes", "") or ""
        notes = st.text_area("Hiring Notes", value=current_notes, height=105, key="d_notes", placeholder="Add private notes...")
        if st.button("Save Notes", use_container_width=True):
            update_notes(record["id"], notes)
            st.cache_data.clear()
            st.success("Notes saved")
            st.rerun()

    st.markdown("---")
    if st.button("🗑 Delete Applicant", use_container_width=True):
        delete_applicant(record["id"])
        st.cache_data.clear()
        st.session_state.view_id = None
        st.rerun()

    st.stop()


# ═══════════════════════════════════
#  DASHBOARD (LIST VIEW)
# ═══════════════════════════════════

# KPIs
total = len(data)
new_ct = sum(1 for d in data if d.get("status") == "NEW")
contacted_ct = sum(1 for d in data if d.get("status") == "CONTACTED")
interview_ct = sum(1 for d in data if d.get("status") == "INTERVIEW")
hired_ct = sum(1 for d in data if d.get("status") == "HIRED")
recent_ct = 0
for d in data:
    try:
        dt = datetime.fromisoformat(d.get("created_at", "").replace("Z", "+00:00"))
        if dt > datetime.now(dt.tzinfo) - timedelta(days=7):
            recent_ct += 1
    except:
        pass

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi"><div class="kpi-label">Total</div><div class="kpi-num">{total}</div><div class="kpi-sub muted">all time</div></div>
    <div class="kpi"><div class="kpi-label">New</div><div class="kpi-num">{new_ct}</div><div class="kpi-sub green">+{recent_ct} this week</div></div>
    <div class="kpi"><div class="kpi-label">Contacted</div><div class="kpi-num">{contacted_ct}</div><div class="kpi-sub muted">pipeline</div></div>
    <div class="kpi"><div class="kpi-label">Interview</div><div class="kpi-num">{interview_ct}</div><div class="kpi-sub muted">scheduled</div></div>
    <div class="kpi"><div class="kpi-label">Hired</div><div class="kpi-num">{hired_ct}</div><div class="kpi-sub green">active</div></div>
</div>
""", unsafe_allow_html=True)

# Filters
f1, f2, f3, f4, f5 = st.columns([2, 1, 1, 1, 0.8])
with f1: search = st.text_input("Search", key="search", label_visibility="collapsed", placeholder="Search by name...")
with f2: status_filter = st.multiselect("Status", STATUS_LIST, default=[], key="sf", placeholder="Status")
with f3: state_filter = st.multiselect("State", sorted(list(set(d.get("state", "") for d in data if d.get("state")))), default=[], key="stf", placeholder="State")
with f4: exp_filter = st.multiselect("Experience", ["Starlink", "DirecTV", "Low Voltage"], default=[], key="ef", placeholder="Exp Type")
with f5: 
    if data:
        st.download_button("Export CSV", pd.DataFrame(data).to_csv(index=False).encode("utf-8"), "applicants.csv", "text/csv", use_container_width=True)

# Filter Logic
filtered = data
if search: filtered = [d for d in filtered if search.lower() in d.get("name", "").lower()]
if status_filter: filtered = [d for d in filtered if d.get("status") in status_filter]
if state_filter: filtered = [d for d in filtered if d.get("state") in state_filter]
if exp_filter: filtered = [d for d in filtered if any(e in d.get("exp_types", "") for e in exp_filter)]

# Tabs
tabs = st.tabs([f"All ({len(filtered)})", "New", "Contacted", "Interview", "Hired", "Rejected"])
statuses = [None, "NEW", "CONTACTED", "INTERVIEW", "HIRED", "REJECTED"]

for i, tab in enumerate(tabs):
    with tab:
        subset = filtered if statuses[i] is None else [d for d in filtered if d.get("status") == statuses[i]]
        
        if not subset:
            st.markdown('<div style="text-align:center;padding:3rem;color:#9CA3AF;border:1px dashed #E5E7EB;border-radius:12px;">No applicants found</div>', unsafe_allow_html=True)
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

            for app in subset:
                rad = f"{app.get('radius')} mi" if app.get("radius") else ""
                
                # Render list items as simple strings inside Python to avoid complexity
                exp_list_tags = ""
                if app.get("exp_types") and app.get("exp_types") != "None selected":
                    tags = [t.strip() for t in app.get("exp_types").split(",")]
                    exp_list_tags = "".join(f'<span class="ac-tag">{t}</span>' for t in tags[:3]) # Limit to 3 tags in list view

                st.markdown(f"""
                <div class="applicant-card">
                    <div>
                        <div class="ac-name">{app.get("name", "—")}</div>
                        <div class="ac-email">{app.get("email") or ""} &nbsp;{status_badge_html(app.get("status", "NEW"))}</div>
                    </div>
                    <div>
                        <div class="ac-location">{app.get("state", "—")}</div>
                        <div class="ac-radius">{rad}</div>
                    </div>
                    <div class="ac-phone">{app.get("phone", "—")}</div>
                    <div>
                        <div class="ac-exp">{app.get("experience", "—")}</div>
                        <div style="margin-top:0.2rem;">{exp_list_tags}</div>
                    </div>
                    <div style="display:flex;">{equip_html(app)}</div>
                    <div class="ac-date">{fmt_date_short(app.get("created_at", ""))}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # --- UNIQUE KEY FIX ---
                # We use 'i' (tab index) AND 'app[id]' to ensure every button is unique
                if st.button(f"View Details", key=f"btn_{i}_{app['id']}", use_container_width=True):
                    st.session_state.view_id = app["id"]
                    st.rerun()
