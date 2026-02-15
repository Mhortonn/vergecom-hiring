import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom Careers", page_icon="📡", layout="centered")

# --- CUSTOM CSS (THE LOOK & FEEL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    /* 1. DARK SATELLITE BACKGROUND */
    .stApp {
        /* High-quality Dark Satellite Orbit Image */
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), 
                          url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'DM Sans', sans-serif;
    }

    /* 2. HEADERS */
    h1, h2, h3 {
        color: #0066FF !important;
        font-weight: 700 !important;
    }
    
    /* 3. WHITE CARD DESIGN */
    .job-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
        margin-bottom: 30px;
    }

    /* 4. BLACK BUTTON (BECOME A TECHNICIAN) */
    .stButton button {
        background-color: #000000 !important; /* Pure Black */
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        border-radius: 8px !important;
        padding: 1rem 2rem !important;
        border: 1px solid #333 !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background-color: #333333 !important; /* Dark Grey Hover */
        transform: scale(1.01);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* 5. INPUT FIELDS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #F9FAFB;
        border: 1px solid #D1D5DB;
        color: #111827;
        border-radius: 6px;
    }
    
    /* 6. HIDE DEFAULT STREAMLIT MENU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect('starlink_candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applicants 
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, 
                  status TEXT, skills TEXT, timestamp TEXT)''')
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

# ==========================================
# PAGE 1: LANDING PAGE (JOB DESCRIPTION)
# ==========================================
if st.session_state.page == 'landing':
    
    st.write("") # Spacer

    # THE MAIN CARD
    st.markdown("""
    <div class="job-card">
        <h1 style="margin-bottom: 10px; font-size: 38px;">Starlink Technician</h1>
        <p style="color: #4B5563; font-size: 16px; margin-bottom: 30px;">
            Vergecom is hiring experienced <strong>Independent Contractors (1099)</strong><br>
            for high-volume residential & commercial installations.
        </p>

        <div style="display: flex; justify-content: center; gap: 40px; margin-bottom: 30px;">
            <div style="text-align: center;">
                <div style="font-size: 24px;">💰</div>
                <h3 style="margin: 5px 0 0 0; font-size: 18px; color: #111;">Pay</h3>
                <p style="margin: 0; color: #666; font-weight: 500;">$1,200 - $1,800 / week</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px;">📍</div>
                <h3 style="margin: 5px 0 0 0; font-size: 18px; color: #111;">Location</h3>
                <p style="margin: 0; color: #666; font-weight: 500;">Greater Metro Area</p>
            </div>
        </div>

        <div style="background-color: #F3F4F6; padding: 25px; border-radius: 10px; text-align: left; border-left: 5px solid #000;">
            <strong style="color: #000; font-size: 16px; display: block; margin-bottom: 10px;">REQUIREMENTS:</strong>
            <ul style="margin: 0; padding-left: 20px; color: #374151; font-size: 15px; line-height: 1.6;">
                <li>Must have reliable <strong>Truck, Van, or SUV</strong>.</li>
                <li>Must have <strong>28ft Extension Ladder</strong>.</li>
                <li>Must have basic power tools (Drill, Impact, Hand Tools).</li>
                <li>Valid Driver's License & General Liability Insurance required.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # THE BLACK BUTTON
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        if st.button("BECOME A TECHNICIAN"):
            st.session_state.page = 'application'
            st.rerun()

# ==========================================
# PAGE 2: APPLICATION FORM
# ==========================================
elif st.session_state.page == 'application':

    # Back Button (Simple text link style)
    if st.button("← Back"):
        st.session_state.page = 'landing'
        st.rerun()

    # White Container for Form
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.95); padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
        <h2 style="margin:0; color: #000 !important;">Technician Application</h2>
        <p style="margin:0; color: #666;">Please complete the details below.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- FORM INPUTS ---
    SKILLS_LIST = [
        "Satellite systems (DirecTV, HughesNet)", "Starlink installation",
        "TV mounting", "Security camera installation",
        "Low voltage wiring (Cat5/Coax)", "Smart home systems",
        "No installation experience"
    ]
    TOOLS_LIST = ["Power drill", "Crimper tools", "Cable tester", "Fish tape", "Stud finder", "Signal meter"]
    
    # Use standard Streamlit containers (they look like white cards due to our CSS)
    with st.container(border=True):
        st.subheader("👤 Contact Info")
        name = st.text_input("Full Name *")
        c1, c2 = st.columns(2)
        phone = c1.text_input("Phone Number *")
        email = c2.text_input("Email Address *")
        
        c3, c4, c5 = st.columns([2, 1, 1])
        city = c3.text_input("City")
        state = c4.text_input("State")
        zip_code = c5.text_input("Zip")

    with st.container(border=True):
        st.subheader("🛠 Experience")
        skills = st.multiselect("Installation Experience *", SKILLS_LIST)
        c1, c2 = st.columns(2)
        years = c1.selectbox("Years of Experience", ["< 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"])
        roof = c2.radio("Roof Work?", ["Yes", "Limited", "No"], horizontal=True)

    with st.container(border=True):
        st.subheader("🚗 Vehicle & Tools")
        vehicle = st.radio("Do you have a reliable vehicle?", ["Yes - Truck/Van", "Yes - SUV", "No"], horizontal=True)
        c1, c2 = st.columns(2)
        license_valid = c1.radio("Valid Driver's License?", ["Yes", "No"], horizontal=True)
        ladder = c2.radio("Own a 28ft+ Ladder?", ["Yes", "No"], horizontal=True)
        user_tools = st.multiselect("Tools Owned", TOOLS_LIST)

    with st.container(border=True):
        st.subheader("🛡 Requirements")
        insurance = st.radio("General Liability Insurance", ["Yes, I have it", "No, but will get it", "No"])
        counties = st.text_area("Counties you can cover *")

    # --- SUBMIT ---
    if st.button("SUBMIT APPLICATION"):
        if not name or not phone:
            st.error("⚠️ Please fill in Name and Phone Number.")
        else:
            status = "QUALIFIED"
            if "No installation experience" in skills: status = "REJECTED"
            if vehicle == "No" or ladder == "No": status = "REJECTED"
            
            data = {
                "name": name, "phone": phone, "email": email, 
                "skills": skills, "years": years, "vehicle": vehicle
            }
            save_applicant(data, status)
            
            st.balloons()
            st.markdown(f"""
            <div style="background-color: white; padding: 40px; border-radius: 12px; text-align: center; border-top: 6px solid #00B37E;">
                <h1 style="color:#00B37E !important; margin:0;">Application Received!</h1>
                <p style="font-size: 18px; margin-top: 10px;">Thank you <strong>{name}</strong>.</p>
                <p style="color: #666;">We will review your info and contact you at <strong>{phone}</strong> shortly.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
