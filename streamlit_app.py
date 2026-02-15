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

# --- CUSTOM CSS (BACKGROUND & GLASS CARDS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

    /* 1. MAIN BACKGROUND IMAGE */
    /* I used a high-quality Unsplash image of a Satellite Dish. 
       To use your own Gen 3 Dish image: 
       1. Upload your photo to your GitHub repository (e.g., 'background.jpg').
       2. Change the URL below to: 'https://raw.githubusercontent.com/YOUR_USERNAME/vergecom-hiring/main/background.jpg' 
    */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                          url('https://images.unsplash.com/photo-1541873676-a18131494184?q=80&w=2518&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'DM Sans', sans-serif;
    }

    /* 2. HEADERS */
    h1, h2, h3 {
        color: #0066FF !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* 3. GLASS CARDS (White with slight transparency & blur) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.95); /* 95% Opaque White */
        backdrop-filter: blur(10px); /* Frosted Glass Effect */
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin-bottom: 24px;
    }

    /* 4. INPUT FIELDS (Clean styling) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        color: #1F2937;
    }

    /* 5. SUBMIT BUTTON (Starlink Blue) */
    .stButton button {
        background-color: #0066FF !important;
        color: white !important;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        border: none;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(0, 102, 255, 0.4);
    }
    .stButton button:hover {
        background-color: #0052CC !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 102, 255, 0.6);
    }

    /* 6. HERO SECTION */
    .hero-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 40px;
        border-top: 6px solid #0066FF;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }
    .hero-badge {
        background: #E3FBF0;
        color: #00875A;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
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
    <div style="text-align:center; padding: 60px; background: rgba(255,255,255,0.95); border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">
        <div style="font-size: 70px; margin-bottom: 20px;">✅</div>
        <h2 style="color: #0066FF; margin-bottom: 10px;">Application Received</h2>
        <p style="font-size: 18px; color: #4B5563;">Thank you, <strong>{st.session_state.form['name']}</strong>.</p>
        <p style="color: #6B7280;">Our team will contact you at <strong>{st.session_state.form['phone']}</strong> within 24 hours.</p>
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
        <h1 style="margin: 10px 0; font-size: 2.5rem;">Starlink Installation Technician</h1>
        <p style="color: #4B5563; font-size: 1.1rem;">Apply to become a Certified Field Technician (1099)</p>
    </div>
    """, unsafe_allow_html=True)

    # PROGRESS BAR (Custom styling via Streamlit)
    progress = 0
    if st.session_state.form['name']: progress += 20
