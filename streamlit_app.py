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
        margin-bottom: 30px;
        border-bottom: 2px solid #000000;
        padding-bottom: 30px;
    }
    
    .company-name {
        color: #000000;
        font-size: 16px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
    
    /* New styles for the white space */
    .starlink-title {
        color: #000000;
        font-size: 48px;
        font-weight: 700;
        margin: 5px 0 5px 0;
        line-height: 1.2;
        text-align: center;
        letter-spacing: -0.02em;
    }
    
    .vergecom-llc {
        color: #000000;
        font-size: 24px;
        font-weight: 400;
        margin-top: 5px;
        opacity: 0.8;
        text-align: center;
        letter-spacing: 1px;
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
    
    /* White space styling */
    .white-space-content {
        text-align: center;
        padding: 20px 0 30px 0;
        margin-bottom: 20px;
    }
    
    /* Qualifying questions highlight */
    .qualifying-box {
        background-color: #F8FAFC;
        border-left: 4px solid #000000;
        padding: 15px;
        margin: 20px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .qualifying-box p {
        margin: 0;
        color: #000000;
        font-weight: 500;
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

# ==========================================
# PAGE 1: LANDING PAGE
# ==========================================
if st.session_state.page == 'landing':
    
    # Main white container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
    
    # White space content with Starlink Installation Technician and Vergecom LLC
    st.markdown("""
        <div class="white-space-content">
            <div class="starlink-title">STARLINK INSTALLATION TECHNICIAN</div>
            <div class="vergecom-llc">VERGECOM LLC</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Company header
    st.markdown("""
        <div class="company-header">
            <div class="company-name">FIELD SERVICE TECHNICIAN</div>
            <div class="job-type">Independent Contractor • 1099 Position</div>
        </div>
    """, unsafe_allow_html=True)
    
    # About the Role
    st.markdown('<div class="section-title">About the Role</div>', unsafe_allow_html=True)
    st.markdown("""
        <p class="body-text">
            Vergecom is seeking professional, self-motivated Field Technicians to join our network of installation experts. 
            In this <strong>1099 Independent Contractor</strong> role, you'll install and service Starlink satellite systems for 
            residential and commercial customers. This position offers flexibility, autonomy, and uncapped earning potential 
            through our performance-based compensation model.
        </p>
    """, unsafe_allow_html=True)
    
    # Key Responsibilities
    st.markdown('<div class="section-title">Key Responsibilities</div>', unsafe_allow_html=True)
    st.markdown("""
        <ul class="corporate-list">
            <li><strong>Site Assessment:</strong> Conduct thorough site surveys to determine optimal Starlink equipment placement</li>
            <li><strong>Installation:</strong> Mount Starlink hardware on roofs, siding, and poles using industry-standard techniques</li>
            <li><strong>Cabling:</strong> Route and terminate cables professionally, ensuring clean and secure installations</li>
            <li><strong>Configuration:</strong> Set up Starlink network equipment and verify system connectivity and performance</li>
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
            Work is dispatched within the Greater Metropolitan Area. Technicians complete an average of 3-6 Starlink installations per day.
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
# PAGE 2: APPLICATION FORM (Hiring Manager Script)
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
        <div class="form-title">Starlink Installation Technician Application</div>
        <div class="form-subtitle">Independent Contractor (1099) • Vergecom LLC</div>
    """, unsafe_allow_html=True)
    
    # 1. CONTACT INFORMATION
    st.subheader("📋 Contact Information")
    
    name = st.text_input("Full Name *")
    
    col1, col2 = st.columns(2)
    with col1:
        phone = st.text_input("Phone Number *")
    with col2:
        email = st.text_input("Email Address")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.text_input("City *")
    with col2:
        state = st.text_input("State *")
    with col3:
        zip_code = st.text_input("Zip Code *")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 2. PROFESSIONAL EXPERIENCE
    st.subheader("🛠️ Professional Experience")
    
    # Multi-select Skills
    skills = st.multiselect(
        "Select your areas of experience *",
        [
            "Satellite systems (DirecTV/Dish)",
            "Starlink installation",
            "TV mounting",
            "Security cameras",
            "Low voltage wiring (Cat5/Coax)",
            "Smart home systems"
        ]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        # Years of Experience
        years_exp = st.selectbox(
            "Years of Experience *",
            ["Select", "< 1 year", "1-2 years", "3-5 years", "5+ years"]
        )
    
    with col2:
        # Roof Work Comfort Level
        roof_work = st.radio(
            "Are you comfortable working on roofs? *",
            ["Yes", "Limited", "No"],
            horizontal=True
        )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 3. VEHICLE & EQUIPMENT (Qualifying Questions)
    st.subheader("🚗 Vehicle & Equipment")
    st.markdown('<div class="qualifying-box"><p>⚠️ Minimum requirements to qualify for this position</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Vehicle
        vehicle = st.radio(
            "Do you have a reliable Truck, Van, or SUV? *",
            ["Yes", "No"],
            horizontal=True
        )
        
        # Ladder
        ladder = st.radio(
            "Do you own a 28ft+ extension ladder? *",
            ["Yes", "No"],
            horizontal=True
        )
    
    with col2:
        # Driver's License
        license_valid = st.radio(
            "Do you have a valid Driver's License? *",
            ["Yes", "No"],
            horizontal=True
        )
    
    # Tools Checklist
    tools = st.multiselect(
        "Checklist of required tools you own *",
        [
            "Drill",
            "Impact Driver",
            "Crimper",
            "Cable Tester",
            "Fish Tape",
            "Signal Meter"
        ]
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 4. REQUIREMENTS & LOGISTICS
    st.subheader("📦 Requirements & Logistics")
    
    col1, col2 = st.columns(2)
    with col1:
        # Insurance
        insurance = st.radio(
            "Do you have General Liability Insurance? *",
            ["Yes", "Will Obtain", "No"],
            horizontal=True
        )
    
    with col2:
        # Start Date
        start_date = st.radio(
            "How soon can you start? *",
            ["Immediately", "1-2 Weeks", "2+ Weeks"],
            horizontal=True
        )
    
    # Service Area
    service_area = st.text_area(
        "Counties you are willing to cover *",
        placeholder="e.g., Miami-Dade, Broward, Palm Beach",
        height=80
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
        <p style="color: #666; font-size: 14px; text-align: center;">
            By submitting this application, you confirm that the information provided is accurate and complete.
            Vergecom LLC is an equal opportunity employer.
        </p>
    """, unsafe_allow_html=True)
    
    # Submit button
    if st.button("SUBMIT APPLICATION", use_container_width=True):
        # Validation
        if not name or not phone or not city or not state or not zip_code:
            st.error("⚠️ Please complete all required contact information fields.")
        elif not skills:
            st.error("⚠️ Please select at least one skill area.")
        elif years_exp == "Select":
            st.error("⚠️ Please select your years of experience.")
        elif vehicle == "No" or ladder == "No" or license_valid == "No":
            st.error("⚠️ You must meet the minimum vehicle and equipment requirements to qualify.")
        elif not tools:
            st.error("⚠️ Please select the tools you own.")
        elif insurance == "No":
            st.error("⚠️ General Liability Insurance is required for this position.")
        elif not service_area:
            st.error("⚠️ Please enter the counties you are willing to cover.")
        else:
            # Determine status
            status = "QUALIFIED"
            if years_exp == "< 1 year" or len(skills) < 2:
                status = "REVIEW NEEDED"
            
            # Save to database
            data = {
                "name": name, "phone": phone, "email": email,
                "city": city, "state": state, "zip": zip_code,
                "skills": skills, "years_exp": years_exp, "roof_work": roof_work,
                "vehicle": vehicle, "ladder": ladder, "license": license_valid,
                "tools": tools, "insurance": insurance,
                "service_area": service_area, "start_date": start_date
            }
            save_applicant(data, status)
            
            # Success message
            st.balloons()
            st.markdown(f"""
                <div class="success-container">
                    <div class="success-title">Application Received</div>
                    <div class="success-text">
                        Thank you, {name}. Your application for <strong>Starlink Installation Technician</strong> has been submitted.<br><br>
                        A Vergecom LLC hiring manager will review your qualifications and contact you at <strong>{phone}</strong> within 2-3 business days.<br><br>
                        Status: <strong>{status}</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("← Submit Another Application", use_container_width=True):
                st.session_state.page = 'landing'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close form-card
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
