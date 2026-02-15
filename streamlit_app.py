import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom Careers", page_icon="📡", layout="centered")

# --- MODERN DARK THEME CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }

    /* Main Container */
    .main-container {
        background-color: #1A1C23;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #2D3748;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }

    /* Typography */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        color: #A0AEC0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Section Titles */
    .section-title {
        color: #63B3ED;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* Cards / Info Boxes */
    .info-card {
        background-color: #2D3748;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #4A5568;
        height: 100%;
        transition: transform 0.2s;
    }
    .info-card:hover {
        transform: translateY(-2px);
        border-color: #63B3ED;
    }
    .info-label {
        color: #A0AEC0;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .info-value {
        color: #FFFFFF;
        font-size: 1.2rem;
        font-weight: 700;
    }

    /* Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #FFFFFF !important;
        border: 2px solid #3182CE !important;
        border-radius: 50px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        text-transform: none !important;
        width: auto !important;
        min-width: 150px;
    }
    div.stButton > button:hover {
        background-color: #3182CE !important;
        box-shadow: 0 0 15px rgba(49, 130, 206, 0.4);
        border-color: #3182CE !important;
    }
    
    /* Primary Action Button (Full Width) */
    .apply-btn div.stButton > button {
        width: 100% !important;
        background-color: #3182CE !important;
        margin-top: 20px;
    }

    /* Form Inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea, .stMultiSelect div[data-baseweb="select"] {
        background-color: #2D3748 !important;
        color: #FFFFFF !important;
        border: 1px solid #4A5568 !important;
        border-radius: 10px !important;
    }
    
    .stTextInput label, .stSelectbox label, .stTextArea label, .stMultiSelect label, .stRadio label {
        color: #A0AEC0 !important;
        font-weight: 500 !important;
    }

    /* Radio Group */
    div[role="radiogroup"] {
        background-color: #2D3748;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4A5568;
    }

    /* Success Message */
    .success-box {
        background: linear-gradient(135deg, #2D3748 0%, #1A1C23 100%);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #48BB78;
        text-align: center;
        margin-top: 30px;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- DATABASE FUNCTIONS ---
def init_db():
    conn = sqlite3.connect('vergecom_candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applicants 
                 (id INTEGER PRIMARY KEY, 
                  name TEXT, phone TEXT, email TEXT, city TEXT, state TEXT, zip TEXT,
                  skills TEXT, years_exp TEXT, roof_work TEXT,
                  vehicle TEXT, ladder TEXT, license TEXT, tools TEXT,
                  insurance TEXT, service_area TEXT, start_date TEXT,
                  status TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_applicant(data, status):
    conn = sqlite3.connect('vergecom_candidates.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO applicants 
        (name, phone, email, city, state, zip, skills, years_exp, roof_work,
         vehicle, ladder, license, tools, insurance, service_area, start_date, status, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (data['name'], data['phone'], data['email'], data['city'], data['state'], data['zip'],
         str(data['skills']), data['years_exp'], data['roof_work'],
         data['vehicle'], data['ladder'], data['license'], str(data['tools']),
         data['insurance'], data['service_area'], data['start_date'], status, datetime.now()))
    conn.commit()
    conn.close()

init_db()

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# ==========================================
# PAGE 1: JOB DESCRIPTION
# ==========================================
if st.session_state.page == 'landing':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("<h1>Starlink Installation Technician</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Vergecom LLC • Independent Contractor (1099)</p>", unsafe_allow_html=True)

    # Info Grid
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-label">Compensation</div>
            <div class="info-value">$1,200 - $1,800 / Week</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-label">Location</div>
            <div class="info-value">Greater Metro Area</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Position Summary</div>", unsafe_allow_html=True)
    st.write("Vergecom is seeking professional Field Technicians to install and service Starlink satellite systems for residential and commercial customers. This is a high-volume, piece-rate position requiring reliable transportation and professional tools.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Key Responsibilities</div>", unsafe_allow_html=True)
        st.markdown("""
        - 3-6 residential installs daily
        - Roof & siding mounting
        - Cable running & termination
        - Router configuration
        """)
    with col2:
        st.markdown("<div class='section-title'>Requirements</div>", unsafe_allow_html=True)
        st.markdown("""
        - Truck/Van/SUV (Must carry 28ft ladder)
        - 28ft fiberglass extension ladder
        - Full set of professional tools
        - General Liability Insurance
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="apply-btn">', unsafe_allow_html=True)
    if st.button("Apply Now", use_container_width=True):
        st.session_state.page = 'application'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: APPLICATION FORM
# ==========================================
elif st.session_state.page == 'application':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if st.button("← Back"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("<h2>Application Form</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Please provide your professional details below.</p>", unsafe_allow_html=True)

    with st.form(key="app_form"):
        st.markdown("<div class='section-title'>1. Personal Information</div>", unsafe_allow_html=True)
        name = st.text_input("Full Legal Name")
        col1, col2 = st.columns(2)
        phone = col1.text_input("Phone Number")
        email = col2.text_input("Email Address")
        
        col1, col2, col3 = st.columns(3)
        city = col1.text_input("City")
        state = col2.text_input("State")
        zip_code = col3.text_input("Zip")

        st.markdown("<div class='section-title'>2. Experience & Skills</div>", unsafe_allow_html=True)
        SKILLS = ["Satellite (DirecTV/Dish)", "Starlink", "TV Mounting", "Security Cameras", "Low Voltage", "Smart Home"]
        skills = st.multiselect("Select your expertise", SKILLS)
        
        col1, col2 = st.columns(2)
        years = col1.selectbox("Years of Experience", ["Select", "< 1 year", "1-2 years", "3-5 years", "5+ years"])
        roof_work = col2.radio("Comfortable on roofs?", ["Yes", "Limited", "No"], horizontal=True)

        st.markdown("<div class='section-title'>3. Equipment & Logistics</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        vehicle = col1.radio("Do you have a Truck/Van/SUV?", ["Yes", "No"], horizontal=True)
        ladder = col2.radio("Do you have a 28ft ladder?", ["Yes", "No"], horizontal=True)
        
        col1, col2 = st.columns(2)
        license_v = col1.radio("Valid Driver's License?", ["Yes", "No"], horizontal=True)
        insurance = col2.radio("Liability Insurance?", ["Yes", "Will Obtain", "No"], horizontal=True)
        
        service_area = st.text_area("Service Counties", placeholder="e.g., Miami-Dade, Broward...")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Application")

        if submitted:
            if not name or not phone or not email:
                st.error("Please fill in all required fields.")
            elif vehicle == "No" or ladder == "No":
                st.warning("Minimum equipment requirements not met.")
            else:
                data = {
                    "name": name, "phone": phone, "email": email,
                    "city": city, "state": state, "zip": zip_code,
                    "skills": skills, "years_exp": years, "roof_work": roof_work,
                    "vehicle": vehicle, "ladder": ladder, "license": license_v,
                    "tools": [], "insurance": insurance,
                    "service_area": service_area, "start_date": "Immediate"
                }
                save_applicant(data, "QUALIFIED")
                st.session_state.page = 'success'
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 3: SUCCESS
# ==========================================
elif st.session_state.page == 'success':
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: #48BB78 !important;'>Application Submitted!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2rem; color: #E0E0E0;'>Thank you for your interest in Vergecom. Our hiring team will review your application and contact you shortly.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Return Home"):
        st.session_state.page = 'landing'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
