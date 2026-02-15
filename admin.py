import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client

# ── Config ──
st.set_page_config(page_title="Vergecom | Master Control", page_icon="🏢", layout="wide")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ── Styles ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        --bg: #F8FAFC;
        --white: #FFFFFF;
        --border: #E2E8F0;
        --border-light: #F1F5F9;
        --accent: #1E40AF;
        --accent-light: #DBEAFE;
        --text-1: #0F172A;
        --text-2: #475569;
        --text-3: #94A3B8;
        --green: #059669;
        --green-bg: #ECFDF5;
        --amber: #D97706;
        --amber-bg: #FFFBEB;
        --red: #DC2626;
        --red-bg: #FEF2F2;
        --blue: #2563EB;
        --blue-bg: #EFF6FF;
        --purple: #7C3AED;
        --purple-bg: #F5F3FF;
        --cyan: #0891B2;
        --cyan-bg: #ECFEFF;
    }

    .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif !important; }
    .block-container { padding: 0 2rem 4rem !important; max-width: 1300px !important; }

    /* Header */
    .mc-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #0F172A 100%);
        color: white;
        padding: 1rem 1.75rem;
        border-radius: 0 0 12px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -1rem -2rem 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .mc-brand {
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    .mc-brand span { color: #60A5FA; }
    .mc-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.75rem;
        color: #94A3B8;
    }
    .mc-dot {
        width: 8px;
        height: 8px;
        background: #34D399;
        border-radius: 50%;
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.3; } }

    /* KPI */
    .kpi-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.6rem; margin-bottom: 1.25rem; }
    .kpi-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.9rem 0.8rem;
        text-align: center;
    }
    .kpi-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.55rem;
        font-weight: 500;
        color: var(--text-3);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.25rem;
    }
    .kpi-num { font-size: 1.5rem; font-weight: 700; color: var(--text-1); line-height: 1; }
    .kpi-sub { font-size: 0.6rem; font-weight: 500; margin-top: 0.15rem; }
    .kpi-sub.green { color: var(--green); }
    .kpi-sub.muted { color: var(--text-3); }

    /* Cards */
    .card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-1);
        margin-bottom: 0.25rem;
    }
    .card-sub {
        font-size: 0.78rem;
        color: var(--text-3);
        margin-bottom: 1rem;
    }
    .sec-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        font-weight: 600;
        color: var(--text-3);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.5rem;
    }

    /* Applicant row */
    .ap-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.85rem 1.1rem;
        margin-bottom: 0.4rem;
        display: grid;
        grid-template-columns: 2fr 1fr 1.2fr 1.4fr 1fr 0.8fr;
        align-items: center;
        gap: 0.6rem;
        transition: border-color 0.15s;
    }
    .ap-card:hover { border-color: var(--blue); }
    .ap-name { font-size: 0.85rem; font-weight: 600; color: var(--text-1); }
    .ap-sub { font-size: 0.7rem; color: var(--text-3); margin-top: 0.05rem; }
    .ap-cell { font-size: 0.78rem; color: var(--text-2); }
    .ap-mono { font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: var(--text-3); }
    .ap-tag {
        font-size: 0.58rem; font-weight: 600; padding: 0.15rem 0.4rem; border-radius: 4px;
        display: inline-block; margin: 0.1rem 0.1rem 0.1rem 0;
    }
    .ap-tag.blue { background: var(--blue-bg); color: var(--blue); }
    .s-badge {
        font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; font-weight: 600;
        padding: 0.2rem 0.5rem; border-radius: 5px; display: inline-block;
    }
    .eq-pill { font-size: 0.62rem; font-weight: 500; padding: 0.15rem 0.35rem; border-radius: 4px; display: inline-block; margin-right: 0.15rem; }
    .eq-y { background: var(--green-bg); color: var(--green); }
    .eq-n { background: var(--red-bg); color: var(--red); }

    .list-hdr {
        display: grid;
        grid-template-columns: 2fr 1fr 1.2fr 1.4fr 1fr 0.8fr;
        gap: 0.6rem;
        padding: 0.5rem 1.1rem;
        margin-bottom: 0.25rem;
    }
    .list-hdr-cell {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.55rem; font-weight: 600; color: var(--text-3);
        text-transform: uppercase; letter-spacing: 0.06em;
    }

    .empty-box {
        background: var(--white); border: 1px dashed var(--border); border-radius: 10px;
        text-align: center; padding: 2.5rem; color: var(--text-3); font-size: 0.85rem;
    }

    /* Detail */
    .detail-name { font-size: 1.4rem; font-weight: 700; color: var(--text-1); }
    .detail-date { font-size: 0.75rem; color: var(--text-3); margin-top: 0.2rem; }
    .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1rem; }
    .info-box { background: var(--bg); border: 1px solid var(--border-light); border-radius: 10px; padding: 1rem; }
    .info-box-title { font-family: 'IBM Plex Mono', monospace; font-size: 0.55rem; font-weight: 600; color: var(--blue); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.6rem; }
    .info-row { margin-bottom: 0.4rem; }
    .info-label { font-size: 0.65rem; color: var(--text-3); }
    .info-val { font-size: 0.85rem; color: var(--text-1); font-weight: 500; }

    /* Overrides */
    .stSelectbox div[data-baseweb="select"] > div { background: var(--white) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; font-size: 0.82rem !important; }
    .stTextInput input, .stTextArea textarea { background: var(--white) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; font-size: 0.85rem !important; }
    label { font-family: 'DM Sans', sans-serif !important; font-size: 0.78rem !important; color: var(--text-2) !important; }
    .stMultiSelect div[data-baseweb="select"] > div { background: var(--white) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
    div.stButton > button { font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; border-radius: 8px !important; }
    .stDownloadButton > button { background: var(--white) !important; color: var(--text-2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; font-size: 0.78rem !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 0; background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 0.2rem; }
    .stTabs [data-baseweb="tab"] { font-family: 'DM Sans', sans-serif; font-size: 0.78rem; font-weight: 500; color: var(--text-3); border-radius: 8px; padding: 0.45rem 0.9rem; }
    .stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown(f"""
<div class="mc-header">
    <div class="mc-brand">Verge<span>com</span> &nbsp;Master Console</div>
    <div class="mc-status"><div class="mc-dot"></div>SYSTEM ACTIVE &middot; {datetime.now().strftime("%b %d, %Y %I:%M %p")}</div>
</div>
""", unsafe_allow_html=True)

# ── Data ──
@st.cache_data(ttl=30)
def load_applicants():
    res = supabase.table("applicants").select("*").order("created_at", desc=True).execute()
    return res.data or []

@st.cache_data(ttl=60)
def load_site_settings():
    try:
        res = supabase.table("site_settings").select("*").eq("id", 1).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
        return None
    except Exception as e:
        return None

def update_status(aid, s):
    supabase.table("applicants").update({"status": s}).eq("id", aid).execute()
def update_notes(aid, n):
    supabase.table("applicants").update({"notes": n}).eq("id", aid).execute()
def delete_applicant(aid):
    supabase.table("applicants").delete().eq("id", aid).execute()

if "view_id" not in st.session_state:
    st.session_state.view_id = None

data = load_applicants()

# ── Helpers ──
STATUS_LIST = ["NEW", "REVIEWED", "CONTACTED", "INTERVIEW", "HIRED", "REJECTED"]
STATUS_BG = {"NEW":"blue","REVIEWED":"purple","CONTACTED":"amber","INTERVIEW":"cyan","HIRED":"green","REJECTED":"red"}

def badge(s):
    bg = STATUS_BG.get(s, "blue")
    return f'<span class="s-badge" style="background:var(--{bg}-bg);color:var(--{bg});">{s}</span>'

def fmt_d(iso):
    try: return datetime.fromisoformat(iso.replace("Z","+00:00")).strftime("%b %d")
    except: return "—"

def fmt_full(iso):
    try: return datetime.fromisoformat(iso.replace("Z","+00:00")).strftime("%b %d, %Y %I:%M %p")
    except: return "—"

def exp_tags(s):
    if not s or s == "None selected": return ""
    return "".join(f'<span class="ap-tag blue">{t.strip()}</span>' for t in s.split(",")[:4])

def eq(r):
    out = ""
    for k, l in [("vehicle","Veh"),("ladder","Ldr"),("insurance","Ins")]:
        v = r.get(k,"No")
        c = "eq-y" if v=="Yes" else "eq-n"
        out += f'<span class="eq-pill {c}">{"✓" if v=="Yes" else "✗"} {l}</span>'
    return out


# ═══════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════
main_tab1, main_tab2 = st.tabs(["👥 Applicant Registry", "🛠️ Website Maintenance"])


# ═══════════════ TAB 1: REGISTRY ═══════════════
with main_tab1:

    # ── DETAIL VIEW ──
    if st.session_state.view_id is not None:
        rec = next((r for r in data if str(r["id"]) == str(st.session_state.view_id)), None)

        if st.button("← Back to registry"):
            st.session_state.view_id = None
            st.rerun()

        if not rec:
            st.error("Applicant not found.")
            st.stop()

        s = rec.get("status", "NEW")
        exp_t = rec.get("exp_types", "")
        et_html = " ".join(f'<span class="ap-tag blue" style="font-size:0.7rem;padding:0.2rem 0.5rem;">{t.strip()}</span>' for t in exp_t.split(",")) if exp_t and exp_t != "None selected" else '<span style="color:var(--text-3);">None</span>'

        st.markdown(f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.25rem;padding-bottom:1rem;border-bottom:1px solid var(--border-light);">
                <div>
                    <div class="detail-name">{rec.get("name","—")}</div>
                    <div class="detail-date">Applied {fmt_full(rec.get("created_at",""))}</div>
                </div>
                <div>{badge(s)}</div>
            </div>
            <div class="info-grid">
                <div class="info-box">
                    <div class="info-box-title">Contact</div>
                    <div class="info-row"><div class="info-label">Phone</div><div class="info-val">{rec.get("phone","—")}</div></div>
                    <div class="info-row"><div class="info-label">Email</div><div class="info-val">{rec.get("email") or "—"}</div></div>
                </div>
                <div class="info-box">
                    <div class="info-box-title">Service Area</div>
                    <div class="info-row"><div class="info-label">State</div><div class="info-val">{rec.get("state","—")}</div></div>
                    <div class="info-row"><div class="info-label">Counties</div><div class="info-val">{rec.get("counties","—")}</div></div>
                    <div class="info-row"><div class="info-label">Travel Radius</div><div class="info-val">{rec.get("radius","—")}</div></div>
                </div>
            </div>
            <div class="info-grid">
                <div class="info-box">
                    <div class="info-box-title">Experience</div>
                    <div class="info-row"><div class="info-label">Years</div><div class="info-val">{rec.get("experience","—")}</div></div>
                    <div class="info-row"><div class="info-label">Types</div><div style="margin-top:0.2rem;">{et_html}</div></div>
                </div>
                <div class="info-box">
                    <div class="info-box-title">Equipment</div>
                    <div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-top:0.3rem;">{eq(rec)}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Photos
        p1 = rec.get("photo1_url","")
        p2 = rec.get("photo2_url","")
        if p1 or p2:
            st.markdown('<div class="sec-label">Install Photos</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if p1:
                with c1: st.image(p1, use_container_width=True)
            if p2:
                with c2: st.image(p2, use_container_width=True)

        # Actions
        st.markdown('<div class="sec-label" style="margin-top:1rem;">Actions</div>', unsafe_allow_html=True)
        ac1, ac2 = st.columns([1, 2])
        with ac1:
            ci = STATUS_LIST.index(s) if s in STATUS_LIST else 0
            ns = st.selectbox("Status", STATUS_LIST, index=ci, key="ds")
            if st.button("Save Status", type="primary", use_container_width=True):
                update_status(rec["id"], ns)
                st.cache_data.clear()
                st.success(f"→ {ns}")
                st.rerun()
        with ac2:
            cn = rec.get("notes","") or ""
            notes = st.text_area("Hiring Notes", value=cn, height=105, key="dn", placeholder="Private notes...")
            if st.button("Save Notes", use_container_width=True):
                update_notes(rec["id"], notes)
                st.cache_data.clear()
                st.success("Saved")
                st.rerun()

        st.markdown("---")
        _, _, dc = st.columns([3, 3, 1])
        with dc:
            if st.button("🗑 Delete", use_container_width=True):
                delete_applicant(rec["id"])
                st.cache_data.clear()
                st.session_state.view_id = None
                st.rerun()

    # ── LIST VIEW ──
    else:
        # KPIs
        total = len(data)
        new_ct = sum(1 for d in data if d.get("status") == "NEW")
        cont_ct = sum(1 for d in data if d.get("status") == "CONTACTED")
        int_ct = sum(1 for d in data if d.get("status") == "INTERVIEW")
        hire_ct = sum(1 for d in data if d.get("status") == "HIRED")
        rej_ct = sum(1 for d in data if d.get("status") == "REJECTED")
        week_ct = 0
        for d in data:
            try:
                dt = datetime.fromisoformat(d.get("created_at","").replace("Z","+00:00"))
                if dt > datetime.now(dt.tzinfo) - timedelta(days=7): week_ct += 1
            except: pass

        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card"><div class="kpi-label">Total</div><div class="kpi-num">{total}</div><div class="kpi-sub muted">all time</div></div>
            <div class="kpi-card"><div class="kpi-label">New</div><div class="kpi-num">{new_ct}</div><div class="kpi-sub green">+{week_ct} this week</div></div>
            <div class="kpi-card"><div class="kpi-label">Contacted</div><div class="kpi-num">{cont_ct}</div><div class="kpi-sub muted">pipeline</div></div>
            <div class="kpi-card"><div class="kpi-label">Interview</div><div class="kpi-num">{int_ct}</div><div class="kpi-sub muted">scheduled</div></div>
            <div class="kpi-card"><div class="kpi-label">Hired</div><div class="kpi-num">{hire_ct}</div><div class="kpi-sub green">onboarded</div></div>
            <div class="kpi-card"><div class="kpi-label">Rejected</div><div class="kpi-num">{rej_ct}</div><div class="kpi-sub muted">declined</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Filters
        f1, f2, f3, f4 = st.columns([2, 1.3, 1.3, 0.8])
        with f1: search = st.text_input("Search", key="s", label_visibility="collapsed", placeholder="Search name or phone...")
        with f2: sf = st.multiselect("Status", STATUS_LIST, default=[], key="sf", placeholder="All statuses")
        with f3: ef = st.multiselect("Exp", ["Starlink","DirecTV","Dish Network","HughesNet","Low Voltage","TV Mounting","Cable Installation","Other"], default=[], key="ef", placeholder="All experience")
        with f4:
            if data:
                csv = pd.DataFrame(data).to_csv(index=False).encode("utf-8")
                st.download_button("Export CSV", csv, "applicants.csv", "text/csv", use_container_width=True)

        filtered = data
        if search:
            q = search.lower()
            filtered = [d for d in filtered if q in d.get("name","").lower() or q in d.get("phone","").lower()]
        if sf: filtered = [d for d in filtered if d.get("status") in sf]
        if ef: filtered = [d for d in filtered if any(e in d.get("exp_types","") for e in ef)]

        # Tabs
        tabs = st.tabs([
            f"All  {len(filtered)}",
            f"New  {sum(1 for d in filtered if d.get('status')=='NEW')}",
            f"Contacted  {sum(1 for d in filtered if d.get('status')=='CONTACTED')}",
            f"Interview  {sum(1 for d in filtered if d.get('status')=='INTERVIEW')}",
            f"Hired  {sum(1 for d in filtered if d.get('status')=='HIRED')}",
            f"Rejected  {sum(1 for d in filtered if d.get('status')=='REJECTED')}",
        ])

        def render(apps, kp):
            if not apps:
                st.markdown('<div class="empty-box">No applicants here yet.</div>', unsafe_allow_html=True)
                return
            st.markdown("""<div class="list-hdr">
                <div class="list-hdr-cell">Applicant</div>
                <div class="list-hdr-cell">Phone</div>
                <div class="list-hdr-cell">Location</div>
                <div class="list-hdr-cell">Experience</div>
                <div class="list-hdr-cell">Equipment</div>
                <div class="list-hdr-cell">Date</div>
            </div>""", unsafe_allow_html=True)

            for a in apps:
                loc = f"{a.get('counties','—')}, {a.get('state','')}" if a.get('state') else a.get('counties','—')
                st.markdown(f"""
                <div class="ap-card">
                    <div><div class="ap-name">{a.get("name","—")}</div><div class="ap-sub">{a.get("email") or "—"} &nbsp;{badge(a.get("status","NEW"))}</div></div>
                    <div class="ap-mono">{a.get("phone","—")}</div>
                    <div><div class="ap-cell">{loc}</div><div class="ap-sub">{a.get("radius","")}</div></div>
                    <div><div class="ap-cell">{a.get("experience","—")}</div><div class="ap-sub" style="margin-top:0.15rem;">{exp_tags(a.get("exp_types",""))}</div></div>
                    <div>{eq(a)}</div>
                    <div class="ap-mono">{fmt_d(a.get("created_at",""))}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"View {a.get('name','—')}", key=f"{kp}_{a['id']}", use_container_width=True):
                    st.session_state.view_id = a["id"]
                    st.rerun()

        tab_filters = [
            lambda d: True,
            lambda d: d.get("status") == "NEW",
            lambda d: d.get("status") == "CONTACTED",
            lambda d: d.get("status") == "INTERVIEW",
            lambda d: d.get("status") == "HIRED",
            lambda d: d.get("status") == "REJECTED",
        ]
        tab_keys = ["all","new","cont","int","hire","rej"]
        for i, tab in enumerate(tabs):
            with tab:
                render([d for d in filtered if tab_filters[i](d)], tab_keys[i])


# ═══════════════ TAB 2: WEBSITE MAINTENANCE ═══════════════
with main_tab2:

    st.markdown("""
    <div class="card">
        <div class="card-title">Website Content Editor</div>
        <div class="card-sub">Edit the live job listing text that applicants see on the public site. Changes go live immediately.</div>
    </div>
    """, unsafe_allow_html=True)

    curr = load_site_settings()

    if curr is None:
        st.warning("⚠️ No `site_settings` table found. Run this SQL in Supabase SQL Editor to create it:")
        st.code("""CREATE TABLE site_settings (
    id          INTEGER PRIMARY KEY DEFAULT 1,
    hero_title  TEXT DEFAULT 'Starlink Technician',
    hero_subtitle TEXT DEFAULT 'Greater metro area · Flexible schedule · Performance-based pay',
    job_desc    TEXT DEFAULT 'We are hiring experienced technicians to install Starlink satellite internet systems across the greater metro area.',
    earning_min TEXT DEFAULT '$1,200',
    earning_max TEXT DEFAULT '$1,800',
    daily_installs TEXT DEFAULT '3 – 5',
    requirements TEXT DEFAULT 'Reliable truck/van/SUV, 24ft+ fiberglass ladder, Basic tools & power drill, Smartphone w/ data plan',
    duties      TEXT DEFAULT 'Residential Starlink installations, Roof mounting & cable routing, Signal optimization & testing, Customer walkthroughs',
    last_updated TIMESTAMPTZ DEFAULT now(),
    CHECK (id = 1)
);

INSERT INTO site_settings (id) VALUES (1);

-- Allow your app to read/write it
CREATE POLICY "Anon site settings access"
ON site_settings FOR ALL TO anon
USING (true) WITH CHECK (true);

ALTER TABLE site_settings ENABLE ROW LEVEL SECURITY;""", language="sql")
        st.info("After running the SQL above, refresh this page.")
    else:
        with st.form("site_editor"):
            st.markdown('<div class="sec-label">Hero Section</div>', unsafe_allow_html=True)
            new_title = st.text_input("Job Title", value=curr.get("hero_title", ""))
            new_subtitle = st.text_input("Subtitle Line", value=curr.get("hero_subtitle", ""))

            st.markdown('<div class="sec-label" style="margin-top:1rem;">Pay & Schedule</div>', unsafe_allow_html=True)
            pc1, pc2, pc3 = st.columns(3)
            with pc1: earn_min = st.text_input("Earning Min", value=curr.get("earning_min", "$1,200"))
            with pc2: earn_max = st.text_input("Earning Max", value=curr.get("earning_max", "$1,800"))
            with pc3: daily = st.text_input("Daily Installs", value=curr.get("daily_installs", "3 – 5"))

            st.markdown('<div class="sec-label" style="margin-top:1rem;">Job Description</div>', unsafe_allow_html=True)
            new_desc = st.text_area("Description paragraph", value=curr.get("job_desc", ""), height=150)

            st.markdown('<div class="sec-label" style="margin-top:1rem;">What You\'ll Do (comma separated)</div>', unsafe_allow_html=True)
            new_duties = st.text_area("Duties list", value=curr.get("duties", ""), height=100,
                                      placeholder="Residential Starlink installations, Roof mounting & cable routing, ...")

            st.markdown('<div class="sec-label" style="margin-top:1rem;">What You Need (comma separated)</div>', unsafe_allow_html=True)
            new_reqs = st.text_area("Requirements list", value=curr.get("requirements", ""), height=100,
                                    placeholder="Reliable truck/van/SUV, 24ft+ fiberglass ladder, ...")

            if st.form_submit_button("🚀 Publish Updates to Live Site", type="primary", use_container_width=True):
                try:
                    supabase.table("site_settings").upsert({
                        "id": 1,
                        "hero_title": new_title,
                        "hero_subtitle": new_subtitle,
                        "earning_min": earn_min,
                        "earning_max": earn_max,
                        "daily_installs": daily,
                        "job_desc": new_desc,
                        "duties": new_duties,
                        "requirements": new_reqs,
                        "last_updated": datetime.now().isoformat(),
                    }).execute()
                    st.cache_data.clear()
                    st.success("✅ Website content updated. Changes are live.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update: {e}")

        if curr.get("last_updated"):
            st.markdown(f'<div style="font-size:0.72rem;color:var(--text-3);margin-top:0.5rem;">Last updated: {fmt_full(curr["last_updated"])}</div>', unsafe_allow_html=True)
