import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(page_title="Vergecom Admin | Hiring Dashboard", page_icon="⚡", layout="wide")

# --- SUPABASE ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Supabase credentials missing.")
    st.stop()

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- STATUS CONFIG ---
STATUS_OPTIONS = ["NEW", "REVIEWED", "CONTACTED", "INTERVIEW", "HIRED", "REJECTED"]
STATUS_COLORS = {
    "NEW": "#3B82F6",
    "REVIEWED": "#A855F7",
    "CONTACTED": "#F59E0B",
    "INTERVIEW": "#06B6D4",
    "HIRED": "#22C55E",
    "REJECTED": "#EF4444",
}

# --- STYLES ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Sora:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #060608;
        --bg-card: #0D0D10;
        --bg-elevated: #131317;
        --bg-input: #0F0F13;
        --border: #1C1C22;
        --border-mid: #28282F;
        --accent: #3B82F6;
        --accent-bright: #60A5FA;
        --glow: rgba(59,130,246,0.12);
        --text-1: #F0F0F3;
        --text-2: #9CA3AF;
        --text-3: #6B7280;
        --text-4: #3F3F46;
        --green: #22C55E;
        --amber: #F59E0B;
        --red: #EF4444;
        --purple: #A855F7;
        --cyan: #06B6D4;
        --r-sm: 8px;
        --r-md: 12px;
        --r-lg: 16px;
        --r-xl: 20px;
    }

    .stApp {
        background: var(--bg);
        font-family: 'Sora', sans-serif;
        color: var(--text-1);
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 1280px !important;
    }

    /* ── TOP BAR ── */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid var(--border);
    }
    .top-bar-left { display: flex; align-items: center; gap: 1rem; }
    .top-bar-logo {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-1);
        letter-spacing: -0.02em;
    }
    .top-bar-logo span { color: var(--accent); }
    .top-bar-divider { width: 1px; height: 24px; background: var(--border-mid); }
    .top-bar-page {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 500;
        color: var(--text-3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .top-bar-right {
        font-size: 0.75rem;
        color: var(--text-3);
    }

    /* ── STAT CARDS ── */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.75rem;
    }
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-lg);
        padding: 1.2rem 1rem;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
    }
    .stat-card.blue::before { background: var(--accent); }
    .stat-card.green::before { background: var(--green); }
    .stat-card.amber::before { background: var(--amber); }
    .stat-card.purple::before { background: var(--purple); }
    .stat-card.cyan::before { background: var(--cyan); }
    .stat-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.58rem;
        font-weight: 500;
        color: var(--text-3);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }
    .stat-num {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-1);
        line-height: 1;
    }
    .stat-delta {
        font-size: 0.65rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    .stat-delta.up { color: var(--green); }
    .stat-delta.neutral { color: var(--text-3); }

    /* ── FILTERS BAR ── */
    .filter-bar {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-lg);
        padding: 1rem 1.25rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .filter-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: var(--text-3);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-right: 0.5rem;
        white-space: nowrap;
    }

    /* ── TABLE CARD ── */
    .table-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-xl);
        overflow: hidden;
        margin-bottom: 1.5rem;
    }
    .table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border);
    }
    .table-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-1);
    }
    .table-count {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-3);
        background: var(--bg-elevated);
        padding: 0.2rem 0.6rem;
        border-radius: 100px;
        border: 1px solid var(--border);
    }

    /* ── APPLICANT ROW ── */
    .app-row {
        display: grid;
        grid-template-columns: 2fr 1.2fr 1.5fr 1fr 1fr 0.8fr;
        align-items: center;
        padding: 0.9rem 1.5rem;
        border-bottom: 1px solid var(--border);
        transition: background 0.15s;
        cursor: pointer;
    }
    .app-row:hover { background: rgba(59,130,246,0.03); }
    .app-row:last-child { border-bottom: none; }

    .app-name {
        font-weight: 500;
        font-size: 0.88rem;
        color: var(--text-1);
    }
    .app-sub {
        font-size: 0.72rem;
        color: var(--text-3);
        margin-top: 0.1rem;
    }
    .app-cell {
        font-size: 0.8rem;
        color: var(--text-2);
    }
    .app-cell-mono {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-3);
    }

    .status-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 0.25rem 0.6rem;
        border-radius: 100px;
        display: inline-block;
        text-transform: uppercase;
    }

    /* ── DETAIL PANEL ── */
    .detail-panel {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-xl);
        padding: 2rem;
        margin-bottom: 1.25rem;
    }
    .detail-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    .detail-name {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-1);
        letter-spacing: -0.02em;
    }
    .detail-meta {
        font-size: 0.78rem;
        color: var(--text-3);
        margin-top: 0.3rem;
    }
    .detail-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.25rem;
        margin-bottom: 1.5rem;
    }
    .detail-section {
        background: var(--bg-elevated);
        border: 1px solid var(--border);
        border-radius: var(--r-md);
        padding: 1.25rem;
    }
    .detail-section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.58rem;
        font-weight: 600;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    .detail-field {
        margin-bottom: 0.6rem;
    }
    .detail-field:last-child { margin-bottom: 0; }
    .detail-field-label {
        font-size: 0.68rem;
        color: var(--text-3);
        margin-bottom: 0.15rem;
    }
    .detail-field-value {
        font-size: 0.88rem;
        color: var(--text-1);
        font-weight: 500;
    }

    .equip-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        font-size: 0.75rem;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        margin: 0.15rem 0.15rem 0.15rem 0;
    }
    .equip-yes {
        background: rgba(34,197,94,0.08);
        color: #4ADE80;
        border: 1px solid rgba(34,197,94,0.15);
    }
    .equip-no {
        background: rgba(239,68,68,0.06);
        color: #F87171;
        border: 1px solid rgba(239,68,68,0.12);
    }

    .exp-tag {
        display: inline-block;
        font-size: 0.72rem;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        background: rgba(59,130,246,0.08);
        color: var(--accent-bright);
        border: 1px solid rgba(59,130,246,0.12);
        margin: 0.15rem 0.15rem 0.15rem 0;
    }

    .photo-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-top: 0.5rem;
    }
    .photo-grid img {
        width: 100%;
        border-radius: var(--r-md);
        border: 1px solid var(--border);
    }

    /* ── FORM OVERRIDES ── */
    .stSelectbox div[data-baseweb="select"] > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-mid) !important;
        border-radius: var(--r-sm) !important;
        color: var(--text-1) !important;
        font-size: 0.82rem !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-mid) !important;
        border-radius: var(--r-sm) !important;
        color: var(--text-1) !important;
        font-size: 0.85rem !important;
    }
    label { color: var(--text-2) !important; font-size: 0.78rem !important; }
    .stMultiSelect div[data-baseweb="select"] > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-mid) !important;
        border-radius: var(--r-sm) !important;
    }

    div.stButton > button {
        font-family: 'Sora', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        border-radius: var(--r-sm) !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s !important;
    }

    .stDownloadButton > button {
        background: var(--bg-elevated) !important;
        color: var(--text-2) !important;
        border: 1px solid var(--border-mid) !important;
        border-radius: var(--r-sm) !important;
        font-size: 0.78rem !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--text-1) !important;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-md);
        padding: 0.25rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Sora', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--text-3);
        border-radius: var(--r-sm);
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: var(--bg-elevated) !important;
        color: var(--text-1) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: var(--text-3);
    }
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.3;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# ── DATA ──
@st.cache_data(ttl=30)
def load_applicants():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return res.data if res.data else []


