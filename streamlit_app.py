import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Starlink Tech Application",
    page_icon="📡",
    layout="centered"
)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('starlink_candidates.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            status TEXT,
            skills TEXT,
            vehicle TEXT,
            insurance TEXT,
            location TEXT,
            timestamp TEXT,
            full_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_applicant(data, status):
    conn = sqlite3.connect('starlink_candidates.db')
    c = conn.cursor()
    skills_str = ", ".join(data['skills'])
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_dump = str(data)
    c.execute('''INSERT INTO applicants 
                 (name, phone, email, status, skills, vehicle, insurance, location, timestamp, full_data) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['name'], data['phone'], data['email'], status, skills_str,
               data['vehicle'], data['insurance'], data['counties'], date_str, full_dump))
    conn.commit()
    conn.close()

init_db()

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* Global */
    .stApp {
        background-color: #F4F5F7;
    }
    .block-container {
        max-width: 720px !important;
        padding-top: 1rem !important;
    }

    /* Top brand bar */
    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #ECEEF2;
        margin-bottom: 8px;
    }
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 0.04em;
        color: #1A1D23;
    }
    .brand-logo .dim {
        font-weight: 400;
        color: #7A7F8D;
    }
    .brand-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        color: #7A7F8D;
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 36px 0 28px;
    }
    .hero-badge {
        display: inline-block;
        font-family: 'DM Sans', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #00875A;
        background: #E3FBF0;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 14px;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #1A1D23;
        margin: 0 0 8px;
        line-height: 1.2;
    }
    .hero p {
        font-family: 'DM Sans', sans-serif;
        font-size: 15px;
        color: #7A7F8D;
        margin: 0 0 24px;
    }
    .hero-stats {
        display: inline-flex;
        align-items: center;
        gap: 24px;
        background: #fff;
        border-radius: 14px;
        padding: 16px 32px;
        box-shadow: 0 1px 3px rgba(0,0,0,.06);
        border: 1px solid #ECEEF2;
    }
    .hero-stats .stat {
        text-align: center;
    }
    .hero-stats .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #1A1D23;
    }
    .hero-stats .stat-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 12px;
        color: #9CA1AE;
        margin-top: 2px;
    }
    .hero-stats .divider {
        width: 1px;
        height: 32px;
        background: #ECEEF2;
    }

    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    .section-num {
        width: 28px;
        height: 28px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        background: #0066FF;
        color: #fff;
    }
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #1A1D23;
    }

    /* Form styling - inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #FFFFFF !important;
        color: #1A1D23 !important;
        border-radius: 10px !important;
        border: 1.5px solid #E2E4E9 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        caret-color: #0066FF !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0066FF !important;
        box-shadow: 0 0 0 1px #0066FF !important;
        background-color: #FFFFFF !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9CA1AE !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1.5px solid #E2E4E9 !important;
    }
    .stSelectbox > div > div > div {
        background-color: #FFFFFF !important;
        color: #1A1D23 !important;
    }

    /* Multiselect */
    .stMultiSelect > div > div {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1.5px solid #E2E4E9 !important;
    }
    .stMultiSelect > div > div > div {
        background-color: #FFFFFF !important;
        color: #1A1D23 !important;
    }

    /* Select slider */
    .stSlider > div > div {
        background-color: transparent !important;
    }

    /* Radio buttons */
    .stRadio > div {
        gap: 8px;
    }
    .stRadio > div > label {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E4E9 !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
    }

    /* Checkboxes */
    .stCheckbox > label {
        color: #3A3F4B !important;
    }

    /* Labels */
    .stTextInput > label, .stTextArea > label, .stSelectbox > label,
    .stMultiSelect > label, .stRadio > label, .stCheckbox > label,
    .stSlider > label {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #4A4F5C !important;
    }

    /* Expander (section cards) */
    .stExpander {
        background: #fff;
        border: 1.5px solid #ECEEF2 !important;
        border-radius: 14px !important;
        margin-bottom: 12px;
    }
    .stExpander > details > summary {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }

    /* Container borders */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border-color: #ECEEF2 !important;
        background: #fff;
    }

    /* Submit button */
    .stFormSubmitButton > button {
        background: #0066FF !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 14px 24px !important;
        box-shadow: 0 2px 8px rgba(0,102,255,.25) !important;
        transition: all 0.2s ease !important;
    }
    .stFormSubmitButton > button:hover {
        background: #0052CC !important;
        transform: translateY(-1px);
    }

    /* Footer */
    .footer-text {
        text-align: center;
        font-family: 'DM Sans', sans-serif;
        font-size: 12px;
        color: #9CA1AE;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# THE APP
# ==========================================

# --- BRAND BAR ---
st.markdown("""
<div class="brand-bar">
    <div class="brand-logo">
        📡 STARLINK <span class="dim">TECH</span>
    </div>
    <div class="brand-sub">Field Technician Application</div>
</div>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero">
    <div class="hero-badge">NOW HIRING</div>
    <h1>Starlink Installation Technician</h1>
    <p>Apply to become a Certified Field Technician — Independent Contractor (1099)</p>
    <div class="hero-stats">
        <div class="stat">
            <div class="stat-value">$45–75</div>
            <div class="stat-label">Per Install</div>
        </div>
        <div class="divider"></div>
        <div class="stat">
            <div class="stat-value">Flexible</div>
            <div class="stat-label">Schedule</div>
        </div>
        <div class="divider"></div>
        <div class="stat">
            <div class="stat-value">Training</div>
            <div class="stat-label">Provided</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- APPLICATION FORM ---
with st.form("application_form"):

    # --- SECTION 1: CONTACT ---
    with st.container(border=True):
        st.markdown("""
        <div class="section-header">
            <div class="section-num">1</div>
            <div class="section-title">Contact Information</div>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("Full Name *")
        c1, c2 = st.columns(2)
        phone = c1.text_input("Phone Number *")
        email = c2.text_input("Email Address *")

        c3, c4, c5 = st.columns([2, 1, 1])
        city = c3.text_input("City")
        state = c4.text_input("State")
        zip_code = c5.text_input("ZIP")

    st.write("")

    # --- SECTION 2: EXPERIENCE ---
    with st.container(border=True):
        st.markdown("""
        <div class="section-header">
            <div class="section-num">2</div>
            <div class="section-title">Experience & Qualifications</div>
        </div>
        """, unsafe_allow_html=True)

        skills = st.multiselect("What installation experience do you have? *",
            ["Satellite systems (DirecTV, HughesNet)", "Starlink installation", "TV mounting",
             "Security camera installation", "Low voltage wiring (Cat5/Coax)",
             "Smart home systems", "No installation experience"])

        c_exp1, c_exp2 = st.columns(2)
        years = c_exp1.selectbox("Years of Experience *",
            ["Less than 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"])
        roof_work = c_exp2.radio("Experience working on roofs? *",
            ["Yes, comfortable", "Yes, limited", "No, but willing", "No"], horizontal=True)

        st.markdown("**Comfortable with tasks:**")
        t1, t2 = st.columns(2)
        task_drill = t1.checkbox("Drilling through walls/roofs")
        task_attic = t2.checkbox("Running cables in attics")
        t3, t4 = st.columns(2)
        task_height = t3.checkbox("Working at heights (20ft+)")
        task_net = t4.checkbox("Troubleshooting network issues")

    st.write("")

    # --- SECTION 3: VEHICLE & TOOLS ---
    with st.container(border=True):
        st.markdown("""
        <div class="section-header">
            <div class="section-num">3</div>
            <div class="section-title">Vehicle & Equipment</div>
        </div>
        """, unsafe_allow_html=True)

        vehicle = st.radio("Do you have a reliable vehicle? *",
            ["Yes - Truck", "Yes - Van", "Yes - SUV", "No"], horizontal=True)

        c_v1, c_v2 = st.columns(2)
        license_valid = c_v1.radio("Valid Driver's License? *", ["Yes", "No"], horizontal=True)
        ladder = c_v2.radio("Do you have a 28ft+ extension ladder? *",
            ["Yes, I own one", "No, but I can get one", "No"], horizontal=True)

        tools = st.multiselect("Tools owned (select all that apply):",
            ["Power drill", "Crimper tools", "Cable tester", "Fish tape", "Stud finder", "Signal meter"])

    st.write("")

    # --- SECTION 4: INSURANCE ---
    with st.container(border=True):
        st.markdown("""
        <div class="section-header">
            <div class="section-num">4</div>
            <div class="section-title">Insurance</div>
        </div>
        """, unsafe_allow_html=True)

        insurance = st.radio("Do you have General Liability Insurance? *",
            ["Yes, I currently have insurance", "No, but I can obtain within 1 week",
             "No, but I can obtain within 2 weeks", "No"])

    st.write("")

    # --- SECTION 5: AVAILABILITY ---
    with st.container(border=True):
        st.markdown("""
        <div class="section-header">
            <div class="section-num">5</div>
            <div class="section-title">Availability</div>
        </div>
        """, unsafe_allow_html=True)

        c_av1, c_av2 = st.columns(2)
        start_date = c_av1.selectbox("When can you start?",
            ["Immediately", "Within 1 week", "Within 2 weeks"])
        emp_type = c_av2.radio("Employment Type", ["Independent Contractor (1099)"], horizontal=True)

        days_avail = st.multiselect("Days Available",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    st.write("")

    # --- SECTION 6: SERVICE AREA ---
    with st.container(border=True):
        st.markdown("""
        <div class="section-header">
            <div class="section-num">6</div>
            <div class="section-title">Service Area</div>
        </div>
        """, unsafe_allow_html=True)

        counties = st.text_area("Which counties are you willing to work in? (Separate by comma) *",
            placeholder="Example: Orange County, Lake County, Seminole County")
        radius = st.select_slider("Max Travel Radius",
            options=["15 miles", "30 miles", "50 miles", "75 miles", "100+ miles"])

    st.write("")

    # --- SUBMIT ---
    submitted = st.form_submit_button("Submit Application →", type="primary", use_container_width=True)

    if submitted:
        if not name or not phone or not email or not counties:
            st.error("⚠️ Please fill in all required fields marked with *")
        else:
            application_status = "QUALIFIED"

            # Logic Engine
            is_rejected = False
            if "No installation experience" in skills:
                is_rejected = True
            if vehicle == "No":
                is_rejected = True
            if license_valid == "No":
                is_rejected = True
            if insurance == "No":
                is_rejected = True

            if is_rejected:
                application_status = "REJECTED"

            if not is_rejected:
                has_sat_exp = any(x in skills for x in
                    ["Satellite systems (DirecTV, HughesNet)", "Starlink installation"])
                has_ins = (insurance == "Yes, I currently have insurance")
                if has_sat_exp and has_ins and vehicle in ["Yes - Truck", "Yes - Van"]:
                    application_status = "PRIORITY"

            data_package = {
                "name": name, "phone": phone, "email": email,
                "skills": skills, "vehicle": vehicle, "insurance": insurance,
                "counties": counties, "answers": "See Full Data"
            }
            add_applicant(data_package, application_status)

            if application_status == "REJECTED":
                st.error("Thank you for your interest. Unfortunately, based on our current requirements, we're unable to proceed with your application at this time.")
            else:
                st.balloons()
                st.success("✅ Application Received Successfully!")
                if application_status == "PRIORITY":
                    st.info("⭐ **Priority Candidate** — Your qualifications are an excellent match.")
                st.markdown(f"""
                **Thank you, {name}.** Based on your qualifications, you are a strong fit for this position.
                Our hiring team will review your file and contact you at **{phone}** within 24 hours.
                """)

# --- FOOTER ---
st.markdown("""
<div class="footer-text">
    By submitting this application, you agree to our terms and conditions. All information is kept confidential.
</div>
""", unsafe_allow_html=True)
