import streamlit as st
import sqlite3
import base64
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Vergecom Careers", page_icon="📡", layout="centered")

# --- ASSETS & IMAGES ---
# Instructions: Place your images in the same folder as this script.
# Rename them to: slide1.jpeg, slide2.jpeg, slide3.jpeg
# If the files aren't found, it defaults to a high-quality Unsplash image.

def get_base64_image(image_filename):
    """Helper to convert local image to base64 for background"""
    try:
        with open(image_filename, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Try to load your local images
img1 = get_base64_image("slide1.jpeg")
img2 = get_base64_image("slide2.jpeg") 
img3 = get_base64_image("slide3.jpeg")

# Default fallback image (Unsplash) if local files are missing
default_bg = "https://images.unsplash.com/photo-1541873676-a18131494184?q=80&w=2518&auto=format&fit=crop"

# Construct CSS for the slideshow
# If we found local images, we cycle them. If not, we stay static.
if img1 and img2 and img3:
    slideshow_css = f"""
    @keyframes slide {{
        0% {{ background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url("data:image/jpeg;base64,{img1}"); }}
        33% {{ background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url("data:image/jpeg;base64,{img2}"); }}
        66% {{ background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url("data:image/jpeg;base64,{img3}"); }}
        100% {{ background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url("data:image/jpeg;base64,{img1}"); }}
    }}
    .stApp {{
        animation: slide 15s infinite;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        transition: background-image 1s ease-in-out;
    }}
    """
else:
    # Fallback Static Background
    slideshow_css = f"""
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), url('{default_bg}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """

# --- CSS STYLING ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    /* Apply the slideshow or static background calculated above */
    {slideshow_css}

    /* Global Fonts */
    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    /* Headers */
    h1, h2, h3 {{
        color: #0066FF !important;
        font-weight: 700 !important;
    }}
    
    /* GLASS CARDS */
    .glass-card {{
        background-color: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        padding: 40px;
        margin-bottom: 20px;
        text-align: center;
    }}
    
    /* Standard Streamlit Containers made to look like glass cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }}

    /* BUTTONS */
    .stButton button {{
        background-color: #0066FF !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 0.8rem 2rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 102, 255, 0.5) !important;
        transition: transform 0.2s ease !important;
        width: 100%;
    }}
    .stButton button:hover {{
        transform: scale(1.02);
        background-color: #0052CC !important;
    }}
    
    /* INPUTS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        color: #111827;
    }}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'  # Start at landing page

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
# PAGE 1: LANDING PAGE
# ==========================================
if st.session_state.page == 'landing':
    
    # Empty container to push content down slightly
    st.write("")
    st.write("")

    # Main "Glass" Landing Card
    st.markdown("""
    <div class="glass-card">
        <div style="font-size: 60px; margin-bottom: 10px;">📡</div>
        <h1 style="margin: 0; font-size: 42px; color: #111827 !important;">Starlink Technician</h1>
        <p style="font-size: 18px; color: #4B5563; margin-top: 10px;">
            Vergecom is hiring experienced <strong>Independent Contractors (1099)</strong> <br>
            for high-volume residential & commercial installations.
        </p>
        <hr style="margin: 25px 0; border: 0; border-top: 1px solid #E5E7EB;">
        
        <div style="display: flex; justify-content: space-around; text-align: left; margin-bottom: 30px;">
            <div>
                <h3 style="margin:0; font-size: 20px;">💰 Pay</h3>
                <p style="margin:0; color: #374151;">$1,200 - $1,800 / week</p>
            </div>
            <div>
                <h3 style="margin:0; font-size: 20px;">📍 Location</h3>
                <p style="margin:0; color: #374151;">Greater Metro Area</p>
            </div>
        </div>

        <div style="text-align: left; background: #F9FAFB; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
            <strong style="color: #0066FF;">REQUIREMENTS:</strong>
            <ul style="margin-top: 10px; color: #4B5563; padding-left: 20px;">
                <li>Must have reliable <strong>Truck, Van, or SUV</strong>.</li>
                <li>Must have <strong>28ft Extension Ladder</strong>.</li>
                <li>Must have basic power tools (Drill, Impact, Hand Tools).</li>
                <li>Valid Driver's License & Insurance required.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # The "Get Started" Button
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        if st.button("GET STARTED ➤"):
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

    st.markdown("""
    <div style="text-align: center; background: rgba(255,255,255,0.9); padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h2 style="margin:0;">Technician Application</h2>
        <p style="margin:0; color: #666;">Please complete the form below.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- FORM CONSTANTS ---
    SKILLS = [
        "Satellite systems (DirecTV, HughesNet)", "Starlink installation",
        "TV mounting", "Security camera installation",
        "Low voltage wiring (Cat5/Coax)", "Smart home systems",
        "No installation experience"
    ]
    TOOLS = ["Power drill", "Crimper tools", "Cable tester", "Fish tape", "Stud finder", "Signal meter"]
    
    # --- FORM INPUTS ---
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
        skills = st.multiselect("Installation Experience *", SKILLS)
        c1, c2 = st.columns(2)
        years = c1.selectbox("Years of Experience", ["< 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"])
        roof = c2.radio("Roof Work?", ["Yes", "Limited", "No"], horizontal=True)

    with st.container(border=True):
        st.subheader("🚗 Vehicle & Tools")
        vehicle = st.radio("Do you have a reliable vehicle?", ["Yes - Truck/Van", "Yes - SUV", "No"], horizontal=True)
        c1, c2 = st.columns(2)
        license_valid = c1.radio("Valid Driver's License?", ["Yes", "No"], horizontal=True)
        ladder = c2.radio("Own a 28ft+ Ladder?", ["Yes", "No"], horizontal=True)
        user_tools = st.multiselect("Tools Owned", TOOLS)

    with st.container(border=True):
        st.subheader("🛡 Requirements")
        insurance = st.radio("General Liability Insurance", ["Yes, I have it", "No, but will get it", "No"])
        counties = st.text_area("Counties you can cover *")

    # --- SUBMIT LOGIC ---
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
            
            # Show Success
            st.balloons()
            st.markdown(f"""
            <div class="glass-card">
                <h1 style="color:#00B37E !important;">Application Received!</h1>
                <p>Thank you <strong>{name}</strong>.</p>
                <p>We will review your info and contact you at <strong>{phone}</strong> shortly.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
