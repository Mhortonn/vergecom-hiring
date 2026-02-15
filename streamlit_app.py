import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom | Starlink Technician", page_icon="🛰️", layout="centered")

# --- CLEAN, MODERN CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #0A0A0A;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 700px !important;
    }

    .main-card {
        background: #111111;
        border: 1px solid #222222;
        border-radius: 20px;
        padding: 2rem;
    }

    h1 {
        color: #FFFFFF !important;
        font-size: 2.8rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        color: #FFFFFF !important;
        font-size: 1.4rem !important;
        font-weight: 500 !important;
        margin: 1.5rem 0 1rem 0 !important;
    }

    .badge {
        background: #1A5CFF;
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        display: inline-block;
        margin-bottom: 1rem;
        letter-spacing: 0.3px;
    }

    .stats-grid {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }

    .stat-box {
        background: #1A1A1A;
        border: 1px solid #2A2A2A;
        border-radius: 12px;
        padding: 1rem;
        flex: 1;
    }

    .stat-label {
        color: #888888;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    .stat-value {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 600;
        line-height: 1.2;
    }

    .stat-note {
        color: #1A5CFF;
        font-size: 0.7rem;
        font-weight: 500;
    }

    .job-description {
        color: #CCCCCC;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 1.5rem 0;
        padding: 1rem 0;
        border-top: 1px solid #222222;
        border-bottom: 1px solid #222222;
    }

    .list-header {
        color: #FFFFFF;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    .list-item {
        color: #AAAAAA;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }

    .list-item:before {
        content: "•";
        color: #1A5CFF;
        font-weight: bold;
        margin-right: 0.75rem;
    }

    div.stButton > button {
        background: #1A5CFF !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: 0.2s !important;
    }

    div.stButton > button:hover {
        background: #0045E6 !important;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background: #1A1A1A !important;
        border: 1px solid #2A2A2A !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        padding: 0.6rem 1rem !important;
    }

    label {
        color: #CCCCCC !important;
        font-weight: 400 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.25rem !important;
    }

    .back-button {
        color: #888888;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        cursor: pointer;
    }

    .back-button:hover {
        color: #1A5CFF;
    }

    hr {
        border-color: #222222;
        margin: 1.5rem 0;
    }

    .success-message {
        text-align: center;
        padding: 2rem;
    }

    .success-message h3 {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 500;
        margin: 1rem 0;
    }

    .footer-note {
        color: #555555;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 2rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applicants
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT,
                  experience TEXT, vehicle TEXT, ladder TEXT, insurance TEXT,
                  status TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_applicant(data):
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute("""INSERT INTO applicants 
                 (name, phone, email, experience, vehicle, ladder, insurance, status, timestamp) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (data['name'], data['phone'], data['email'], data['experience'], 
         data['vehicle'], data['ladder'], data['insurance'], 'NEW', datetime.now()))
    conn.commit()
    conn.close()

init_db()

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- HOME PAGE ---
if st.session_state.page == 'home':
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        st.markdown('<span class="badge">NOW HIRING</span>', unsafe_allow_html=True)
        st.markdown("<h1>Starlink<br>Technician</h1>", unsafe_allow_html=True)
        
        # Stats
        st.markdown("""
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-label">EARNING POTENTIAL</div>
                <div class="stat-value">$1,400</div>
                <div class="stat-note">avg weekly</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">START DATE</div>
                <div class="stat-value">Immediate</div>
                <div class="stat-note">flexible schedule</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">ROLE TYPE</div>
                <div class="stat-value">1099</div>
                <div class="stat-note">independent</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Description
        st.markdown("""
        <div class="job-description">
            We're looking for experienced technicians to install Starlink satellite systems 
            in the greater metro area. You'll handle 3-5 residential installs daily, working 
            independently with our dispatch support. This is a performance-based role with 
            unlimited earning potential.
        </div>
        """, unsafe_allow_html=True)
        
        # Two columns for requirements
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="list-header">WHAT YOU'LL DO</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">Residential Starlink installations</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">Roof mounting & cable routing</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">Signal optimization & testing</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">Customer education</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="list-header">WHAT YOU NEED</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">Reliable truck/van/SUV</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">24ft+ fiberglass ladder</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">Basic tools & drill</div>', unsafe_allow_html=True)
            st.markdown('<div class="list-item">Smartphone</div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if st.button("APPLY NOW", use_container_width=True):
            st.session_state.page = 'apply'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- APPLICATION PAGE ---
elif st.session_state.page == 'apply':
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        if st.button("← BACK", use_container_width=False):
            st.session_state.page = 'home'
            st.rerun()
        
        st.markdown("<h2>Application Form</h2>", unsafe_allow_html=True)
        
        with st.form("application_form"):
            # Basic Info
            st.markdown("**Basic Information**")
            name = st.text_input("Full name *")
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Phone *")
            with col2:
                email = st.text_input("Email")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Experience**")
            experience = st.selectbox(
                "Years of installation experience",
                ["Less than 1 year", "1-2 years", "3-5 years", "5+ years", "10+ years"]
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Equipment Checklist**")
            
            col1, col2 = st.columns(2)
            with col1:
                vehicle = st.checkbox("I have a reliable truck/van/SUV")
                ladder = st.checkbox("I have a 24ft+ fiberglass ladder")
            with col2:
                tools = st.checkbox("I have basic installation tools")
                insurance = st.checkbox("I have liability insurance")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Submit
            submitted = st.form_submit_button("SUBMIT APPLICATION", use_container_width=True)
            
            if submitted:
                if not name or not phone:
                    st.error("Name and phone are required")
                elif not vehicle or not ladder:
                    st.error("You must have a vehicle and ladder to apply")
                else:
                    save_applicant({
                        'name': name,
                        'phone': phone,
                        'email': email,
                        'experience': experience,
                        'vehicle': 'Yes' if vehicle else 'No',
                        'ladder': 'Yes' if ladder else 'No',
                        'insurance': 'Yes' if insurance else 'No'
                    })
                    st.session_state.page = 'success'
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- SUCCESS PAGE ---
elif st.session_state.page == 'success':
    with st.container():
        st.markdown('<div class="main-card success-message">', unsafe_allow_html=True)
        
        st.markdown("✅")
        st.markdown("<h3>Application<br>Received</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #AAAAAA; margin: 1.5rem 0;">
            Thanks for applying. Our team will review your information<br>
            and contact you within 2 business days.
        </p>
        """, unsafe_allow_html=True)
        
        if st.button("RETURN HOME", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer-note">
    Vergecom LLC • Independent Contractor Opportunities
</div>
""", unsafe_allow_html=True)
