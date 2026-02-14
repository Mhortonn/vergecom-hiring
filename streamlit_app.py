import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vergecom Careers",
    page_icon="🏢",
    layout="wide"  # WIDE layout looks more like enterprise software
)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            skills TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_candidate(name, phone, skills_list):
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    skills_str = ", ".join(skills_list)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO candidates (name, phone, skills, timestamp) VALUES (?, ?, ?, ?)', 
              (name, phone, skills_str, date_str))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect('candidates.db')
    try:
        df = pd.read_sql_query("SELECT * FROM candidates", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

init_db()

# --- SIDEBAR (Internal Use) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1063/1063735.png", width=50) # Generic corporate logo placeholder
    st.markdown("**Vergecom Internal Portal**")
    st.divider()
    
    st.header("Admin Access")
    admin_password = st.text_input("Password", type="password")
    
    if admin_password == "admin123":
        admin_mode = True
        st.success("Authorized")
    else:
        admin_mode = False

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
