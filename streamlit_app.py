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

# --- DYNAMIC CONTENT FETCH ---
@st.cache_data(ttl=10) # Checks for Admin Panel updates every 10 seconds
def fetch_live_content():
    try:
        res = supabase.table("site_settings").select("*").eq("id", 1).single().execute()
        return res.data
    except Exception:
        # Fallback if table isn't ready yet
        return {
            "hero_title": "Starlink Technician",
            "job_desc": "We're hiring experienced technicians to install Starlink satellite internet systems across the greater metro area. You'll work independently — handling residential installs from start to finish with full dispatch support.",
            "requirements": "Reliable truck, van, or SUV. 24 ft+ fiberglass ladder. Basic tools & power drill. Smartphone w/ data plan."
        }

live = fetch_live_content()

# --- STYLES ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@400;500;600&family=Sora:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-primary: #050505;
        --bg-card: #0C0C0C;
        --bg-input: #0F0F0F;
        --border-subtle: #1A1A1A;
        --accent: #3B82F6;
        --text-primary: #F5F5F5;
        --text-secondary: #9CA3AF;
        --text-muted: #6B7280;
    }

    .stApp { background: var(--bg-primary); font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 4rem !important; max-width: 640px !important; }

    .hero-wrapper { position: relative; overflow: hidden; border-radius: 28px; border: 1px solid var(--border-subtle); background: var(--bg-card); margin-bottom: 1.5rem; }
    .hero-content { position: relative; z-index: 2; padding: 3rem 2rem 2rem; }
    .hero-title { font-family: 'Outfit', sans-serif; font-size: 3.4rem; font-weight: 800; line-height: 1.0; color: var(--text-primary); margin: 0; }
    .hero-title span { color: var(--accent); }
    
    .metric-strip { display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid var(--border-subtle); }
    .metric-cell { padding: 1.1rem 0.8rem; border-right: 1px solid var(--border-subtle); text-align: center; }
    .metric-label { font-size: 0.6rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; }
    .metric-value { font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }

    .section-card { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 20px; padding: 2rem; margin-bottom: 1rem; }
    .section-eyebrow { font-size: 0.65rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.75rem; }
    .desc-text { font-size: 0.95rem; line-height: 1.7; color: var(--text-secondary); }

    div.stButton > button { background: var(--accent) !important; color: white !important; border-radius: 12px !important; padding: 0.75rem !important; width: 100% !important; font-weight: 600 !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# --- HELPERS ---
def upload_photo_to_supabase(file, applicant_name):
    try:
        safe_name = applicant_name.strip().replace(" ", "_").lower()
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        ext = file.name.split(".")[-1].lower()
        path = f"installs/{safe_name}_{ts}_{file.name}"
        file_bytes = bytes(file.getbuffer())
        supabase.storage.from_("applicant-photos").upload(path, file_bytes, file_options={"content-type": f"image/{ext}"})
        return supabase.storage.from_("applicant-photos").get_public_url(path)
    except Exception: return ""

def save_applicant(data):
    try:
        supabase.table("applicants").insert({**data, "status": "NEW"}).execute()
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

# --- SESSION STATE ---
if "page" not in st.session_state: st.session_state.page = "home"

# ═══════════════ HOME (DYNAMIC) ═══════════════
if st.session_state.page == "home":
    # Hero Title is now dynamic
    st.markdown(f"""
    <div class="hero-wrapper">
        <div class="hero-content">
            <div style="font-size:0.7rem; color:#4ADE80; font-weight:700; margin-bottom:1rem;">● HIRING NOW</div>
            <div class="hero-title">{live['hero_title']}</div>
            <div style="color:var(--text-muted); margin-top:1rem; font-size:0.9rem;">Independent Contractor Opportunity • Flexible Schedule</div>
        </div>
        <div class="metric-strip">
            <div class="metric-cell"><div class="metric-label">Earnings</div><div class="metric-value">$1,500+</div></div>
            <div class="metric-cell"><div class="metric-label">Start</div><div class="metric-value">Immediate</div></div>
            <div class="metric-cell"><div class="metric-label">Type</div><div class="metric-value">1099</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Job Description is now dynamic
    st.markdown(f"""
    <div class="section-card">
        <div class="section-eyebrow">// OPPORTUNITY OVERVIEW</div>
        <div class="desc-text">{live['job_desc']}</div>
    </div>
    <div class="section-card">
        <div class="section-eyebrow">// MINIMUM REQUIREMENTS</div>
        <div class="desc-text">{live['requirements']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("START APPLICATION →", use_container_width=True):
        st.session_state.page = "apply"
        st.rerun()

# ═══════════════ APPLICATION FORM ═══════════════
elif st.session_state.page == "apply":
    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown('<div style="padding:1rem 0;"><h3>Technician Onboarding</h3></div>', unsafe_allow_html=True)

    with st.form("app_form"):
        st.write("**Personal Information**")
        name = st.text_input("Full Name *")
        col1, col2 = st.columns(2)
        phone = col1.text_input("Phone Number *")
        email = col2.text_input("Email Address")

        st.write("---")
        st.write("**Service Area**")
        state = st.selectbox("Primary State *", ["Alabama", "Florida", "Georgia", "Mississippi", "North Carolina", "South Carolina", "Tennessee", "Texas"])
        counties = st.text_area("Counties Covered *")
        radius = st.number_input("Service Radius (Miles)", value=50)

        st.write("---")
        st.write("**Assets & Experience**")
        experience = st.selectbox("Experience Level", ["< 1 Year", "1-3 Years", "3-5 Years", "5+ Years"])
        
        c1, c2 = st.columns(2)
        v = c1.checkbox("I have a reliable truck/van")
        l = c2.checkbox("I have a 24ft+ fiberglass ladder")
        
        st.write("---")
        st.write("**Install Photos**")
        p1 = st.file_uploader("Upload Work Sample 1", type=['jpg','png'])
        p2 = st.file_uploader("Upload Work Sample 2", type=['jpg','png'])

        if st.form_submit_button("SUBMIT APPLICATION"):
            if not name or not phone or not counties:
                st.error("Please fill in all required fields (*)")
            else:
                p1_url = upload_photo_to_supabase(p1, name) if p1 else ""
                p2_url = upload_photo_to_supabase(p2, name) if p2 else ""
                
                success = save_applicant({
                    "name": name, "phone": phone, "email": email,
                    "state": state, "counties": counties, "radius": radius,
                    "experience": experience, "vehicle": "Yes" if v else "No",
                    "ladder": "Yes" if l else "No",
                    "photo1_url": p1_url, "photo2_url": p2_url
                })
                if success:
                    st.session_state.page = "success"
                    st.rerun()

elif st.session_state.page == "success":
    st.balloons()
    st.success("Application Submitted! Our team will contact you within 48 hours.")
    if st.button("Return Home"):
        st.session_state.page = "home"
        st.rerun()
