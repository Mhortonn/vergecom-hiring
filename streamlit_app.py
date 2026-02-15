import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom Careers", page_icon="📡", layout="centered")

# --- ULTRA-PREMIUM CORPORATE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #111827, #05070A);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #94A3B8;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 800px !important;
    }

    .premium-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }

    h1 {
        color: #FFFFFF !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        line-height: 1.1 !important;
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .company-tag {
        color: #3B82F6;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        display: block;
    }

    .subtitle {
        color: #64748B;
        font-size: 1.25rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    .section-header {
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-top: 2.5rem;
        margin-bottom: 1.25rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .info-grid-container {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .info-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .info-box-label {
        color: #64748B;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .info-box-value {
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 700;
    }

    .requirement-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 0.75rem;
        color: #94A3B8;
        font-size: 0.95rem;
    }
    
    .requirement-item::before {
        content: "→";
        color: #3B82F6;
        margin-right: 0.75rem;
        font-weight: 800;
    }

    div.stButton > button {
        background: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3) !important;
    }
    
    div.stButton > button:hover {
        background: #2563EB !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        padding: 0.75rem 1rem !important;
    }
    
    label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect('vergecom_candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applicants 
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, city TEXT, state TEXT, zip TEXT,
                  skills TEXT, years_exp TEXT, roof_work TEXT, vehicle TEXT, ladder TEXT, license TEXT, tools TEXT,
                  insurance TEXT, service_area TEXT, start_date TEXT, status TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_applicant(data, status):
    conn = sqlite3.connect('vergecom_candidates.db')
    c = conn.cursor()
    c.execute("INSERT INTO applicants (name, phone, email, city, state, zip, skills, years_exp, roof_work, vehicle, ladder, license, tools, insurance, service_area, start_date, status, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (data['name'], data['phone'], data['email'], data['city'], data['state'], data['zip'], str(data['skills']), data['years_exp'], data['roof_work'], data['vehicle'], data['ladder'], data['license'], "[]", data['insurance'], data['service_area'], "Immediate", status, datetime.now()))
    conn.commit()
    conn.close()

init_db()

if 'page' not in st.session_state: st.session_state.page = 'landing'

# --- PAGES ---
if st.session_state.page == 'landing':
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<span class="company-tag">Vergecom LLC</span><h1>Starlink<br>Technician</h1><p class="subtitle">Join our elite field force as an Independent Contractor (1099).</p>', unsafe_allow_html=True)
    st.markdown('<div class="info-grid-container"><div class="info-box"><div class="info-box-label">Compensation</div><div class="info-box-value">$1,200 – $1,800 / Week</div></div><div class="info-box"><div class="info-box-label">Location</div><div class="info-box-value">Greater Metro Area</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Position Summary</div><p style="font-size: 1.1rem; line-height: 1.6; color: #94A3B8; margin-bottom: 2rem;">Vergecom is seeking professional Field Technicians to install and service Starlink satellite systems. This is a high-volume, performance-driven role for those with technical precision.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Responsibilities</div><div class="requirement-item">3-6 precision installs daily</div><div class="requirement-item">Advanced roof mounting</div><div class="requirement-item">Cable termination</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="section-header">Requirements</div><div class="requirement-item">Truck/Van/SUV</div><div class="requirement-item">28ft Fiberglass ladder</div><div class="requirement-item">Liability Insurance</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 3rem;">', unsafe_allow_html=True)
    if st.button("Begin Application"):
        st.session_state.page = 'application'
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

elif st.session_state.page == 'application':
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    if st.button("← Back"):
        st.session_state.page = 'landing'
        st.rerun()
    st.markdown('<h1>Apply Now</h1><p class="subtitle">Complete your professional profile below.</p>', unsafe_allow_html=True)
    with st.form("app"):
        st.markdown('<div class="section-header">1. Identity</div>', unsafe_allow_html=True)
        name = st.text_input("Full Name")
        c1, c2 = st.columns(2)
        phone = c1.text_input("Phone")
        email = c2.text_input("Email")
        st.markdown('<div class="section-header">2. Expertise</div>', unsafe_allow_html=True)
        skills = st.multiselect("Skills", ["Satellite", "Starlink", "TV Mounting", "Low Voltage"])
        years = st.selectbox("Experience", ["Select", "< 1 year", "1-2 years", "3-5 years", "5+ years"])
        st.markdown('<div class="section-header">3. Logistics</div>', unsafe_allow_html=True)
        v = st.radio("Truck/Van?", ["Yes", "No"], horizontal=True)
        l = st.radio("28ft Ladder?", ["Yes", "No"], horizontal=True)
        sub = st.form_submit_button("Submit Application")
        if sub:
            if not name or not phone: st.error("Fields required")
            else:
                save_applicant({"name":name,"phone":phone,"email":email,"city":"","state":"","zip":"","skills":skills,"years_exp":years,"roof_work":"","vehicle":v,"ladder":l,"license":"","insurance":"","service_area":""}, "PENDING")
                st.session_state.page = 'success'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'success':
    st.markdown('<div class="premium-card" style="text-align: center; padding: 5rem 2rem;"><h1>Success</h1><p class="subtitle">Application received. We will contact you shortly.</p>', unsafe_allow_html=True)
    if st.button("Home"):
        st.session_state.page = 'landing'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
