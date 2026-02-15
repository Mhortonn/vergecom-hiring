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
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)), 
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
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 12px;
        padding: 50px 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        text-align: left;
        margin-bottom: 30px;
        border-top: 6px solid #0066FF;
    }

    /* 4. BLACK BUTTON (BECOME A TECHNICIAN) */
    .stButton button {
        background-color: #000000 !important;
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
        background-color: #333333 !important;
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

    /* 6. TEXT STYLING CLASSES */
    .job-section-title {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 5px;
    }
    .job-text {
        color: #4B5563;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    .job-list {
        margin: 0; 
        padding-left: 20px; 
        color: #4B5563; 
        font-size: 15px; 
        line-height: 1.6;
    }
    .job-list li {
        margin-bottom: 8px;
    }

    /* HIDE MENU */
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

    # THE MAIN JOB CARD
    st.markdown("""
    <div class="job-card">
        <h1 style="text-align: center; font-size: 38px; margin-bottom: 5px;">Starlink Technician</h1>
        <p style="text-align: center; color: #6B7280; font-weight: 500; font-size: 16px; margin-bottom: 30px;">
            Independent Contractor (1099) | High-Volume Installations
        </p>

        <div style="background: #F3F4F6; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 25px;">
            <strong style="color: #059669; font-size: 18px;">💰 Est. Pay: $1,200 - $1,800 / week</strong>
        </div>

        <div class="job-section-title">About the Role</div>
        <p class="job-text">
            Vergecom is looking for professional, self-motivated Field Technicians to install, service, and upgrade Starlink satellite systems for residential and commercial customers. 
            This is a <strong>1099 Independent Contractor</strong> position offering flexibility and high earning potential based on piece-rate pay.
        </p>

        <div class="job-section-title">Key Responsibilities</div>
        <ul class="job-list">
            <li>Perform site surveys to determine the optimal placement for satellite dishes.</li>
            <li>Mount hardware on roofs, siding, or poles using professional techniques (drilling, sealing, lag bolting).</li>
            <li>Route cabling cleanly from the exterior to the interior of the home (drilling, fishing walls, tacking cable).</li>
            <li>Configure routers and assist customers with app setup and Wi-Fi connectivity.</li>
            <li>Troubleshoot and resolve signal or connectivity issues on-site.</li>
            <li>Maintain accurate inventory of equipment and report job status via mobile app.</li>
        </ul>

        <div class="job-section-title">Requirements</div>
        <ul class="job-list">
            <li><strong>Vehicle:</strong> Must own a reliable Truck, Van, or SUV capable of carrying a ladder.</li>
            <li><strong>Ladder:</strong> Must own a 28ft fiberglass extension ladder.</li>
            <li><strong>Tools:</strong> Must possess standard installation tools (Power Drill, Impact Driver, Spade Bits, Hand Tools, Cable Stapler).</li>
            <li><strong>Smart Device:</strong> Must have a smartphone (iOS or Android) with a data plan for dispatch apps.</li>
            <li><strong>Legal:</strong> Valid Driver's License and General Liability Insurance (or willingness to obtain).</li>
            <li><strong>Skills:</strong> Comfort working at heights, on roofs, and in crawl spaces/attics.</li>
        </ul>

        <div class="job-section-title">Schedule & Territory</div>
        <p class="job-text">
            Routes are dispatched daily within the Greater Metro Area. Technicians typically complete 3-6 jobs per day. Weekend availability is a plus.
        </p>
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

    # Back Button
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
