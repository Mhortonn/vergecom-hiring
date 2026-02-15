import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom Careers", page_icon="📡", layout="centered")

# --- CUSTOM CSS (STRICT CORPORATE BLACK & WHITE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* 1. GLOBAL RESET */
    .stApp {
        background-color: #FFFFFF; /* Pure White Background */
        font-family: 'Inter', sans-serif;
        color: #000000;
    }

    /* 2. MAIN CONTAINER BORDER */
    .main-container {
        border: 2px solid #000000;
        padding: 40px;
        margin-top: 20px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        background-color: #FFFFFF;
    }

    /* 3. TYPOGRAPHY */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: -0.5px;
    }
    
    p, li, label, .stMarkdown, .stText, .stSelectbox, .stMultiselect {
        color: #000000 !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
    }

    /* 4. BUTTONS (BLACK & WHITE) */
    .stButton button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 0px !important; /* Square corners */
        border: 2px solid #000000 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        padding: 14px 28px !important;
        transition: all 0.2s;
        width: 100%;
        letter-spacing: 0.5px;
    }
    .stButton button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
    }

    /* 5. INPUT FIELDS */
    .stTextInput input, .stSelectbox div, .stTextArea textarea, .stMultiselect div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 0px !important; /* Square inputs */
        padding: 10px !important;
    }
    
    .stTextInput label, .stSelectbox label, .stTextArea label, .stMultiselect label, .stRadio label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* 6. RADIO BUTTONS */
    .stRadio div[role="radiogroup"] {
        border: 1px solid #000000;
        padding: 12px;
        background-color: #FFFFFF;
    }
    
    .stRadio div[role="radiogroup"] label {
        color: #000000 !important;
    }

    /* 7. DIVIDERS */
    hr {
        border-top: 2px solid #000000 !important;
        margin: 30px 0;
    }

    /* 8. HEADER STYLES */
    .corporate-header {
        text-align: center;
        border-bottom: 2px solid black;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }
    
    .corporate-header h1 {
        margin: 0;
        font-size: 36px;
    }
    
    .corporate-header p {
        margin: 5px 0 0 0;
        font-weight: 600;
    }
    
    /* 9. INFO GRID */
    .info-grid {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
    }
    
    .info-box {
        flex: 1;
        border: 1px solid #000000;
        padding: 15px;
        text-align: center;
    }
    
    .info-box strong {
        display: block;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    /* 10. QUALIFYING BOX */
    .qualifying-box {
        border: 2px solid #000000;
        padding: 15px;
        margin: 20px 0;
        background-color: #FFFFFF;
    }
    
    .qualifying-box p {
        margin: 0;
        font-weight: 700;
    }
    
    /* 11. SUCCESS MESSAGE */
    .success-container {
        border: 2px solid #000000;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
        background-color: #FFFFFF;
    }
    
    .success-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .success-text {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* 12. BACK BUTTON */
    .back-button {
        border: 1px solid #000000 !important;
        background-color: transparent !important;
        color: #000000 !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
    }
    
    .back-button:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* 13. HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 14. SECTION TITLES */
    .section-title {
        font-weight: 700;
        font-size: 20px;
        margin: 30px 0 20px 0;
        border-bottom: 1px solid #000000;
        padding-bottom: 8px;
    }
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
# PAGE 1: JOB DESCRIPTION (CORPORATE)
# ==========================================
if st.session_state.page == 'landing':
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # HEADER
    st.markdown("""
    <div class="corporate-header">
        <h1>STARLINK INSTALLATION TECHNICIAN</h1>
        <p>VERGECOM LLC | INDEPENDENT CONTRACTOR (1099)</p>
    </div>
    """, unsafe_allow_html=True)

    # INFO GRID
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-box">
            <strong>COMPENSATION</strong>
            $1,200 - $1,800 / WEEK
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-box">
            <strong>LOCATION</strong>
            GREATER METRO AREA
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

    # DESCRIPTION
    st.markdown("""
    <div class="section-title">POSITION SUMMARY</div>
    <p style="margin-bottom: 25px;">
        Vergecom is seeking professional Field Technicians to install and service Starlink satellite systems for 
        residential and commercial customers. This is a high-volume, piece-rate position requiring reliable 
        transportation and professional tools. This <strong>1099 Independent Contractor</strong> role offers 
        flexibility and uncapped earning potential.
    </p>
    
    <div class="section-title">KEY RESPONSIBILITIES</div>
    <ul style="margin-bottom: 25px;">
        <li>Complete daily route of 3-6 residential installations.</li>
        <li>Mount Starlink hardware to roofs, siding, or poles using professional techniques.</li>
        <li>Run and terminate RG6/Cat5 cabling cleanly and securely.</li>
        <li>Configure customer routers and verify system connectivity.</li>
        <li>Conduct site surveys to determine optimal equipment placement.</li>
        <li>Troubleshoot and resolve signal issues on-site.</li>
    </ul>
    
    <div class="section-title">MINIMUM REQUIREMENTS</div>
    <ul style="margin-bottom: 25px;">
        <li><strong>Vehicle:</strong> Truck, Van, or SUV (Must carry 28ft ladder).</li>
        <li><strong>Ladder:</strong> 28ft fiberglass extension ladder in good condition.</li>
        <li><strong>Tools:</strong> Power Drill, Impact Driver, Hand Tools, Crimper, Cable Tester.</li>
        <li><strong>License:</strong> Valid Driver's License & Auto Insurance.</li>
        <li><strong>Insurance:</strong> General Liability Policy (Required).</li>
        <li><strong>Physical:</strong> Comfortable working at heights, on roofs, and in confined spaces.</li>
    </ul>
    
    <div class="section-title">SCHEDULE & TERRITORY</div>
    <p>
        Work is dispatched within the Greater Metropolitan Area. You control your schedule—choose the days 
        and hours that work best for you. Weekend availability can increase earnings.
    </p>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("APPLY NOW", use_container_width=True):
        st.session_state.page = 'application'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: APPLICATION FORM (CORPORATE)
# ==========================================
elif st.session_state.page == 'application':
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← RETURN", key="back", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
    
    st.markdown("""
    <h2 style="margin-top: 20px; border-bottom: 2px solid black; padding-bottom: 10px;">CANDIDATE APPLICATION</h2>
    <p style="margin-bottom: 30px;">Starlink Installation Technician • Independent Contractor (1099)</p>
    """, unsafe_allow_html=True)

    # FORM
    with st.form(key="application_form"):
        # 1. CONTACT INFORMATION
        st.markdown("### 1. CONTACT INFORMATION")
        name = st.text_input("FULL LEGAL NAME *")
        
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("PHONE NUMBER *")
        with col2:
            email = st.text_input("EMAIL ADDRESS")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            city = st.text_input("CITY *")
        with col2:
            state = st.text_input("STATE *")
        with col3:
            zip_code = st.text_input("ZIP CODE *")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 2. PROFESSIONAL EXPERIENCE
        st.markdown("### 2. PROFESSIONAL EXPERIENCE")
        
        SKILLS = [
            "Satellite systems (DirecTV/Dish)",
            "Starlink installation",
            "TV mounting",
            "Security cameras",
            "Low voltage wiring (Cat5/Coax)",
            "Smart home systems"
        ]
        skills = st.multiselect("SELECT RELEVANT EXPERIENCE *", SKILLS)
        
        col1, col2 = st.columns(2)
        with col1:
            years = st.selectbox("YEARS OF EXPERIENCE *", ["Select", "< 1 year", "1-2 years", "3-5 years", "5+ years"])
        with col2:
            roof_work = st.radio("COMFORTABLE ON ROOFS? *", ["Yes", "Limited", "No"], horizontal=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)

        # 3. VEHICLE & EQUIPMENT (Qualifying Questions)
        st.markdown("### 3. VEHICLE & EQUIPMENT")
        st.markdown('<div class="qualifying-box"><p>⚠️ MINIMUM REQUIREMENTS TO QUALIFY</p></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            vehicle = st.radio("DO YOU HAVE A TRUCK/VAN/SUV? *", ["Yes", "No"], horizontal=True)
            ladder = st.radio("DO YOU HAVE A 28FT+ LADDER? *", ["Yes", "No"], horizontal=True)
        with col2:
            license_valid = st.radio("VALID DRIVER'S LICENSE? *", ["Yes", "No"], horizontal=True)
        
        TOOLS = ["Drill", "Impact Driver", "Crimper", "Cable Tester", "Fish Tape", "Signal Meter"]
        tools = st.multiselect("TOOLS YOU OWN *", TOOLS)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 4. REQUIREMENTS & LOGISTICS
        st.markdown("### 4. REQUIREMENTS & LOGISTICS")
        
        col1, col2 = st.columns(2)
        with col1:
            insurance = st.radio("GENERAL LIABILITY INSURANCE? *", ["Yes", "Will Obtain", "No"], horizontal=True)
        with col2:
            start_date = st.radio("HOW SOON CAN YOU START? *", ["Immediately", "1-2 Weeks", "2+ Weeks"], horizontal=True)
        
        service_area = st.text_area("COUNTIES YOU ARE WILLING TO COVER *", placeholder="e.g., Miami-Dade, Broward, Palm Beach", height=80)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Disclaimer
        st.markdown("""
            <p style="text-align: center; font-size: 12px; color: #666;">
                By submitting this application, you confirm that the information provided is accurate and complete.
                Vergecom LLC is an equal opportunity employer.
            </p>
        """, unsafe_allow_html=True)
        
        # Submit button
        submitted = st.form_submit_button("SUBMIT APPLICATION", use_container_width=True)
        
        if submitted:
            # Validation
            if not name or not phone or not city or not state or not zip_code:
                st.error("⚠️ PLEASE COMPLETE ALL CONTACT INFORMATION FIELDS.")
            elif not skills:
                st.error("⚠️ PLEASE SELECT AT LEAST ONE SKILL AREA.")
            elif years == "Select":
                st.error("⚠️ PLEASE SELECT YOUR YEARS OF EXPERIENCE.")
            elif vehicle == "No" or ladder == "No" or license_valid == "No":
                st.error("⚠️ YOU MUST MEET THE MINIMUM VEHICLE AND EQUIPMENT REQUIREMENTS TO QUALIFY.")
            elif not tools:
                st.error("⚠️ PLEASE SELECT THE TOOLS YOU OWN.")
            elif insurance == "No":
                st.error("⚠️ GENERAL LIABILITY INSURANCE IS REQUIRED FOR THIS POSITION.")
            elif not service_area:
                st.error("⚠️ PLEASE ENTER THE COUNTIES YOU ARE WILLING TO COVER.")
            else:
                # Determine status
                status = "QUALIFIED"
                if years == "< 1 year" or len(skills) < 2:
                    status = "REVIEW NEEDED"
                
                # Save to database
                data = {
                    "name": name, "phone": phone, "email": email,
                    "city": city, "state": state, "zip": zip_code,
                    "skills": skills, "years_exp": years, "roof_work": roof_work,
                    "vehicle": vehicle, "ladder": ladder, "license": license_valid,
                    "tools": tools, "insurance": insurance,
                    "service_area": service_area, "start_date": start_date
                }
                save_applicant(data, status)
                
                # Success message
                st.balloons()
                st.markdown(f"""
                    <div class="success-container">
                        <div class="success-title">APPLICATION RECEIVED</div>
                        <div class="success-text">
                            Thank you, {name}. Your application for <strong>Starlink Installation Technician</strong> has been submitted.<br><br>
                            A Vergecom LLC hiring manager will review your qualifications and contact you at <strong>{phone}</strong> within 2-3 business days.<br><br>
                            STATUS: <strong>{status}</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
