import streamlit as st
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom Careers", page_icon="📡", layout="centered")

# --- CUSTOM CSS (THE LOOK & FEEL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    /* DARK SATELLITE BACKGROUND */
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)), 
                          url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'DM Sans', sans-serif;
    }

    /* HEADERS */
    h1, h2, h3 {
        color: #0066FF !important;
        font-weight: 700 !important;
    }
    
    /* WHITE CARD DESIGN */
    .job-card {
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 12px;
        padding: 40px 35px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        margin: 20px 0 30px 0;
        border-top: 6px solid #0066FF;
    }

    /* SECTION TITLES */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin-top: 30px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 2px solid #0066FF;
        padding-bottom: 8px;
    }
    
    /* FIRST SECTION TITLE SHOULDN'T HAVE TOP MARGIN */
    .section-title:first-of-type {
        margin-top: 10px;
    }
    
    /* JOB TEXT */
    .job-text {
        color: #2D3748;
        font-size: 16px;
        line-height: 1.7;
        margin-bottom: 20px;
    }
    
    /* JOB LIST */
    .job-list {
        margin: 10px 0 20px 0;
        padding-left: 25px;
        color: #2D3748;
        font-size: 16px;
        line-height: 1.7;
    }
    
    .job-list li {
        margin-bottom: 12px;
    }
    
    /* PAY HIGHLIGHT BOX */
    .pay-box {
        background: linear-gradient(135deg, #F0F9FF 0%, #E6F7F0 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0 25px 0;
        border-left: 6px solid #059669;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .pay-text {
        color: #059669;
        font-size: 24px;
        font-weight: 800;
        margin: 0;
    }
    
    .pay-subtext {
        color: #4B5563;
        font-size: 16px;
        margin: 5px 0 0 0;
    }
    
    /* BLACK BUTTON */
    .stButton button {
        background-color: #000000 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        border-radius: 8px !important;
        padding: 1rem 2rem !important;
        border: 2px solid #333 !important;
        width: 100%;
        transition: all 0.2s ease;
        letter-spacing: 1px;
    }
    .stButton button:hover {
        background-color: #333333 !important;
        transform: scale(1.01);
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        border-color: #0066FF !important;
    }
    
    /* INPUT FIELDS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        color: #1A202C;
        border-radius: 8px;
        padding: 10px;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0066FF !important;
        box-shadow: 0 0 0 3px rgba(0,102,255,0.1);
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* FORM CONTAINER */
    .form-container {
        background-color: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin: 20px 0;
    }
    
    /* SUCCESS MESSAGE */
    .success-box {
        background-color: white;
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        border-top: 8px solid #00B37E;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 30px 0;
    }
    
    .success-title {
        color: #00B37E !important;
        font-size: 36px !important;
        margin: 0 0 20px 0 !important;
    }
    
    .success-text {
        font-size: 18px;
        color: #4A5568;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- DATABASE FUNCTIONS ---
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
    
    # Create a clean job description card using st.markdown with proper HTML
    st.markdown("""
    <div class="job-card">
        <h1 style="text-align: center; font-size: 42px; margin-bottom: 5px; color: #0066FF !important;">Starlink Technician</h1>
        <p style="text-align: center; color: #4B5563; font-weight: 500; font-size: 18px; margin-bottom: 20px;">
            Independent Contractor (1099) | High-Volume Installations
        </p>
    """, unsafe_allow_html=True)
    
    # Pay box - separate for clarity
    st.markdown("""
        <div class="pay-box">
            <p class="pay-text">💰 $1,200 - $1,800 per week</p>
            <p class="pay-subtext">Average earnings for qualified technicians</p>
        </div>
    """, unsafe_allow_html=True)
    
    # About the Role
    st.markdown("""
        <div class="section-title">📋 About the Role</div>
        <p class="job-text">
            Vergecom is looking for professional, self-motivated Field Technicians to install, service, and upgrade Starlink satellite systems for residential and commercial customers. 
            This is a <strong>1099 Independent Contractor</strong> position offering flexibility and high earning potential based on piece-rate pay.
        </p>
    """, unsafe_allow_html=True)
    
    # Key Responsibilities
    st.markdown("""
        <div class="section-title">🔧 Key Responsibilities</div>
        <ul class="job-list">
            <li><strong>Site Surveys:</strong> Determine optimal placement for satellite dishes for safe and efficient operation.</li>
            <li><strong>Hardware Installation:</strong> Mount hardware on roofs, siding, or poles using professional techniques.</li>
            <li><strong>Cabling:</strong> Route cabling cleanly from exterior to interior of homes.</li>
            <li><strong>Configuration:</strong> Set up routers and assist customers with app connectivity.</li>
            <li><strong>Troubleshooting:</strong> Resolve signal or connectivity issues on-site.</li>
            <li><strong>Inventory Management:</strong> Maintain accurate equipment records and report job status.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    # Requirements
    st.markdown("""
        <div class="section-title">✅ Requirements</div>
        <ul class="job-list">
            <li><strong>Vehicle:</strong> Must own a reliable Truck, Van, or SUV capable of carrying a ladder.</li>
            <li><strong>Ladder:</strong> Must own a 28ft fiberglass extension ladder.</li>
            <li><strong>Tools:</strong> Must possess standard installation tools (Power Drill, Impact Driver, Hand Tools).</li>
            <li><strong>Smart Device:</strong> Must have a smartphone with data plan for dispatch apps.</li>
            <li><strong>Legal:</strong> Valid Driver's License and General Liability Insurance.</li>
            <li><strong>Skills:</strong> Comfort working at heights, on roofs, and in confined spaces.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    # Schedule
    st.markdown("""
        <div class="section-title">📅 Schedule & Territory</div>
        <p class="job-text">
            Routes are dispatched daily within the Greater Metro Area. Technicians typically complete 3-6 jobs per day. 
            <strong>Weekend availability is a plus.</strong> Flexible scheduling - you choose your working days.
        </p>
    </div> <!-- Close job-card -->
    """, unsafe_allow_html=True)
    
    # Button to apply
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 BECOME A TECHNICIAN", use_container_width=True):
            st.session_state.page = 'application'
            st.rerun()

# ==========================================
# PAGE 2: APPLICATION FORM
# ==========================================
elif st.session_state.page == 'application':
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
    
    # Form header
    st.markdown("""
    <div class="form-container">
        <h2 style="text-align: center; color: #0066FF !important; margin-top: 0;">Technician Application</h2>
        <p style="text-align: center; color: #666; margin-bottom: 30px;">Please complete all required fields (*)</p>
    """, unsafe_allow_html=True)
    
    # --- FORM INPUTS ---
    with st.container():
        st.subheader("👤 Contact Information")
        name = st.text_input("Full Name *")
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Phone Number *")
        with col2:
            email = st.text_input("Email Address")
        
        col3, col4, col5 = st.columns(3)
        with col3:
            city = st.text_input("City")
        with col4:
            state = st.text_input("State")
        with col5:
            zip_code = st.text_input("ZIP Code")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    with st.container():
        st.subheader("🛠️ Experience & Skills")
        experience = st.selectbox("Years of installation experience *", 
                                  ["Select...", "< 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"])
        
        skills = st.multiselect("Select your areas of experience *", 
                                ["Satellite TV Installation", "Starlink Installation", "TV Mounting", 
                                 "Low Voltage Wiring", "Network Setup", "Security Cameras", "None"])
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    with st.container():
        st.subheader("🚗 Equipment & Requirements")
        col1, col2 = st.columns(2)
        with col1:
            vehicle = st.radio("Do you have a reliable truck/van/SUV? *", ["Yes", "No"], horizontal=True)
            ladder = st.radio("Do you own a 28ft+ ladder? *", ["Yes", "No"], horizontal=True)
        with col2:
            license_valid = st.radio("Valid Driver's License? *", ["Yes", "No"], horizontal=True)
            insurance = st.radio("General Liability Insurance?", ["Yes", "No, but can obtain", "No"], horizontal=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    with st.container():
        st.subheader("📍 Availability")
        counties = st.text_area("Counties/Cities you can work in *", 
                                placeholder="e.g., Miami-Dade, Broward, Palm Beach")
        
        weekend = st.checkbox("I am available to work on weekends")
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📨 SUBMIT APPLICATION", use_container_width=True):
        if not name or not phone or experience == "Select..." or vehicle == "No" or ladder == "No" or license_valid == "No":
            st.error("⚠️ Please fill in all required fields and ensure you meet the minimum requirements.")
        else:
            # Save to database
            data = {
                "name": name, "phone": phone, "email": email, 
                "skills": skills, "experience": experience
            }
            
            # Determine status
            status = "QUALIFIED" if "None" not in skills else "REVIEW NEEDED"
            save_applicant(data, status)
            
            # Success message
            st.balloons()
            st.markdown(f"""
            <div class="success-box">
                <h1 class="success-title">✅ Application Received!</h1>
                <p class="success-text">Thank you <strong>{name}</strong> for applying!</p>
                <p class="success-text">We will review your application and contact you at <strong>{phone}</strong> within 2-3 business days.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a button to go back
            if st.button("← Return to Job Description"):
                st.session_state.page = 'landing'
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close form-container
