import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom | Starlink Technician", page_icon="🛰️", layout="centered")

# --- BOLD EDITORIAL / INDUSTRIAL AESTHETIC ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Sora:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-primary: #050505;
        --bg-card: #0C0C0C;
        --bg-elevated: #131313;
        --bg-input: #0F0F0F;
        --border-subtle: #1A1A1A;
        --border-mid: #252525;
        --accent: #3B82F6;
        --accent-bright: #60A5FA;
        --accent-glow: rgba(59, 130, 246, 0.15);
        --accent-warm: #F59E0B;
        --text-primary: #F5F5F5;
        --text-secondary: #9CA3AF;
        --text-muted: #6B7280;
        --text-faint: #404040;
        --success: #22C55E;
        --error: #EF4444;
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --radius-xl: 28px;
    }

    .stApp {
        background: var(--bg-primary);
        font-family: 'Sora', sans-serif;
    }

    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 640px !important;
    }

    /* ── HERO SECTION ── */
    .hero-wrapper {
        position: relative;
        overflow: hidden;
        border-radius: var(--radius-xl);
        border: 1px solid var(--border-subtle);
        background: var(--bg-card);
        margin-bottom: 1.5rem;
    }

    .hero-grid-bg {
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        mask-image: radial-gradient(ellipse 70% 60% at 50% 0%, black 0%, transparent 100%);
        -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 0%, black 0%, transparent 100%);
    }

    .hero-glow {
        position: absolute;
        top: -100px;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        height: 300px;
        background: radial-gradient(ellipse, rgba(59,130,246,0.08) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-content {
        position: relative;
        z-index: 2;
        padding: 2.5rem 2rem 2rem;
    }

    .hero-topline {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.75rem;
    }

    .pill-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.3rem 0.85rem;
        border-radius: 100px;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    .pill-hiring {
        background: rgba(34,197,94,0.1);
        color: #4ADE80;
        border: 1px solid rgba(34,197,94,0.2);
    }

    .pill-hiring::before {
        content: "";
        width: 6px;
        height: 6px;
        background: #4ADE80;
        border-radius: 50%;
        animation: pulse-dot 2s ease-in-out infinite;
    }

    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .pill-type {
        background: rgba(59,130,246,0.08);
        color: var(--accent-bright);
        border: 1px solid rgba(59,130,246,0.15);
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3.4rem;
        font-weight: 800;
        line-height: 1.0;
        letter-spacing: -0.035em;
        color: var(--text-primary);
        margin: 0 0 0.25rem 0;
    }

    .hero-title span {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-bright) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-family: 'Sora', sans-serif;
        font-size: 0.85rem;
        color: var(--text-muted);
        font-weight: 400;
        margin-top: 0.5rem;
    }

    /* ── METRIC STRIP ── */
    .metric-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        border-top: 1px solid var(--border-subtle);
        overflow: hidden;
    }

    .metric-cell {
        padding: 1.1rem 0.8rem;
        border-right: 1px solid var(--border-subtle);
        position: relative;
        min-width: 0;
        overflow: hidden;
    }

    .metric-cell:last-child {
        border-right: none;
    }

    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.55rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
        white-space: nowrap;
    }

    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.2;
        white-space: nowrap;
    }

    .metric-sub {
        font-size: 0.65rem;
        color: var(--accent-bright);
        font-weight: 500;
        margin-top: 0.1rem;
        white-space: nowrap;
    }

    @media (max-width: 480px) {
        .metric-cell {
            padding: 0.9rem 0.6rem;
        }
        .metric-value {
            font-size: 1.1rem;
        }
        .metric-label {
            font-size: 0.5rem;
        }
        .hero-title {
            font-size: 2.6rem;
        }
        .hero-content {
            padding: 2rem 1.25rem 1.5rem;
        }
    }

    /* ── SECTION CARD ── */
    .section-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 1.75rem 1.75rem;
        margin-bottom: 1rem;
    }

    .section-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        font-weight: 600;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.75rem;
    }

    .desc-text {
        font-size: 0.92rem;
        line-height: 1.7;
        color: var(--text-secondary);
    }

    /* ── ROLE / REQUIREMENTS GRID ── */
    .dual-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .grid-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
    }

    .grid-panel-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        font-weight: 600;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--border-subtle);
    }

    .grid-item {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        margin-bottom: 0.7rem;
        font-size: 0.82rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }

    .grid-item:last-child {
        margin-bottom: 0;
    }

    .grid-icon {
        width: 18px;
        height: 18px;
        min-width: 18px;
        background: rgba(59,130,246,0.08);
        border: 1px solid rgba(59,130,246,0.12);
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.55rem;
        color: var(--accent-bright);
        margin-top: 1px;
    }

    /* ── CTA BUTTON ── */
    div.stButton > button {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.85rem 2rem !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em !important;
        width: 100% !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 0 0 0 rgba(59,130,246,0) !important;
    }

    div.stButton > button:hover {
        background: #2563EB !important;
        box-shadow: 0 4px 24px rgba(59,130,246,0.3) !important;
        transform: translateY(-1px) !important;
    }

    div.stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── FORM STYLES ── */
    .form-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 2rem;
        margin-bottom: 1rem;
    }

    .form-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }

    .form-subtitle {
        font-size: 0.82rem;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
    }

    .form-divider {
        height: 1px;
        background: var(--border-subtle);
        margin: 1.25rem 0;
    }

    .form-section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }

    .stTextInput input, .stTextArea textarea {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-mid) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.88rem !important;
        padding: 0.65rem 0.9rem !important;
        transition: border-color 0.2s !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-glow) !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background: var(--bg-input) !important;
        border-radius: var(--radius-sm) !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-mid) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.88rem !important;
    }

    label {
        color: var(--text-secondary) !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 400 !important;
        font-size: 0.8rem !important;
    }

    .stCheckbox label span {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }

    /* ── BACK LINK ── */
    .back-link {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: color 0.2s;
    }

    .back-link:hover {
        color: var(--accent-bright);
    }

    /* ── SUCCESS STATE ── */
    .success-wrapper {
        text-align: center;
        padding: 3rem 2rem;
    }

    .success-icon {
        width: 72px;
        height: 72px;
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.15);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
    }

    .success-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }

    .success-desc {
        font-size: 0.88rem;
        color: var(--text-muted);
        line-height: 1.6;
        max-width: 320px;
        margin: 0 auto 2rem;
    }

    /* ── FOOTER ── */
    .site-footer {
        text-align: center;
        padding: 1.5rem 0 0;
    }

    .footer-brand {
        font-family: 'Outfit', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-faint);
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .footer-sub {
        font-size: 0.65rem;
        color: var(--text-faint);
        margin-top: 0.2rem;
        opacity: 0.6;
    }

    /* ── ERROR ── */
    .stAlert {
        border-radius: var(--radius-md) !important;
    }

    /* ── HIDE STREAMLIT DEFAULTS ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# --- DATABASE ---
def init_db():
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS applicants
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT,
                  experience TEXT, exp_types TEXT, vehicle TEXT, ladder TEXT, insurance TEXT,
                  status TEXT, timestamp TEXT)""")
    conn.commit()
    conn.close()


def save_applicant(data):
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()
    c.execute(
        """INSERT INTO applicants
           (name, phone, email, experience, exp_types, vehicle, ladder, insurance, status, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data["name"], data["phone"], data["email"], data["experience"],
            data["exp_types"], data["vehicle"], data["ladder"], data["insurance"],
            "NEW", datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


init_db()

# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "home"


# ╔══════════════════════════════════════════╗
# ║              HOME  PAGE                  ║
# ╚══════════════════════════════════════════╝
if st.session_state.page == "home":

    # ── Hero ──
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-grid-bg"></div>
        <div class="hero-glow"></div>
        <div class="hero-content">
            <div class="hero-topline">
                <span class="pill-badge pill-hiring">HIRING NOW</span>
                <span class="pill-badge pill-type">1099 · INDEPENDENT</span>
            </div>
            <div class="hero-title">Starlink<br><span>Technician</span></div>
            <div class="hero-subtitle">Greater metro area · Flexible schedule · Performance-based pay</div>
        </div>
        <div class="metric-strip">
            <div class="metric-cell">
                <div class="metric-label">Earnings</div>
                <div class="metric-value">$1,200–$1,800</div>
                <div class="metric-sub">per week</div>
            </div>
            <div class="metric-cell">
                <div class="metric-label">Availability</div>
                <div class="metric-value">Immediate</div>
                <div class="metric-sub">start this week</div>
            </div>
            <div class="metric-cell">
                <div class="metric-label">Daily Installs</div>
                <div class="metric-value">3 – 5</div>
                <div class="metric-sub">residential</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Description ──
    st.markdown("""
    <div class="section-card">
        <div class="section-eyebrow">// About the Role</div>
        <div class="desc-text">
            We're hiring experienced technicians to install Starlink satellite internet
            systems across the greater metro area. You'll work independently — handling
            residential installs from start to finish with full dispatch support. This is a
            performance-based, uncapped-earning opportunity for self-starters who take pride
            in quality work.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Dual grid ──
    st.markdown("""
    <div class="dual-grid">
        <div class="grid-panel">
            <div class="grid-panel-title">// What You'll Do</div>
            <div class="grid-item"><div class="grid-icon">▸</div>Residential Starlink installations</div>
            <div class="grid-item"><div class="grid-icon">▸</div>Roof mounting &amp; cable routing</div>
            <div class="grid-item"><div class="grid-icon">▸</div>Signal optimization &amp; testing</div>
            <div class="grid-item"><div class="grid-icon">▸</div>Customer walkthroughs</div>
        </div>
        <div class="grid-panel">
            <div class="grid-panel-title">// What You Need</div>
            <div class="grid-item"><div class="grid-icon">✓</div>Reliable truck, van, or SUV</div>
            <div class="grid-item"><div class="grid-icon">✓</div>24 ft+ fiberglass ladder</div>
            <div class="grid-item"><div class="grid-icon">✓</div>Basic tools &amp; power drill</div>
            <div class="grid-item"><div class="grid-icon">✓</div>Smartphone w/ data plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA ──
    if st.button("APPLY NOW →", use_container_width=True):
        st.session_state.page = "apply"
        st.rerun()


# ╔══════════════════════════════════════════╗
# ║          APPLICATION  PAGE               ║
# ╚══════════════════════════════════════════╝
elif st.session_state.page == "apply":

    if st.button("← Back to listing"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("""
    <div class="form-card" style="margin-top:0.25rem;">
        <div class="form-title">Apply</div>
        <div class="form-subtitle">Fill out the basics — we'll be in touch within 48 hours.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("application_form"):

        # — Contact —
        st.markdown('<div class="form-section-label">Contact Information</div>', unsafe_allow_html=True)
        name = st.text_input("Full name *")
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Phone number *")
        with col2:
            email = st.text_input("Email address")

        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)

        # — Experience —
        st.markdown('<div class="form-section-label">Experience</div>', unsafe_allow_html=True)
        experience = st.selectbox(
            "Years of installation experience",
            ["Less than 1 year", "1–2 years", "3–5 years", "5+ years", "10+ years"],
        )

        st.markdown('<div class="form-section-label" style="margin-top:1rem;">Installation Experience (select all that apply)</div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            exp_starlink = st.checkbox("Starlink")
            exp_directv = st.checkbox("DirecTV")
            exp_dish = st.checkbox("Dish Network")
            exp_hughesnet = st.checkbox("HughesNet")
        with col_b:
            exp_lowvoltage = st.checkbox("Low Voltage")
            exp_tvmount = st.checkbox("TV Mounting")
            exp_cable = st.checkbox("Cable Installation")
            exp_other = st.checkbox("Other Related")

        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)

        # — Equipment —
        st.markdown('<div class="form-section-label">Equipment Check</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            vehicle = st.checkbox("Reliable truck / van / SUV")
            ladder = st.checkbox("24 ft+ fiberglass ladder")
        with col2:
            tools = st.checkbox("Basic installation tools")
            insurance = st.checkbox("Liability insurance")

        st.markdown("<br>", unsafe_allow_html=True)

        submitted = st.form_submit_button("SUBMIT APPLICATION →", use_container_width=True)

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Name and phone number are required.")
            elif not vehicle or not ladder:
                st.error("A vehicle and ladder are required for this role.")
            else:
                exp_list = []
                if exp_starlink: exp_list.append("Starlink")
                if exp_directv: exp_list.append("DirecTV")
                if exp_dish: exp_list.append("Dish Network")
                if exp_hughesnet: exp_list.append("HughesNet")
                if exp_lowvoltage: exp_list.append("Low Voltage")
                if exp_tvmount: exp_list.append("TV Mounting")
                if exp_cable: exp_list.append("Cable Installation")
                if exp_other: exp_list.append("Other")
                save_applicant({
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "experience": experience,
                    "exp_types": ", ".join(exp_list) if exp_list else "None selected",
                    "vehicle": "Yes" if vehicle else "No",
                    "ladder": "Yes" if ladder else "No",
                    "insurance": "Yes" if insurance else "No",
                })
                st.session_state.page = "success"
                st.rerun()


# ╔══════════════════════════════════════════╗
# ║            SUCCESS  PAGE                 ║
# ╚══════════════════════════════════════════╝
elif st.session_state.page == "success":

    st.markdown("""
    <div class="form-card">
        <div class="success-wrapper">
            <div class="success-icon">✓</div>
            <div class="success-title">Application Received</div>
            <div class="success-desc">
                Thanks for your interest. Our team will review your information
                and reach out within two business days.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("BACK TO LISTING", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()


# ── Footer ──
st.markdown("""
<div class="site-footer">
    <div class="footer-brand">VERGECOM LLC</div>
    <div class="footer-sub">Independent Contractor Opportunities</div>
</div>
""", unsafe_allow_html=True)
