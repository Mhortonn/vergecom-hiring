import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIG & CONSTANTS ---
st.set_page_config(page_title="Starlink Tech Application", page_icon="📡", layout="centered")

SKILLS = [
    "Satellite systems (DirecTV, HughesNet)",
    "Starlink installation",
    "TV mounting",
    "Security camera installation",
    "Low voltage wiring (Cat5/Coax)",
    "Smart home systems",
    "No installation experience",
]
TOOLS = ["Power drill", "Crimper tools", "Cable tester", "Fish tape", "Stud finder", "Signal meter"]
YEARS_OPTIONS = ["Less than 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"]

# --- CUSTOM CSS (THE "PAINT") ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

    /* 1. Main Background */
    .stApp {
        background-color: #F0F2F6; /* Clean Off-White */
        font-family: 'DM Sans', sans-serif;
    }

    /* 2. Headers (Add Blue Color) */
    h1, h2, h3 {
        color: #0066FF !important; /* Starlink Blue */
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* 3. The "Cards" (White Boxes with Shadow) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); /* Soft Shadow */
        padding: 20px;
        margin-bottom: 20px;
    }

    /* 4. Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
    }

    /* 5. Submit Button (Force Blue) */
    .stButton button {
        background-color: #0066FF !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 102, 255, 0.2);
    }
    .stButton button:hover {
        background-color: #0052CC !important;
    }

    /* 6. Hero Section Styling */
    .hero-box {
        background: white;
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        border-top: 5px solid #0066FF;
    }
    .hero-badge {
        background: #E3FBF0;
        color: #00875A;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('starlink_candidates.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, phone TEXT, email TEXT, status TEXT, 
            skills TEXT, timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_applicant(data, status):
    conn = sqlite3.connect('starlink_candidates.db')
    c = conn.cursor()
    c.execute("INSERT INTO applicants (name, phone, email, status, skills, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (data['name'], data['phone'], data['email'], status, str(data['skills']), datetime.now()))
    conn.commit()
    conn.close()

init_db()

# --- SESSION STATE ---
if 'form' not in st.session_state:
    st.session_state.form = {
        "name": "", "phone": "", "email": "", "skills": [], "years": "", 
        "vehicle": "No", "license": "No", "insurance": "No", "counties": ""
    }
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
    st.session_state.status = ""

# --- MAIN APP LOGIC ---

if st.session_state.submitted:
    # SUCCESS SCREEN
    st.markdown(f"""
    <div style="text-align:center; padding: 50px; background: white; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="font-size: 60px;">✅</div>
        <h2 style="color: #0066FF;">Application Received</h2>
        <p>Thank you, <strong>{st.session_state.form['name']}</strong>.</p>
        <p>Our team will contact you at <strong>{st.session_state.form['phone']}</strong> within 24 hours.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start New Application"):
        st.session_state.submitted = False
        st.rerun()

else:
    # HERO HEADER
    st.markdown("""
    <div class="hero-box">
        <div class="hero-badge">NOW HIRING</div>
        <h1 style="margin: 10px 0;">Starlink Installation Technician</h1>
        <p style="color: #666;">Apply to become a Certified Field Technician (1099)</p>
    </div>
    """, unsafe_allow_html=True)

    # PROGRESS BAR
    progress = 0
    if st.session_state.form['name']: progress += 20
    if st.session_state.form['skills']: progress += 20
    if st.session_state.form['vehicle'] != "No": progress += 20
    if st.session_state.form['counties']: progress += 40
    st.progress(progress)

    # --- FORM SECTIONS (Using Containers as "Cards") ---

    with st.container(border=True):
        st.subheader("👤 1. Contact Information")
        st.session_state.form['name'] = st.text_input("Full Name *", value=st.session_state.form['name'])
        c1, c2 = st.columns(2)
        st.session_state.form['phone'] = c1.text_input("Phone Number *", value=st.session_state.form['phone'])
        st.session_state.form['email'] = c2.text_input("Email Address *", value=st.session_state.form['email'])
        
        # STREET ADDRESS REMOVED
        c3, c4, c5 = st.columns([2, 1, 1])
        c3.text_input("City")
        c4.text_input("State")
        c5.text_input("Zip")

    with st.container(border=True):
        st.subheader("🛠 2. Experience")
        st.session_state.form['skills'] = st.multiselect("Installation Experience *", SKILLS, default=st.session_state.form['skills'])
        
        c1, c2 = st.columns(2)
        st.session_state.form['years'] = c1.selectbox("Years of Experience", [""] + YEARS_OPTIONS)
        c2.radio("Experience working on roofs?", ["Yes", "Limited", "No"], horizontal=True)

    with st.container(border=True):
        st.subheader("🚗 3. Vehicle & Tools")
        st.session_state.form['vehicle'] = st.radio("Do you have a reliable vehicle?", ["Yes - Truck/Van", "Yes - SUV", "No"], horizontal=True)
        
        c1, c2 = st.columns(2)
        st.session_state.form['license'] = c1.radio("Valid Driver's License?", ["Yes", "No"], horizontal=True)
        c2.radio("Own a 28ft+ Ladder?", ["Yes", "No"], horizontal=True)
        
        st.multiselect("Tools Owned", TOOLS)

    with st.container(border=True):
        st.subheader("🛡 4. Requirements")
        st.session_state.form['insurance'] = st.radio("General Liability Insurance", ["Yes, I have it", "No, but I will get it", "No"])
        st.session_state.form['counties'] = st.text_area("Counties you can cover *", placeholder="e.g. Orange, Lake, Seminole...", value=st.session_state.form['counties'])

    # SUBMIT BUTTON
    if st.button("Submit Application"):
        # Validation
        if not st.session_state.form['name'] or not st.session_state.form['phone']:
            st.error("Please fill in Name and Phone Number.")
        else:
            # Logic
            status = "QUALIFIED"
            if "No installation experience" in st.session_state.form['skills']: status = "REJECTED"
            
            save_applicant(st.session_state.form, status)
            st.session_state.status = status
            st.session_state.submitted = True
            st.rerun()
