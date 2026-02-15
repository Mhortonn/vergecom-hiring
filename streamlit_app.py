import streamlit as st
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom | Starlink Technician", page_icon="🛰️", layout="centered")

# --- SUPABASE CONFIG ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Supabase credentials missing. Add SUPABASE_URL and SUPABASE_KEY to .streamlit/secrets.toml")
    st.stop()

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- STYLES (identical to previous) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Sora:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-primary: #050505;
        --bg-card: #0C0C0C;
        --bg-input: #0F0F0F;
        --border-subtle: #1A1A1A;
        --border-mid: #252525;
        --accent: #3B82F6;
        --accent-bright: #60A5FA;
        --accent-glow: rgba(59, 130, 246, 0.15);
        --text-primary: #F5F5F5;
        --text-secondary: #9CA3AF;
        --text-muted: #6B7280;
        --text-faint: #404040;
        --success: #22C55E;
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --radius-xl: 28px;
    }

    .stApp { background: var(--bg-primary); font-family: 'Sora', sans-serif; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 4rem !important; max-width: 640px !important; }

    .hero-wrapper { position: relative; overflow: hidden; border-radius: var(--radius-xl); border: 1px solid var(--border-subtle); background: var(--bg-card); margin-bottom: 1.5rem; }
    .hero-grid-bg { position: absolute; inset: 0; background-image: linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px); background-size: 40px 40px; mask-image: radial-gradient(ellipse 70% 60% at 50% 0%, black 0%, transparent 100%); -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 0%, black 0%, transparent 100%); }
    .hero-glow { position: absolute; top: -100px; left: 50%; transform: translateX(-50%); width: 500px; height: 300px; background: radial-gradient(ellipse, rgba(59,130,246,0.08) 0%, transparent 70%); pointer-events: none; }
    .hero-content { position: relative; z-index: 2; padding: 2.5rem 2rem 2rem; }
    .hero-topline { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.75rem; }
    .pill-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.3rem 0.85rem; border-radius: 100px; display: inline-flex; align-items: center; gap: 0.4rem; }
    .pill-hiring { background: rgba(34,197,94,0.1); color: #4ADE80; border: 1px solid rgba(34,197,94,0.2); }
    .pill-hiring::before { content: ""; width: 6px; height: 6px; background: #4ADE80; border-radius: 50%; animation: pulse-dot 2s ease-in-out infinite; }
    @keyframes pulse-dot { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
    .pill-type { background: rgba(59,130,246,0.08); color: var(--accent-bright); border: 1px solid rgba(59,130,246,0.15); }
    .hero-title { font-family: 'Outfit', sans-serif; font-size: 3.4rem; font-weight: 800; line-height: 1.0; letter-spacing: -0.035em; color: var(--text-primary); margin: 0 0 0.25rem 0; }
    .hero-title span { background: linear-gradient(135deg, var(--accent) 0%, var(--accent-bright) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .hero-subtitle { font-size: 0.85rem; color: var(--text-muted); font-weight: 400; margin-top: 0.5rem; }

    .metric-strip { display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid var(--border-subtle); overflow: hidden; }
    .metric-cell { padding: 1.1rem 0.8rem; border-right: 1px solid var(--border-subtle); min-width: 0; overflow: hidden; }
    .metric-cell:last-child { border-right: none; }
    .metric-label { font-family: 'JetBrains Mono', monospace; font-size: 0.55rem; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.3rem; white-space: nowrap; }
    .metric-value { font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--text-primary); line-height: 1.2; white-space: nowrap; }
    .metric-sub { font-size: 0.65rem; color: var(--accent-bright); font-weight: 500; margin-top: 0.1rem; white-space: nowrap; }
    @media (max-width: 480px) { .metric-cell { padding: 0.9rem 0.6rem; } .metric-value { font-size: 1.1rem; } .metric-label { font-size: 0.5rem; } .hero-title { font-size: 2.6rem; } .hero-content { padding: 2rem 1.25rem 1.5rem; } }

    .section-card { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 1.75rem; margin-bottom: 1rem; }
    .section-eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.75rem; }
    .desc-text { font-size: 0.92rem; line-height: 1.7; color: var(--text-secondary); }

    .dual-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
    .grid-panel { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 1.5rem; }
    .grid-panel-title { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 1rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border-subtle); }
    .grid-item { display: flex; align-items: flex-start; gap: 0.6rem; margin-bottom: 0.7rem; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.4; }
    .grid-item:last-child { margin-bottom: 0; }
    .grid-icon { width: 18px; height: 18px; min-width: 18px; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.12); border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 0.55rem; color: var(--accent-bright); margin-top: 1px; }

    div.stButton > button { background: var(--accent) !important; color: white !important; border: none !important; border-radius: var(--radius-md) !important; padding: 0.85rem 2rem !important; font-family: 'Sora', sans-serif !important; font-weight: 600 !important; font-size: 0.9rem !important; width: 100% !important; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important; }
    div.stButton > button:hover { background: #2563EB !important; box-shadow: 0 4px 24px rgba(59,130,246,0.3) !important; transform: translateY(-1px) !important; }

    .form-card { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-xl); padding: 2rem; margin-bottom: 1rem; }
    .form-title { font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em; margin-bottom: 0.25rem; }
    .form-subtitle { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1.5rem; }
    .form-divider { height: 1px; background: var(--border-subtle); margin: 1.25rem 0; }
    .form-section-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem; }

    .stTextInput input, .stTextArea textarea { background: var(--bg-input) !important; border: 1px solid var(--border-mid) !important; border-radius: var(--radius-sm) !important; color: var(--text-primary) !important; font-family: 'Sora', sans-serif !important; font-size: 0.88rem !important; padding: 0.65rem 0.9rem !important; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px var(--accent-glow) !important; }
    .stSelectbox div[data-baseweb="select"] { background: var(--bg-input) !important; border-radius: var(--radius-sm) !important; }
    .stSelectbox div[data-baseweb="select"] > div { background: var(--bg-input) !important; border: 1px solid var(--border-mid) !important; border-radius: var(--radius-sm) !important; color: var(--text-primary) !important; font-family: 'Sora', sans-serif !important; font-size: 0.88rem !important; }
    label { color: var(--text-secondary) !important; font-family: 'Sora', sans-serif !important; font-weight: 400 !important; font-size: 0.8rem !important; }
    .stCheckbox label span { color: var(--text-secondary) !important; font-size: 0.85rem !important; }

    .upload-hint { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.75rem; }
    .stFileUploader > div { background: var(--bg-input) !important; border: 1px dashed var(--border-mid) !important; border-radius: var(--radius-md) !important; }

    .success-wrapper { text-align: center; padding: 3rem 2rem; }
    .success-icon { width: 72px; height: 72px; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.15); border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 1.8rem; margin-bottom: 1.5rem; }
    .success-title { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; }
    .success-desc { font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; max-width: 320px; margin: 0 auto 2rem; }

    .site-footer { text-align: center; padding: 1.5rem 0 0; }
    .footer-brand { font-family: 'Outfit', sans-serif; font-size: 0.7rem; font-weight: 600; color: var(--text-faint); letter-spacing: 0.15em; text-transform: uppercase; }
    .footer-sub { font-size: 0.65rem; color: var(--text-faint); margin-top: 0.2rem; opacity: 0.6; }

    .stAlert { border-radius: var(--radius-md) !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# --- HELPERS ---
def upload_photo_to_supabase(file, applicant_name):
    try:
        safe_name = applicant_name.strip().replace(" ", "_").lower()
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        ext = file.name.split(".")[-1].lower()
        path = f"installs/{safe_name}_{ts}_{file.name}"
        file_bytes = file.getbuffer()
        content_type = "image/jpeg" if ext == "jpg" else f"image/{ext}"
        supabase.storage.from_("applicant-photos").upload(path, file_bytes, {"content-type": content_type})
        return supabase.storage.from_("applicant-photos").get_public_url(path)
    except Exception as e:
        st.warning(f"Photo upload failed: {e}")
        return ""


def save_applicant(data):
    supabase.table("applicants").insert({
        "name": data["name"],
        "phone": data["phone"],
        "email": data["email"],
        "experience": data["experience"],
        "exp_types": data["exp_types"],
        "vehicle": data["vehicle"],
        "ladder": data["ladder"],
        "insurance": data["insurance"],
        "photo1_url": data.get("photo1_url", ""),
        "photo2_url": data.get("photo2_url", ""),
        "status": "NEW",
    }).execute()


# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "home"


# ═══════════════ HOME ═══════════════
if st.session_state.page == "home":

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

    if st.button("APPLY NOW →", use_container_width=True):
        st.session_state.page = "apply"
        st.rerun()


# ═══════════════ APPLICATION ═══════════════
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
        st.markdown('<div class="form-section-label">Contact Information</div>', unsafe_allow_html=True)
        name = st.text_input("Full name *")
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Phone number *")
        with col2:
            email = st.text_input("Email address")

        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-section-label">Experience</div>', unsafe_allow_html=True)
        experience = st.selectbox("Years of installation experience",
            ["Less than 1 year", "1–2 years", "3–5 years", "5+ years", "10+ years"])

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
        st.markdown('<div class="form-section-label">Equipment Check</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            vehicle = st.checkbox("Reliable truck / van / SUV")
            ladder = st.checkbox("24 ft+ fiberglass ladder")
        with col2:
            tools = st.checkbox("Basic installation tools")
            insurance = st.checkbox("Liability insurance")

        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-section-label">Previous Install Photos</div>', unsafe_allow_html=True)
        st.markdown('<div class="upload-hint">Upload up to 2 photos of your previous installation work (JPG, PNG)</div>', unsafe_allow_html=True)
        photo_col1, photo_col2 = st.columns(2)
        with photo_col1:
            photo1 = st.file_uploader("Photo 1", type=["jpg","jpeg","png"], key="photo1", label_visibility="collapsed")
        with photo_col2:
            photo2 = st.file_uploader("Photo 2", type=["jpg","jpeg","png"], key="photo2", label_visibility="collapsed")
        if photo1 or photo2:
            p1, p2 = st.columns(2)
            if photo1:
                with p1: st.image(photo1, use_container_width=True, caption="Photo 1")
            if photo2:
                with p2: st.image(photo2, use_container_width=True, caption="Photo 2")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("SUBMIT APPLICATION →", use_container_width=True)

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Name and phone number are required.")
            elif not vehicle or not ladder:
                st.error("A vehicle and ladder are required for this role.")
            else:
                exp_list = [x for x, c in [
                    ("Starlink", exp_starlink), ("DirecTV", exp_directv),
                    ("Dish Network", exp_dish), ("HughesNet", exp_hughesnet),
                    ("Low Voltage", exp_lowvoltage), ("TV Mounting", exp_tvmount),
                    ("Cable Installation", exp_cable), ("Other", exp_other),
                ] if c]

                photo1_url = upload_photo_to_supabase(photo1, name) if photo1 else ""
                photo2_url = upload_photo_to_supabase(photo2, name) if photo2 else ""

                save_applicant({
                    "name": name.strip(), "phone": phone.strip(), "email": email.strip(),
                    "experience": experience,
                    "exp_types": ", ".join(exp_list) if exp_list else "None selected",
                    "vehicle": "Yes" if vehicle else "No",
                    "ladder": "Yes" if ladder else "No",
                    "insurance": "Yes" if insurance else "No",
                    "photo1_url": photo1_url, "photo2_url": photo2_url,
                })
                st.session_state.page = "success"
                st.rerun()


# ═══════════════ SUCCESS ═══════════════
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

st.markdown("""
<div class="site-footer">
    <div class="footer-brand">VERGECOM LLC</div>
    <div class="footer-sub">Independent Contractor Opportunities</div>
</div>
""", unsafe_allow_html=True)