def update_status(applicant_id, new_status):
    supabase.table("applicants").update({"status": new_status}).eq("id", applicant_id).execute()


def update_notes(applicant_id, notes):
    supabase.table("applicants").update({"notes": notes}).eq("id", applicant_id).execute()


def delete_applicant(applicant_id):
    supabase.table("applicants").delete().eq("id", applicant_id).execute()


# ── SESSION ──
if "view_id" not in st.session_state:
    st.session_state.view_id = None

data = load_applicants()

# ── TOP BAR ──
st.markdown(f"""
<div class="top-bar">
    <div class="top-bar-left">
        <div class="top-bar-logo">Verge<span>com</span></div>
        <div class="top-bar-divider"></div>
        <div class="top-bar-page">Hiring Dashboard</div>
    </div>
    <div class="top-bar-right">{datetime.now().strftime("%B %d, %Y")} · {len(data)} applicants</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
#  DETAIL VIEW
# ══════════════════════════════════════
if st.session_state.view_id is not None:
    record = next((r for r in data if str(r["id"]) == str(st.session_state.view_id)), None)

    if st.button("← Back to all applicants"):
        st.session_state.view_id = None
        st.rerun()

    if not record:
        st.error("Applicant not found.")
        st.stop()

    # Header
    s_color = STATUS_COLORS.get(record.get("status", "NEW"), "#3B82F6")
    created = record.get("created_at", "")
    if created:
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            created_fmt = dt.strftime("%b %d, %Y at %I:%M %p")
        except:
            created_fmt = created
    else:
        created_fmt = "—"

    st.markdown(f"""
    <div class="detail-panel">
        <div class="detail-header">
            <div>
                <div class="detail-name">{record.get("name", "—")}</div>
                <div class="detail-meta">Applied {created_fmt}</div>
            </div>
            <span class="status-badge" style="background:{s_color}18;color:{s_color};border:1px solid {s_color}30;">
                {record.get("status", "NEW")}
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Info grid
    exp_types = record.get("exp_types", "")
    exp_tags = ""
    if exp_types and exp_types != "None selected":
        for t in exp_types.split(", "):
            exp_tags += f'<span class="exp-tag">{t.strip()}</span>'
    else:
        exp_tags = '<span style="color:var(--text-3);font-size:0.8rem;">None listed</span>'

    def equip_tag(val, label):
        if val == "Yes":
            return f'<span class="equip-tag equip-yes">✓ {label}</span>'
        return f'<span class="equip-tag equip-no">✗ {label}</span>'

    st.markdown(f"""
        <div class="detail-grid">
            <div class="detail-section">
                <div class="detail-section-title">// Contact</div>
                <div class="detail-field">
                    <div class="detail-field-label">Phone</div>
                    <div class="detail-field-value">{record.get("phone", "—")}</div>
                </div>
                <div class="detail-field">
                    <div class="detail-field-label">Email</div>
                    <div class="detail-field-value">{record.get("email", "—") or "—"}</div>
                </div>
            </div>
            <div class="detail-section">
                <div class="detail-section-title">// Experience</div>
                <div class="detail-field">
                    <div class="detail-field-label">Years</div>
                    <div class="detail-field-value">{record.get("experience", "—")}</div>
                </div>
                <div class="detail-field">
                    <div class="detail-field-label">Types</div>
                    <div>{exp_tags}</div>
                </div>
            </div>
        </div>

        <div class="detail-section" style="margin-bottom:1.25rem;">
            <div class="detail-section-title">// Equipment</div>
            <div>
                {equip_tag(record.get("vehicle","No"), "Vehicle")}
                {equip_tag(record.get("ladder","No"), "Ladder")}
                {equip_tag(record.get("insurance","No"), "Insurance")}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Photos
    p1 = record.get("photo1_url", "")
    p2 = record.get("photo2_url", "")
    if p1 or p2:
        st.markdown('<div class="detail-section" style="margin-bottom:1.25rem;"><div class="detail-section-title">// Install Photos</div>', unsafe_allow_html=True)
        pcol1, pcol2 = st.columns(2)
        if p1:
            with pcol1:
                st.image(p1, use_container_width=True)
        if p2:
            with pcol2:
                st.image(p2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Actions
    st.markdown("---")
    col_status, col_notes, col_delete = st.columns([1, 2, 0.8])

    with col_status:
        current_idx = STATUS_OPTIONS.index(record.get("status", "NEW")) if record.get("status", "NEW") in STATUS_OPTIONS else 0
        new_status = st.selectbox("Update Status", STATUS_OPTIONS, index=current_idx, key="detail_status")
        if st.button("Save Status", type="primary", use_container_width=True):
            update_status(record["id"], new_status)
            st.cache_data.clear()
            st.success(f"Status updated to {new_status}")
            st.rerun()

    with col_notes:
        current_notes = record.get("notes", "") or ""
        notes = st.text_area("Hiring Notes", value=current_notes, height=100, key="detail_notes")
        if st.button("Save Notes", use_container_width=True):
            update_notes(record["id"], notes)
            st.cache_data.clear()
            st.success("Notes saved")
            st.rerun()

    with col_delete:
        st.write("")
        st.write("")
        if st.button("🗑️ Delete", use_container_width=True):
            delete_applicant(record["id"])
            st.cache_data.clear()
            st.session_state.view_id = None
            st.rerun()

    st.stop()


# ══════════════════════════════════════
#  MAIN DASHBOARD
# ══════════════════════════════════════

# ── Stats Row ──
total = len(data)
new_count = sum(1 for d in data if d.get("status") == "NEW")
contacted = sum(1 for d in data if d.get("status") == "CONTACTED")
interview = sum(1 for d in data if d.get("status") == "INTERVIEW")
hired = sum(1 for d in data if d.get("status") == "HIRED")

# Recent (last 7 days)
recent = 0
for d in data:
    try:
        dt = datetime.fromisoformat(d.get("created_at", "").replace("Z", "+00:00"))
        if dt > datetime.now(dt.tzinfo) - timedelta(days=7):
            recent += 1
    except:
        pass

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card blue">
        <div class="stat-label">Total Applicants</div>
        <div class="stat-num">{total}</div>
        <div class="stat-delta neutral">all time</div>
    </div>
    <div class="stat-card blue">
        <div class="stat-label">New / Unreviewed</div>
        <div class="stat-num">{new_count}</div>
        <div class="stat-delta up">+{recent} this week</div>
    </div>
    <div class="stat-card amber">
        <div class="stat-label">Contacted</div>
        <div class="stat-num">{contacted}</div>
        <div class="stat-delta neutral">in pipeline</div>
    </div>
    <div class="stat-card cyan">
        <div class="stat-label">Interview</div>
        <div class="stat-num">{interview}</div>
        <div class="stat-delta neutral">scheduled</div>
    </div>
    <div class="stat-card green">
        <div class="stat-label">Hired</div>
        <div class="stat-num">{hired}</div>
        <div class="stat-delta up">✓ onboarded</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Filters ──
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 1])

with filter_col1:
    search = st.text_input("🔍 Search name or phone", key="search", label_visibility="collapsed", placeholder="Search name or phone...")

with filter_col2:
    status_filter = st.multiselect("Status", STATUS_OPTIONS, default=[], key="status_filter", placeholder="All statuses")

with filter_col3:
    exp_filter = st.multiselect("Experience", ["Starlink", "DirecTV", "Dish Network", "HughesNet", "Low Voltage", "TV Mounting", "Cable Installation", "Other"], default=[], key="exp_filter", placeholder="All experience")

with filter_col4:
    if data:
        df_export = pd.DataFrame(data)
        csv = df_export.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Export CSV", csv, "applicants.csv", "text/csv", use_container_width=True)

# Apply filters
filtered = data
if search:
    q = search.lower()
    filtered = [d for d in filtered if q in d.get("name", "").lower() or q in d.get("phone", "").lower()]
if status_filter:
    filtered = [d for d in filtered if d.get("status") in status_filter]
if exp_filter:
    def has_exp(d):
        types = d.get("exp_types", "")
        return any(e in types for e in exp_filter)
    filtered = [d for d in filtered if has_exp(d)]


# ── Tabs by Status ──
tab_all, tab_new, tab_contacted, tab_interview, tab_hired, tab_rejected = st.tabs([
    f"All ({len(filtered)})",
    f"New ({sum(1 for d in filtered if d.get('status')=='NEW')})",
    f"Contacted ({sum(1 for d in filtered if d.get('status')=='CONTACTED')})",
    f"Interview ({sum(1 for d in filtered if d.get('status')=='INTERVIEW')})",
    f"Hired ({sum(1 for d in filtered if d.get('status')=='HIRED')})",
    f"Rejected ({sum(1 for d in filtered if d.get('status')=='REJECTED')})",
])


def render_applicant_list(applicants, tab_key):
    if not applicants:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📋</div>
            <div>No applicants match your filters.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Table header
    st.markdown(f"""
    <div class="table-card">
        <div class="table-header">
            <div class="table-title">Applicants</div>
            <div class="table-count">{len(applicants)} results</div>
        </div>
        <div class="app-row" style="cursor:default;border-bottom:1px solid var(--border);">
            <div class="app-cell-mono" style="font-weight:600;">NAME</div>
            <div class="app-cell-mono" style="font-weight:600;">PHONE</div>
            <div class="app-cell-mono" style="font-weight:600;">EXPERIENCE</div>
            <div class="app-cell-mono" style="font-weight:600;">EQUIPMENT</div>
            <div class="app-cell-mono" style="font-weight:600;">STATUS</div>
            <div class="app-cell-mono" style="font-weight:600;">DATE</div>
        </div>
    """, unsafe_allow_html=True)

    for i, app in enumerate(applicants):
        s = app.get("status", "NEW")
        sc = STATUS_COLORS.get(s, "#3B82F6")

        # Equipment summary
        equip = []
        if app.get("vehicle") == "Yes": equip.append("🚛")
        if app.get("ladder") == "Yes": equip.append("🪜")
        if app.get("insurance") == "Yes": equip.append("🛡️")
        equip_str = " ".join(equip) if equip else "—"

        # Date
        created = app.get("created_at", "")
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            date_str = dt.strftime("%b %d")
        except:
            date_str = "—"

        exp_short = app.get("experience", "—")
        exp_types = app.get("exp_types", "")
        types_preview = exp_types[:30] + "..." if len(exp_types) > 30 else exp_types

        st.markdown(f"""
        <div class="app-row" id="row-{app['id']}">
            <div>
                <div class="app-name">{app.get("name","—")}</div>
                <div class="app-sub">{app.get("email","") or "no email"}</div>
            </div>
            <div class="app-cell">{app.get("phone","—")}</div>
            <div>
                <div class="app-cell">{exp_short}</div>
                <div class="app-sub">{types_preview}</div>
            </div>
            <div class="app-cell">{equip_str}</div>
            <div><span class="status-badge" style="background:{sc}18;color:{sc};border:1px solid {sc}30;">{s}</span></div>
            <div class="app-cell-mono">{date_str}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Clickable buttons for each applicant
    cols = st.columns(6)
    for i, app in enumerate(applicants):
        col_idx = i % 6
        with cols[col_idx]:
            if st.button(f"View: {app.get('name','—')[:15]}", key=f"{tab_key}_{app['id']}", use_container_width=True):
                st.session_state.view_id = app["id"]
                st.rerun()


with tab_all:
    render_applicant_list(filtered, "all")

with tab_new:
    render_applicant_list([d for d in filtered if d.get("status") == "NEW"], "new")

with tab_contacted:
    render_applicant_list([d for d in filtered if d.get("status") == "CONTACTED"], "cont")

with tab_interview:
    render_applicant_list([d for d in filtered if d.get("status") == "INTERVIEW"], "int")

with tab_hired:
    render_applicant_list([d for d in filtered if d.get("status") == "HIRED"], "hire")

with tab_rejected:
    render_applicant_list([d for d in filtered if d.get("status") == "REJECTED"], "rej")
