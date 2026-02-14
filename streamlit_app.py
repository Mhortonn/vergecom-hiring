import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vergecom Hiring",
    page_icon="🚀",
    layout="centered"
)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    # Create table if it doesn't exist
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
    # Convert list to string for storage
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

# Initialize DB on startup
init_db()

# --- SIDEBAR (ADMIN LOGIN) ---
with st.sidebar:
    st.header("🔧 Admin Login")
    admin_password = st.text_input("Enter Password", type="password")
    
    # Check password (default is "admin123")
    if admin_password == "admin123":
        admin_mode = True
        st.success("✅ Admin Mode Active")
    else:
        admin_mode = False

# ==========================================
# LOGIC: SHOW ADMIN PANEL OR SHOW FORM
# ==========================================

if admin_mode:
    # --- ADMIN VIEW ---
    st.title("📋 Candidate List")
    
    df = get_all_candidates()
    
    if df.empty:
        st.info("No applications received yet.")
    else:
        # Display the data
        st.dataframe(
            df,
            column_config={
                "name": "Name",
                "phone": "Phone",
                "skills": "Experience",
                "timestamp": "Applied On"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name='vergecom_candidates.csv',
            mime='text/csv',
        )

else:
    # --- CANDIDATE VIEW ---
    st.title("🚀 Vergecom Hiring Portal")

    # Job Card
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("### 📡 **Field Technician / Installer**")
            st.write("We are looking for experienced installers for **Satellite**, **Starlink**, and **A/V systems**.")
            st.caption("📍 **Location:** Greater Metro Area | 🕒 **Type:** Contract/Full-time")
        with col2:
            st.metric(label="Est. Weekly Pay", value="$1,200 - $1,800")

    with st.expander("▶ Show Requirements & Tools Needed"):
        st.write("""
        * **Vehicle:** Must have a truck/van capable of carrying a 28ft ladder.
        * **Tools:** Drill, signal meter, hand tools, PPE.
        * **Experience:** Prior experience with coax/cat5 cabling preferred.
        """)

    st.divider()

    # The Form
    st.progress(16, text="**16% completed**")
    st.subheader("Installation Experience")
    st.write("Please select at least one option to continue.")

    # Inputs
    col_a, col_b = st.columns(2)
    with col_a:
        candidate_name = st.text_input("Full Name", placeholder="e.g. John Smith")
    with col_b:
        candidate_phone = st.text_input("Phone Number", placeholder="e.g. 555-0199")

    st.write("") 

    # Skills Checkboxes
    st.write("**Select your skills:**")
    skills_options = [
        "**Satellite systems** (DirecTV, HughesNet, Dish Network)",
        "**Starlink installation**",
        "**TV mounting**",
        "**Security camera installation**",
        "**Home theater/audio systems**",
        "**Low voltage wiring** (Cat5/Cat6/Coax)"
    ]
    
    selected_skills = []
    for skill in skills_options:
        with st.container(border=True):
            if st.checkbox(skill):
                clean_skill = skill.replace("**", "")
                selected_skills.append(clean_skill)

    st.write("")

    # Submit Button
    if st.button("Submit Application ➤", type="primary", use_container_width=True):
        if not candidate_name or not candidate_phone:
            st.error("⚠️ Please fill in your Name and Phone Number.")
        elif not selected_skills:
            st.error("⚠️ Please select at least one skill.")
        else:
            add_candidate(candidate_name, candidate_phone, selected_skills)
            st.balloons()
            st.success("✅ Application Received!")
            st.write(f"Thank you, **{candidate_name}**. Our hiring team will contact you at **{candidate_phone}** shortly.")
