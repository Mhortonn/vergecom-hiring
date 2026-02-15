import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom Careers", page_icon="📡", layout="centered")

# --- CUSTOM CSS (CORPORATE LOOK) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Clean white background */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content container */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* White card for all content */
    .corporate-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 50px 60px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08), 0 6px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #EAECF0;
        margin: 20px 0;
    }
    
    /* Company header */
    .company-header {
        text-align: center;
        margin-bottom: 40px;
        border-bottom: 2px solid #000000;
        padding-bottom: 30px;
    }
    
    .company-name {
        color: #000000;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
    
    .job-title {
        color: #000000;
        font-size: 42px;
        font-weight: 700;
        margin: 10px 0 5px 0;
        line-height: 1.2;
    }
    
    .job-type {
        color: #000000;
        font-size: 18px;
        font-weight: 400;
        margin-top: 5px;
        opacity: 0.8;
    }
    
    /* Section styles - ALL BLACK */
    .section-title {
        color: #000000;
        font-size: 20px;
        font-weight: 700;
        margin: 35px 0 20px 0;
        letter-spacing: -0.02em;
        border-bottom: 1px solid #000000;
        padding-bottom: 8px;
    }
    
    .section-title:first-of-type {
        margin-top: 10px;
    }
    
    /* Text styles - ALL BLACK */
    .body-text {
        color: #000000;
        font-size: 16px;
        line-height: 1.7;
        margin-bottom: 20px;
        font-weight: 400;
    }
    
    .body-text strong {
        color: #000000;
        font-weight: 700;
    }
    
    /* List styles - ALL BLACK */
    .corporate-list {
        margin: 15px 0 25px 0;
        padding-left: 25px;
        color: #000000;
        font-size: 16px;
        line-height: 1.8;
    }
    
    .corporate-list li {
        margin-bottom: 12px;
        color: #000000;
    }
    
    .corporate-list li strong {
        color: #000000;
        font-weight: 700;
    }
    
    /* Pay highlight */
    .pay-summary {
        background-color: #000000;
        border-radius: 16px;
        padding: 25px 30px;
        margin: 30px 0 20px 0;
        border: 1px solid #000000;
        text-align: center;
    }
    
    .pay-range {
        color: #FFFFFF;
        font-size: 36px;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 5px;
    }
    
    .pay-note {
        color: #FFFFFF;
        font-size: 16px;
        font-weight: 400;
        margin-top: 5px;
        opacity: 0.9;
    }
    
    /* Button styles */
    .stButton button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 20px 40px !important;
        border-radius: 12px !important;
        border: 2px solid #000000 !important;
        width: 100%;
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0 0 0 !important;
    }
    
    .stButton button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Form styles */
    .form-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid #EAECF0;
    }
    
    .form-title {
        color: #000000;
        font-size: 28px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .form-subtitle {
        color: #000000;
        font-size: 16px;
        text-align: center;
        margin-bottom: 40px;
        opacity: 0.8;
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF;
        border: 1.5px solid #000000;
        border-radius: 10px;
        padding: 12px;
        color: #000000;
        font-size: 15px;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #000000 !important;
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Labels */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* Radio and checkbox */
    .stRadio div[role="radiogroup"] {
        background-color: #F8FAFC;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #000000;
    }
    
    .stRadio div[role="radiogroup"] label {
        color: #000000 !important;
    }
    
    hr {
        margin: 30px 0;
        border-color: #000000;
        opacity: 0.2;
    }
    
    /* Success message */
    .success-container {
        background-color: #000000;
        border-radius: 20px;
        padding: 60px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid #000000;
        margin: 20px 0;
    }
    
    .success-title {
        color: #FFFFFF;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .success-text {
        color: #FFFFFF;
        font-size: 18px;
        line-height: 1.6;
        opacity: 0.9;
    }
    
    .success-text strong {
        color: #FFFFFF;
        font-weight: 700;
    }
    
    /* Subheaders */
    .stSubheader {
        color: #000000 !important;
        font-weight: 700 !important;
        border-bottom: 1px solid #000000;
        padding-bottom: 8px;
        margin-top: 30px !important;
    }
    
    /* Back button */
    .stButton button[key="Back"] {
        background-color: transparent !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
    }
    
    .stButton button[key="Back"]:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- DATABASE FUNCTIONS ---
def init_db():
    conn = sqlite3.connect('vergecom_candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applicants 
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, 
                  status TEXT, skills TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_applicant(data, status):
    conn = sqlite3.connect('vergecom_candidates.db')
    c = conn.cursor()
    c.execute("INSERT INTO applicants (name, phone, email, status, skills, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (data['name'], data['phone'], data['email'], status, str(data.get('skills', [])), datetime.now()))
    conn.commit()
    conn.close()

init_db()

# ==========================================
# PAGE 1: LANDING PAGE (ALL BLACK TEXT)
# ==========================================
if st.session_state.page == 'landing':
    
    # Main white container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
    
    # Company header
    st.markdown("""
        <div class="company-header">
            <div class="company-name">VERGECOM</div>
            <h1 class="job-title">Field Service Technician</h1>
            <div class="job-type">Independent Contractor • 1099 Position</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Pay summary (black background with white text)
    st.markdown("""
        <div class="pay-summary">
            <div class="pay-range">$1,200 – $1,800 per week</div>
            <div class="pay-note">Average weekly earnings for qualified technicians</div>
        </div>
    """, unsafe_allow_html=True)
    
    # About the Role
    st.markdown('<div class="section-title">About the Role</div>', unsafe_allow_html=True)
    st.markdown("""
        <p class="body-text">
            Vergecom is seeking professional, self-motivated Field Technicians to join our network of installation experts. 
            In this <strong>1099 Independent Contractor</strong> role, you'll install and service satellite systems for 
            residential and commercial customers. This position offers flexibility, autonomy, and uncapped earning potential 
            through our performance-based compensation model.
        </p>
    """, unsafe_allow_html=True)
    
    # Key Responsibilities
    st.markdown('<div class="section-title">Key Responsibilities</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="corporate-list">
            <li><strong>Site Assessment:</strong> Conduct thorough site surveys to determine optimal equipment placement</li>
            <li><strong>Installation:</strong> Mount hardware on roofs, siding, and poles using industry-standard techniques</li>
            <li><strong>Cabling:</strong> Route and terminate cables professionally, ensuring clean and secure installations</li>
            <li><strong>Configuration:</strong> Set up network equipment and verify system connectivity and performance</li>
            <li><strong>Troubleshooting:</strong> Diagnose and resolve signal issues and connectivity problems on-site</li>
            <li><strong>Documentation:</strong> Complete job reports and maintain accurate equipment inventory</li>
        </ul>
    """, unsafe_allow_html=True)
    
    # Requirements
    st.markdown('<div class="section-title">Requirements</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="corporate-list">
            <li><strong>Vehicle:</strong> Reliable truck, van, or SUV capable of transporting installation equipment</li>
            <li><strong>Ladder:</strong> 28ft fiberglass extension ladder in good condition</li>
            <li><strong>Tools:</strong> Standard installation tools including power drill, impact driver, and hand tools</li>
            <li><strong>Technology:</strong> Smartphone with data plan for dispatch and communication apps</li>
            <li><strong>Credentials:</strong> Valid driver's license and general liability insurance</li>
            <li><strong>Physical:</strong> Comfortable working at heights, on roofs, and in confined spaces</li>
        </ul>
    """, unsafe_allow_html=True)
    
    # Schedule
    st.markdown('<div class="section-title">Schedule & Territory</div>', unsafe_allow_html=True)
    st.markdown("""
        <p class="body-text">
            Work is dispatched within the Greater Metropolitan Area. Technicians complete an average of 3-6 installations per day.
            You control your schedule—choose the days and hours that work best for you. Weekend availability can increase earnings.
        </p>
    """, unsafe_allow_html=True)
    
    # Button
    if st.button("BECOME AN INSTALLER", use_container_width=True):
        st.session_state.page = 'application'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close corporate-card
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container

# ==========================================
# PAGE 2: APPLICATION FORM
# ==========================================
elif st.session_state.page == 'application':
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    # Back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back", key="Back", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
    
    # Form header
    st.markdown("""
        <div class="form-title">Installer Application</div>
        <div class="form-subtitle">Please complete all information below</div>
    """, unsafe_allow_html=True)
    
    # Contact Information
    st.subheader("Contact Information")
    name = st.text_input("Full name *")
    col1, col2 = st.columns(2)
    with col1:
        phone = st.text_input("Phone number *")
    with col2:
        email = st.text_input("Email address")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.text_input("City")
    with col2:
        state = st.text_input("State")
    with col3:
        zip_code = st.text_input("ZIP code")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Experience
    st.subheader("Experience")
    experience = st.selectbox("Years of installation experience *", 
                            ["Select", "Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "10+ years"])
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Equipment
    st.subheader("Equipment & Requirements")
    col1, col2 = st.columns(2)
    with col1:
        vehicle = st.radio("Reliable truck/van/SUV? *", ["Yes", "No"], horizontal=True)
        ladder = st.radio("Own 28ft+ ladder? *", ["Yes", "No"], horizontal=True)
    with col2:
        license_valid = st.radio("Valid driver's license? *", ["Yes", "No"], horizontal=True)
        height_work = st.radio("Comfortable with heights? *", ["Yes", "No"], horizontal=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Availability
    st.subheader("Availability")
    counties = st.text_area("Counties where you can work *", placeholder="e.g., Miami-Dade, Broward, Palm Beach")
    weekend = st.checkbox("Available for weekend work")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Submit
    if st.button("SUBMIT APPLICATION", use_container_width=True):
        if not name or not phone or experience == "Select" or vehicle == "No" or ladder == "No":
            st.error("⚠️ Please complete all required fields and ensure you meet the minimum requirements.")
        else:
            data = {"name": name, "phone": phone, "email": email, "skills": [], "experience": experience}
            save_applicant(data, "QUALIFIED")
            
            st.balloons()
            st.markdown(f"""
                <div class="success-container">
                    <div class="success-title">Application Received</div>
                    <div class="success-text">Thank you, {name}. A Vergecom representative will contact you at <strong>{phone}</strong> within 2 business days.</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("← Return to Job Description", use_container_width=True):
                st.session_state.page = 'landing'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close form-card
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
