import streamlit as st
import time

# --- CONSTANTS ---
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
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
YEARS_OPTIONS = ["Less than 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"]
RADIUS_OPTIONS = ["15 miles", "30 miles", "50 miles", "75 miles", "100+ miles"]

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Starlink Tech Application", page_icon="📡", layout="centered")

# Inject Custom CSS to match the React Styles (DM Sans, Space Grotesk, Colors)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* Global Reset */
    .stApp {
        background-color: #F4F5F7;
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #1A1D23;
    }

    /* Hero Section Styles */
    .hero-container {
        background: #F4F5F7;
        text-align: center;
        padding: 40px 20px;
    }
    .hero-badge {
        display: inline-block;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #00875A;
        background: #E3FBF0;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 16px;
    }
    .hero-stats {
        display: inline-flex;
        background: white;
        border-radius: 14px;
        padding: 16px 32px;
        box-shadow: 0 1px 3px rgba(0,0,0,.06);
        border: 1px solid #ECEEF2;
        gap: 24px;
        margin-top: 24px;
    }
    .stat-val { font-family: 'Space Grotesk'; font-weight: 700; font-size: 18px; color: #1A1D23; }
    .stat-label { font-size: 12px; color: #9CA1AE; }

    /* Custom Containers/Cards */
    .custom-card {
        background: white;
        padding: 24px;
        border-radius: 14px;
        border: 2px solid #ECEEF2;
        margin-bottom: 16px;
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }
    .card-num {
        background: #E8EAF0;
        color: #7A7F8D;
        width: 28px; height: 28px;
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700;
        font-family: 'Space Grotesk';
    }
    .active-num { background: #0066FF; color: white; }
    .done-num { background: #00B37E; color: white; }

    /* Inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
        border: 1.5px solid #E2E4E9;
    }
    
    /* Submit Button */
    .stButton button {
        width: 100%;
        background-color: #0066FF;
        color: white;
        border-radius: 12px;
        padding: 12px 0;
        font-weight: 600;
        border: none;
    }
    .stButton button:hover {
        background-color: #0052CC;
        color: white;
    }
    
    /* Result Box */
    .result-box {
        text-align: center;
        padding: 60px 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
# Initialize session state for all fields
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
    st.session_state.status = ""
    st.session_state.form_data = {
        "name": "", "phone": "", "email": "",
        "city": "", "state": "", "zip": "",
        "skills": [], "years": "", "roof": "No",
        "tasks": [], "vehicle": "No", "license": "No",
        "ladder": "No", "tools": [], "insurance": "No",
        "start_date": "", "days": [], "counties": "", "radius": "30 miles"
    }

# --- HELPER FUNCTIONS ---
def update_progress():
    d = st.session_state.form_data
    # Logic to calculate sections completed (similar to React logic)
    sections = [
        bool(d['name'] and d['phone'] and d['email']), # Contact
        bool(d['skills'] and d['years']), # Experience
        bool(d['vehicle'] != "No" and d['license'] != "No"), # Vehicle
        bool(d['insurance'] != "No"), # Insurance
        bool(d['start_date'] and d['days']), # Availability
        bool(d['counties']) # Area
    ]
    return int((sum(sections) / 6) * 100)

def submit_logic():
    d = st.session_state.form_data
    
    # Validation
    if not d['name'] or not d['phone'] or not d['email'] or not d['counties']:
        st.error("Please fill in all required fields marked with *")
        return

    # "The Brain" Logic (Directly translated from React)
    app_status = "QUALIFIED"
    is_rejected = False
    
    if "No installation experience" in d['skills']: is_rejected = True
    if d['vehicle'] == "No": is_rejected = True
    if d['license'] == "No": is_rejected = True
    if d['insurance'] == "No": is_rejected = True

    if is_rejected:
        app_status = "REJECTED"
    else:
        has_sat_exp = any(s in ["Satellite systems (DirecTV, HughesNet)", "Starlink installation"] for s in d['skills'])
        has_ins = d['insurance'] == "Yes, I currently have insurance"
        valid_vehicle = d['vehicle'] in ["Yes - Truck", "Yes - Van"]
        
        if has_sat_exp and has_ins and valid_vehicle:
            app_status = "PRIORITY"

    st.session_state.status = app_status
    st.session_state.submitted = True

# --- MAIN APP RENDER ---

if st.session_state.submitted:
    # === RESULT SCREEN ===
    status = st.session_state.status
    data = st.session_state.form_data
    
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if status == "REJECTED":
            st.markdown(f"""
            <div style="background:#FFF1F0; width:64px; height:64px; border-radius:50%; margin:0 auto; display:flex; align-items:center; justify-content:center;">
                <span style="font-size:30px">❌</span>
            </div>
            <h2>Application Not Accepted</h2>
            <p style="color:#7A7F8D">Thank you for your interest. Based on our current requirements, we're unable to proceed with your application at this time.</p>
            """, unsafe_allow_html=True)
        else:
            priority_badge = ""
            if status == "PRIORITY":
                priority_badge = """<div style="background:#FFF7ED; color:#B45309; border:1px solid #FBBF24; padding:4px 14px; border-radius:20px; display:inline-block; font-weight:600; font-size:13px; margin-bottom:10px;">★ Priority Candidate</div>"""
            
            st.markdown(f"""
            <div style="background:#ECFDF3; width:64px; height:64px; border-radius:50%; margin:0 auto; display:flex; align-items:center; justify-content:center;">
                <span style="font-size:30px">✅</span>
            </div>
            <br>
            {priority_badge}
            <h2>Application Received</h2>
            <p style="color:#7A7F8D">Thank you, <strong>{data['name']}</strong>. Your qualifications are a strong match.</p>
            <p style="color:#7A7F8D">Our hiring team will review your file and contact you at <strong>{data['phone']}</strong> within 24 hours.</p>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Start New Application"):
        st.session_state.submitted = False
        st.rerun()

else:
    # === HERO SECTION ===
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">NOW HIRING</div>
        <h1>Starlink Installation Technician</h1>
        <p style="color: #7A7F8D;">Apply to become a Certified Field Technician — Independent Contractor (1099)</p>
        <div class="hero-stats">
            <div><div class="stat-val">$45-75</div><div class="stat-label">Per Install</div></div>
            <div style="width:1px; background:#ECEEF2;"></div>
            <div><div class="stat-val">Flexible</div><div class="stat-label">Schedule</div></div>
            <div style="width:1px; background:#ECEEF2;"></div>
            <div><div class="stat-val">Training</div><div class="stat-label">Provided</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === PROGRESS BAR ===
    progress = update_progress()
    st.progress(progress)
    st.caption(f"Application progress: {progress}%")

    # === FORM SECTIONS ===
    
    # 1. Contact Info
    with st.container(border=True):
        st.markdown('### 👤 1. Contact Information')
        st.session_state.form_data['name'] = st.text_input("Full Name *", value=st.session_state.form_data['name'])
        c1, c2 = st.columns(2)
        st.session_state.form_data['phone'] = c1.text_input("Phone Number *", value=st.session_state.form_data['phone'])
        st.session_state.form_data['email'] = c2.text_input("Email Address *", value=st.session_state.form_data['email'])
        
        st.session_state.form_data['street'] = st.text_input("Street Address", value=st.session_state.form_data.get('street', ''))
        c3, c4, c5 = st.columns([2,1,1])
        st.session_state.form_data['city'] = c3.text_input("City", value=st.session_state.form_data['city'])
        st.session_state.form_data['state'] = c4.text_input("State", value=st.session_state.form_data['state'])
        st.session_state.form_data['zip'] = c5.text_input("Zip", value=st.session_state.form_data['zip'])

    # 2. Experience
    with st.container(border=True):
        st.markdown('### 🛠 2. Experience & Qualifications')
        st.session_state.form_data['skills'] = st.multiselect("Installation Experience *", SKILLS, default=st.session_state.form_data['skills'])
        
        c1, c2 = st.columns(2)
        st.session_state.form_data['years'] = c1.selectbox("Years of Experience *", [""] + YEARS_OPTIONS, index=0)
        st.session_state.form_data['roof'] = c2.radio("Experience working on roofs? *", ["Yes, comfortable", "Yes, limited", "No, but willing", "No"], horizontal=True)
        
        st.markdown("**Comfortable with tasks:**")
        cols = st.columns(2)
        tasks_list = ["Drilling through walls/roofs", "Running cables in attics", "Working at heights (20ft+)", "Troubleshooting network issues"]
        selected_tasks = []
        for i, task in enumerate(tasks_list):
            if cols[i % 2].checkbox(task, key=f"task_{i}"):
                selected_tasks.append(task)
        st.session_state.form_data['tasks'] = selected_tasks

    # 3. Vehicle & Equipment
    with st.container(border=True):
        st.markdown('### 🚗 3. Vehicle & Equipment')
        st.session_state.form_data['vehicle'] = st.radio("Do you have a reliable vehicle? *", ["Yes - Truck", "Yes - Van", "Yes - SUV", "No"], horizontal=True)
        
        c1, c2 = st.columns(2)
        st.session_state.form_data['license'] = c1.radio("Valid Driver's License? *", ["Yes", "No"], horizontal=True)
        st.session_state.form_data['ladder'] = c2.radio("28ft+ extension ladder? *", ["Yes, I own one", "No, but I can get one", "No"], horizontal=True)
        
        st.session_state.form_data['tools'] = st.multiselect("Tools Owned", TOOLS, default=st.session_state.form_data['tools'])

    # 4. Insurance
    with st.container(border=True):
        st.markdown('### 🛡 4. Insurance')
        st.session_state.form_data['insurance'] = st.radio("General Liability Insurance *", ["Yes, I currently have insurance", "No, but I can obtain within 1 week", "No, but I can obtain within 2 weeks", "No"])

    # 5. Availability
    with st.container(border=True):
        st.markdown('### 📅 5. Availability')
        c1, c2 = st.columns(2)
        st.session_state.form_data['start_date'] = c1.selectbox("When can you start?", ["", "Immediately", "Within 1 week", "Within 2 weeks"])
        c2.text_input("Employment Type", value="Independent Contractor (1099)", disabled=True)
        
        st.session_state.form_data['days'] = st.multiselect("Days Available", DAYS, default=st.session_state.form_data['days'])

    # 6. Service Area
    with st.container(border=True):
        st.markdown('### 📍 6. Service Area')
        st.session_state.form_data['counties'] = st.text_area("Counties you're willing to work in *", placeholder="e.g. Orange County, Lake County...", value=st.session_state.form_data['counties'])
        st.session_state.form_data['radius'] = st.select_slider("Max travel radius", options=RADIUS_OPTIONS, value=st.session_state.form_data['radius'])

    # === SUBMIT ===
    if st.button("Submit Application"):
        submit_logic()
        if st.session_state.submitted:
            st.rerun()

    st.markdown("""
    <div style="text-align: center; color: #9CA1AE; font-size: 12px; margin-top: 16px;">
        By submitting this application, you agree to our terms and conditions. All information is kept confidential.
    </div>
    """, unsafe_allow_html=True)
