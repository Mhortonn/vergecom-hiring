
import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Skill Assessment", page_icon="📝")

# --- SESSION STATE SETUP ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "selected_skills" not in st.session_state:
    st.session_state.selected_skills = []

# ==========================================
# PAGE 1: SKILLS SELECTION (Like your Image)
# ==========================================
if st.session_state.step == 1:
    
    # 1. The Progress Bar (16% completed)
    st.progress(16, text="16% completed")
    
    # 2. The Header Text
    st.subheader("You didn't select any installation experience.")
    st.write("Please select at least one option or specify if you have other experience.")
    
    st.write("**Select one or more**")
    
    # 3. The Options (Styled as Cards)
    # We use 'border=True' to make them look like the boxes in your screenshot
    
    skills_list = [
        "Satellite systems (DirecTV, HughesNet, Dish Network)",
        "Starlink installation",
        "TV mounting",
        "Security camera installation",
        "Home theater/audio systems",
        "Low voltage wiring (Cat5/Cat6/Coax)"
    ]
    
    selected = []
    
    # This loop creates the "Card" look
    for skill in skills_list:
        with st.container(border=True):
            # Checkbox inside a border box
            is_checked = st.checkbox(skill, key=skill)
            if is_checked:
                selected.append(skill)
    
    # 4. The "Next" Button
    st.write("") # Spacer
    if st.button("Continue to Interview ➤", type="primary", use_container_width=True):
        if not selected:
            st.error("Please select at least one skill to continue.")
        else:
            st.session_state.selected_skills = selected
            st.session_state.step = 2
            st.rerun()

# ==========================================
# PAGE 2: THE AI INTERVIEWER
# ==========================================
elif st.session_state.step == 2:
    
    # Setup Sidebar with API Key
    with st.sidebar:
        api_key = st.text_input("Enter Gemini API Key", type="password")
        st.write(f"**Selected Skills:**")
        for s in st.session_state.selected_skills:
            st.caption(f"✅ {s}")
        
        if st.button("Start Over"):
            st.session_state.step = 1
            st.rerun()

    st.title("🤖 Skills Interview")

    if not api_key:
        st.warning("Please enter your API Key in the sidebar to start the interview.")
        st.stop()
        
    # Initialize Chat
    if "messages" not in st.session_state:
        skills_text = ", ".join(st.session_state.selected_skills)
        st.session_state.messages = [
            {"role": "model", "content": f"I see you have experience with: **{skills_text}**. Let's discuss that. Pick one of those skills and tell me about a difficult installation you handled."}
        ]

    # Show Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if user_input := st.chat_input("Type your answer here..."):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("model"):
            # Simple chat logic
            response = model.generate_content(f"User is interviewing for: {st.session_state.selected_skills}. User said: {user_input}. act as a hiring manager.")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
