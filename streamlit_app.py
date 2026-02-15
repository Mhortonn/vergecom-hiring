import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Starlink Tech Application",
    page_icon="📡",
    layout="wide"
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

# ==========================================
# THE APP (CENTERED & CARD STYLE)
# ==========================================

# 1. CREATE CENTER COLUMN
# We use columns [1, 2, 1] to make the middle column (2) twice as wide as the sides
# This effectively centers your form on the screen.
left_spacer, main_content, right_spacer = st.columns([1, 2, 1])

with main_content:
    
    # --- HEADER ---
    st.image("https://cdn-icons-png.flaticon.com/512/6927/6927640.png", width=70)
    st.title("Starlink Installation Technician")
    st.markdown("**Apply to become a Certified Field Technician**")
    st.info("📋 **Instructions:** Please complete all sections below.")

    with st.form("application_form"):
        
        # --- SECTION 1: CONTACT (CARD) ---
        with st.container(border=True):
            st.markdown("### 1. Contact Information")
            
            name = st.text_input("Full Name *")
            c1, c2 = st.columns(2)
            phone = c1.text_input("Phone Number *")
            email = c2.text_input("Email Address *")
            
            st.markdown("**Address**")
            street = st.text_input("Street Address")
            c3, c4, c5 = st.columns([2, 1, 1])
            city = c3.text_input("City")
            state = c4.text_input("State")
            zip_code = c5.text_input("ZIP")

        st.write("") # Spacer

        # --- SECTION 2: EXPERIENCE (CARD) ---
        with st.container(border=True):
            st.markdown("### 2. Experience & Qualifications")
            
            skills = st.multiselect("What installation experience do you have? *", 
                ["Satellite systems (DirecTV, HughesNet)", "Starlink installation", "TV mounting", 
                 "Security camera installation", "Low voltage wiring (Cat5/Coax)", 
                 "Smart home systems", "No installation experience"])
            
            c_exp1, c_exp2 = st.columns(2)
            years = c_exp1.selectbox("Years of Experience *", ["Less than 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"])
            roof_work = c_exp2.radio("Experience working on roofs? *", ["Yes, comfortable", "Yes, limited", "No, but willing", "No"], horizontal=True)
            
            st.markdown("**Comfortable with tasks:**")
            # We use checkboxes inside columns to make them look like cards too
            t1, t2 = st.columns(2)
            task_drill = t1.checkbox("Drilling through walls/roofs")
            task_attic = t2.checkbox("Running cables in attics")
            t3, t4 = st.columns(2)
            task_height = t3.checkbox("Working at heights (20ft+)")
            task_net = t4.checkbox("Troubleshooting network issues")

        st.write("") # Spacer

        # --- SECTION 3: VEHICLE & TOOLS (CARD) ---
        with st.container(border=True):
            st.markdown("### 3. Vehicle & Equipment")
            
            vehicle = st.radio("Do you have a reliable vehicle? *", ["Yes - Truck", "Yes - Van", "Yes - SUV", "No"], horizontal=True)
            
            c_v1, c_v2 = st.columns(2)
            license_valid = c_v1.radio("Valid Driver's License? *", ["Yes", "No"], horizontal=True)
            ladder = c_v2.radio("Do you have a 28ft+ extension ladder? *", ["Yes, I own one", "No, but I can get one", "No"], horizontal=True)
            
            st.markdown("**Tools owned:**")
            tools = st.multiselect("Select all that apply:", ["Power drill", "Crimper tools", "Cable tester", "Fish tape", "Stud finder", "Signal meter"])

        st.write("") # Spacer

        # --- SECTION 4: INSURANCE (CARD) ---
        with st.container(border=True):
            st.markdown("### 4. Insurance")
            insurance = st.radio("Do you have General Liability Insurance? *", 
                ["Yes, I currently have insurance", "No, but I can obtain within 1 week", "No, but I can obtain within 2 weeks", "No"])

        st.write("") # Spacer

        # --- SECTION 5: AVAILABILITY (CARD) ---
        with st.container(border=True):
            st.markdown("### 5. Availability")
            
            c_av1, c_av2 = st.columns(2)
            start_date = c_av1.selectbox("When can you start?", ["Immediately", "Within 1 week", "Within 2 weeks"])
            emp_type = c_av2.radio("Employment Type", ["Independent Contractor (1099)", "W2 Employee", "Either"], horizontal=True)
            
            days_avail = st.multiselect("Days Available", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        st.write("") # Spacer

        # --- SECTION 6: SERVICE AREA (CARD) ---
        with st.container(border=True):
            st.markdown("### 6. Service Area")
            counties = st.text_area("Which counties are you willing to work in? (Separate by comma) *", placeholder="Example: Orange County, Lake County, Seminole County")
            radius = st.select_slider("Max Travel Radius", options=["15 miles", "30 miles", "50 miles", "75 miles", "100+ miles"])

        st.write("") # Spacer
        
        # --- SUBMIT ---
        submitted = st.form_submit_button("Submit Application", type="primary", use_container_width=True)

        if submitted:
            if not name or not phone or not email or not counties:
                st.error("⚠️ Please fill in all required contact and location fields.")
            else:
                application_status = "QUALIFIED"
                
                # Logic Engine
                is_rejected = False
                if "No installation experience" in skills: is_rejected = True
                if vehicle == "No": is_rejected = True
                if license_valid == "No": is_rejected = True
                if insurance == "No": is_rejected = True
                
                if is_rejected:
                    application_status = "REJECTED"

                if not is_rejected:
                    has_sat_exp = any(x in skills for x in ["Satellite systems (DirecTV, HughesNet)", "Starlink installation"])
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
                    st.error("Thank you for your interest. Unfortunately, based on our requirements, we cannot proceed with your application at this time.")
                else:
                    st.balloons()
                    st.success("✅ Application Received Successfully!")
                    st.markdown(f"""
                    **Thank you, {name}.** Based on your qualifications, you are a strong fit for this position. 
                    Our hiring team will review your file and contact you at **{phone}** within 24 hours.
                    """)
