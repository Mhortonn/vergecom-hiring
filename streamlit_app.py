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
    # We create a robust table to hold the key data and the calculated status
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
    
    # We save specific columns for sorting, and the rest in a big text blob
    skills_str = ", ".join(data['skills'])
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_dump = str(data) # Saving all answers just in case
    
    c.execute('''INSERT INTO applicants 
                 (name, phone, email, status, skills, vehicle, insurance, location, timestamp, full_data) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (data['name'], data['phone'], data['email'], status, skills_str, 
               data['vehicle'], data['insurance'], data['counties'], date_str, full_dump))
    conn.commit()
    conn.close()

def get_applicants():
    conn = sqlite3.connect('starlink_candidates.db')
    try:
        df = pd.read_sql_query("SELECT * FROM applicants", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

init_db()

# --- SIDEBAR (ADMIN) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6927/6927640.png", width=50)
    st.markdown("### 📡 Tech Portal")
    
    admin_password = st.text_input("Admin Password", type="password")
    if admin_password == "admin123":
        admin_mode = True
        st.success("Access Granted")
    else:
        admin_mode = False

# ==========================================
# ADMIN VIEW
# ==========================================
if admin_mode:
    st.title("📂 Applicant Database")
    
    df = get_applicants()
    
    if not df.empty:
        # Filter buttons
        filter_status = st.radio("Filter by Status:", ["All", "PRIORITY", "QUALIFIED", "REJECTED"], horizontal=True)
        
        if filter_status != "All":
            df = df[df['status'] == filter_status]
            
        st.dataframe(
            df,
            column_config={
                "name": "Name",
                "status": "Auto-Grade",
                "phone": "Phone",
                "vehicle": "Vehicle",
                "insurance": "Insurance",
                "location": "Service Counties"
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.download_button("📥 Download CSV", df.to_csv(index=False).encode('utf-8'), "applicants.csv", "text/csv")
    else:
        st.info("No applicants found.")

# ==========================================
# CANDIDATE VIEW (THE FORM)
# ==========================================
else:
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Starlink Installation Technician")
        st.markdown("**Apply to become a Certified Field Technician**")
    with col2:
        st.markdown("### 🛰️ $1,500+/wk")
        st.caption("Est. Contract Pay")

    st.info("📋 **Instructions:** Please complete all sections below. Incomplete applications will not be reviewed.")

    with st.form("application_form"):
        
        # --- SECTION 1: CONTACT ---
        st.markdown("### 1. Contact Information")
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Full Name *")
        phone = c2.text_input("Phone Number *")
        email = c3.text_input("Email Address *")
        
        c4, c5, c6, c7 = st.columns([2, 2, 1, 1])
        street = c4.text_input("Street Address")
        city = c5.text_input("City")
        state = c6.text_input("State")
        zip_code = c7.text_input("ZIP")

        st.divider()

        # --- SECTION 2: EXPERIENCE ---
        st.markdown("### 2. Experience & Qualifications")
        skills = st.multiselect("What installation experience do you have? *", 
            ["Satellite systems (DirecTV, HughesNet)", "Starlink installation", "TV mounting", 
             "Security camera installation", "Low voltage wiring (Cat5/Coax)", 
             "Smart home systems", "No installation experience"])
        
        c_exp1, c_exp2 = st.columns(2)
        years = c_exp1.selectbox("Years of Experience *", ["Less than 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"])
        roof_work = c_exp2.radio("Experience working on roofs? *", ["Yes, comfortable", "Yes, limited", "No, but willing", "No"], horizontal=True)
        
        tasks = st.multiselect("Comfortable with tasks: *", 
            ["Drilling through walls/roofs", "Running cables in attics", "Working at heights (20ft+)", "Troubleshooting network issues"])

        st.divider()

        # --- SECTION 3: VEHICLE & TOOLS ---
        st.markdown("### 3. Vehicle & Equipment")
        c_veh1, c_veh2 = st.columns(2)
        vehicle = c_veh1.radio("Do you have a reliable vehicle? *", ["Yes - Truck", "Yes - Van", "Yes - SUV", "No"])
        license_valid = c_veh2.radio("Valid Driver's License? *", ["Yes", "No"])
        
        ladder = st.radio("Do you have a 28ft+ extension ladder? *", ["Yes, I own one", "No, but I can get one", "No"], horizontal=True)
        
        tools = st.multiselect("Tools owned: *", ["Power drill", "Crimper tools", "Cable tester", "Fish tape", "Stud finder", "Signal meter"])

        st.divider()

        # --- SECTION 4: INSURANCE ---
        st.markdown("### 4. Insurance")
        insurance = st.radio("Do you have General Liability Insurance? *", 
            ["Yes, I currently have insurance", "No, but I can obtain within 1 week", "No, but I can obtain within 2 weeks", "No"])

        st.divider()

        # --- SECTION 5: AVAILABILITY ---
        st.markdown("### 5. Availability")
        c_av1, c_av2 = st.columns(2)
        start_date = c_av1.selectbox("When can you start?", ["Immediately", "Within 1 week", "Within 2 weeks"])
        emp_type = c_av2.radio("Employment Type", ["Independent Contractor (1099)", "W2 Employee", "Either"])
        
        days_avail = st.multiselect("Days Available", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        st.divider()

        # --- SECTION 6: SERVICE AREA ---
        st.markdown("### 6. Service Area")
        counties = st.text_area("Which counties are you willing to work in? (Separate by comma) *", placeholder="Example: Orange County, Lake County, Seminole County")
        radius = st.select_slider("Max Travel Radius", options=["15 miles", "30 miles", "50 miles", "75 miles", "100+ miles"])

        st.divider()
        
        # --- SUBMIT ---
        submitted = st.form_submit_button("Submit Application", type="primary", use_container_width=True)

        if submitted:
            # 1. VALIDATION
            if not name or not phone or not email or not counties:
                st.error("⚠️ Please fill in all required contact and location fields.")
            else:
                # 2. LOGIC ENGINE (The Brain)
                application_status = "QUALIFIED" # Default
                
                # A. Auto-Reject Conditions
                is_rejected = False
                if "No installation experience" in skills: is_rejected = True
                if vehicle == "No": is_rejected = True
                if license_valid == "No": is_rejected = True
                if insurance == "No": is_rejected = True
                
                if is_rejected:
                    application_status = "REJECTED"

                # B. Priority Conditions (Only if not rejected)
                if not is_rejected:
                    has_sat_exp = any(x in skills for x in ["Satellite systems (DirecTV, HughesNet)", "Starlink installation"])
                    has_ins = (insurance == "Yes, I currently have insurance")
                    if has_sat_exp and has_ins and vehicle in ["Yes - Truck", "Yes - Van"]:
                        application_status = "PRIORITY"

                # 3. SAVE TO DB
                data_package = {
                    "name": name, "phone": phone, "email": email,
                    "skills": skills, "vehicle": vehicle, "insurance": insurance, 
                    "counties": counties, "answers": "See Full Data"
                }
                add_applicant(data_package, application_status)

                # 4. SHOW RESULT MESSAGE
                if application_status == "REJECTED":
                    st.error("Thank you for your interest. Unfortunately, based on our requirements (Vehicle, License, or Experience), we cannot proceed with your application at this time.")
                else:
                    st.balloons()
                    st.success("✅ Application Received Successfully!")
                    st.markdown(f"""
                    **Thank you, {name}.** Based on your qualifications, you are a strong fit for this position. 
                    Our hiring team will review your file and contact you at **{phone}** within 24 hours.
                    """)        admin_mode = False

# ==========================================
# ADMIN DASHBOARD
# ==========================================
if admin_mode:
    st.title("📂 Applicant Database")
    st.markdown("Current pipeline of field technician candidates.")
    
    df = get_all_candidates()
    
    if not df.empty:
        # Metrics at the top
        m1, m2 = st.columns(2)
        m1.metric("Total Applicants", len(df))
        m2.metric("Last Application", df.iloc[-1]['timestamp'].split(" ")[0])
        
        st.dataframe(
            df,
            column_config={
                "name": "Candidate Name",
                "phone": "Contact Number",
                "skills": "Technical Skills",
                "timestamp": "Date Applied"
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.download_button(
            label="📥 Export Data (CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='vergecom_candidates.csv',
            mime='text/csv',
        )
    else:
        st.info("No active applications found in the database.")

# ==========================================
# PUBLIC APPLICATION FORM
# ==========================================
else:
    # Use columns to center the content for a professional look
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.header("Vergecom Careers")
        st.markdown("---")
        
        # Corporate Job Description Box
        st.info("""
        **POSITION: Field Technician / Installer** **LOCATION:** Greater Metro Area  
        **COMPENSATION:** Contract ($1,200 - $1,800/week)
        """)
        
        st.markdown("""
        Vergecom is seeking qualified independent contractors for residential and commercial telecommunications installations. 
        Candidates must possess their own work vehicle and necessary tooling.
        """)
        
        with st.expander("View Detailed Requirements"):
            st.markdown("""
            * **Vehicle:** Truck/Van capable of ladder transport (28ft extension ladder required).
            * **Tools:** Standard telecom hand tools, drill, signal meter.
            * **Insurance:** General Liability policy (or willingness to obtain).
            * **Experience:** Low-voltage, coax, or satellite experience preferred.
            """)
        
        st.markdown("### Application for Contract")
        
        # Professional Inputs
        with st.container(border=True):
            name = st.text_input("Full Legal Name")
            phone = st.text_input("Mobile Number")
        
        st.write("")
        st.markdown("**Select Relevant Experience**")
        
        # Clean List Layout
        skills = [
            "Satellite Systems (DirecTV/Dish/HughesNet)",
            "Starlink / LEO Satellite",
            "Residential TV Mounting",
            "Security / CCTV Installation",
            "Home Theater & Audio",
            "Structured Wiring (Cat5/Cat6/Coax)"
        ]
        
        selected_skills = []
        for s in skills:
            if st.checkbox(s):
                selected_skills.append(s)
        
        st.write("")
        
        # Disclaimer / Agreement Text (Very corporate)
        st.caption("By submitting this application, you certify that the information provided is accurate and you consent to being contacted by Vergecom recruiting via phone or text.")
        
        if st.button("Submit Application", type="primary", use_container_width=True):
            if not name or not phone:
                st.error("Submission Failed: Please complete all required fields.")
            elif not selected_skills:
                st.error("Submission Failed: Please select at least one qualification.")
            else:
                add_candidate(name, phone, selected_skills)
                st.success("Application Submitted Successfully.")
                st.markdown(f"""
                **Thank you, {name}.** Your profile has been routed to our hiring manager. If your qualifications match our current territory needs, we will contact you at **{phone}** within 48 hours.
                """)
