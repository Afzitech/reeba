import streamlit as st

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="XAI Career Guide", layout="centered")

# Custom CSS for a clean chatbot look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    .explanation-box { background-color: #e8f4f8; padding: 15px; border-left: 5px solid #2980b9; border-radius: 5px; margin: 10px 0; }
    .skill-tag { display: inline-block; padding: 2px 10px; margin: 2px; border-radius: 15px; background: #d1d8e0; font-size: 0.8em; }
    </style>
    """, unsafe_allow_name=True)

# --- SESSION STATE INITIALIZATION ---
# This keeps track of the user's progress through the steps
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.scores = {"logical": 0, "creative": 0, "comm": 0, "prob_solve": 0, "analytical": 0}
    st.session_state.user_data = {}

# --- HELPER FUNCTIONS ---
def next_step(): st.session_state.step += 1
def restart(): st.session_state.step = 1; st.session_state.scores = {k: 0 for k in st.session_state.scores}

# --- DATA: COLLEGES IN KERALA (Sample Set) ---
COLLEGE_DB = {
    "Thiruvananthapuram": [
        {"name": "College of Engineering (CET)", "type": "Govt", "desc": "Top-tier for Tech/Architecture."},
        {"name": "University College", "type": "Govt", "desc": "Excellent for Humanities and Pure Sciences."},
        {"name": "Government Medical College", "type": "Govt", "desc": "Premier institute for Medical studies."}
    ],
    "Ernakulam": [
        {"name": "CUSAT", "type": "Govt/Aided", "desc": "Renowned for Engineering and Marine Sciences."},
        {"name": "Maharajas College", "type": "Govt", "desc": "Iconic for Arts, Commerce, and Science."},
        {"name": "St. Albert's College", "type": "Aided", "desc": "Strong placement record for Commerce/Management."}
    ],
    "Kozhikode": [
        {"name": "NIT Calicut", "type": "Govt", "desc": "National importance for Engineering/Design."},
        {"name": "Farook College", "type": "Aided", "desc": "Top rated for Humanities and Commerce."},
        {"name": "Govt. Arts & Science College", "type": "Govt", "desc": "Diverse courses in various streams."}
    ]
}

# --- STEP 1: BASIC INFO ---
if st.session_state.step == 1:
    st.title("🎓 AI Career & College Guide")
    st.subheader("Step 1: Tell us about yourself")
    
    name = st.text_input("Enter your name:")
    stream = st.selectbox("What is your Plus Two stream?", 
                         ["Science (Biology)", "Science (Computer Science)", "Commerce", "Humanities"])
    
    if st.button("Start Aptitude Test") and name:
        st.session_state.user_data['name'] = name
        st.session_state.user_data['stream'] = stream
        next_step()

# --- STEP 2: APTITUDE TEST ---
elif st.session_state.step == 2:
    st.title("🧠 Interest & Skill Identification")
    st.info("Answer these 5 questions. There are no wrong answers, just preferences!")

    q1 = st.radio("1. If you see a broken gadget, you would:", 
                 ["Try to figure out why it broke (Analytical)", "Try to fix it using tools (Problem Solving)", "Think of a new design for it (Creative)"])
    q2 = st.radio("2. In a group project, you prefer:", 
                 ["Organizing tasks and timelines (Logical)", "Presenting the ideas to the class (Communication)", "Researching the core data (Analytical)"])
    q3 = st.radio("3. You enjoy solving puzzles like Sudoku or Riddles.", ["Yes, very much", "Sometimes", "Not really"])
    q4 = st.radio("4. Do you like explaining complex things to others?", ["Yes, it's easy", "I prefer writing it down", "I find it difficult"])
    q5 = st.radio("5. When facing a math problem, you:", ["Use a formula step-by-step", "Look for a shortcut", "Visualize the logic"])

    if st.button("Calculate My Profile"):
        # Logic to update scores based on selections
        if "Analytical" in q1: st.session_state.scores["analytical"] += 2
        if "Problem Solving" in q1: st.session_state.scores["prob_solve"] += 2
        if "Logical" in q2: st.session_state.scores["logical"] += 2
        if "Communication" in q2: st.session_state.scores["comm"] += 2
        if "Yes" in q3: st.session_state.scores["logical"] += 2; st.session_state.scores["analytical"] += 1
        if "Yes" in q4: st.session_state.scores["comm"] += 2
        next_step()

# --- STEP 3 & 4: RECOMMENDATIONS & EXPLAINABILITY ---
elif st.session_state.step == 3:
    st.title("🎯 Your Career Path Analysis")
    s = st.session_state.scores
    
    # Rule-based Logic for Recommendations
    recommendations = []
    if s["logical"] >= 2 or s["analytical"] >= 2:
        recommendations.append({"field": "Engineering & Technology", "why": "Your high scores in Logical and Analytical thinking suggest you enjoy structured problem solving."})
    if s["comm"] >= 2:
        recommendations.append({"field": "Management & Law", "why": "Your communication aptitude makes you a great fit for leadership and advocacy roles."})
    if s["creative"] >= 1 or s["prob_solve"] >= 2:
        recommendations.append({"field": "Design & Innovation", "why": "You show a preference for hands-on problem solving and visual thinking."})
    
    # Default fallback
    if not recommendations:
        recommendations.append({"field": "General Academics", "why": "Based on your balanced profile, a versatile degree would suit you best."})

    st.subheader(f"Recommendations for {st.session_state.user_data['name']}:")
    
    for rec in recommendations[:3]:
        with st.expander(f"Recommended Field: {rec['field']}"):
            st.write(f"**Reasoning:** {rec['why']}")
            st.write("**Suggested Courses:**")
            if rec['field'] == "Engineering & Technology":
                courses = ["B.Tech Computer Science", "Data Science", "B.Arch"]
            elif rec['field'] == "Management & Law":
                courses = ["BBA", "Integrated LLB", "Economics"]
            else:
                courses = ["B.Des (Design)", "BCA", "Fine Arts"]
            
            for c in courses: st.write(f"- {c}")

    # --- STEP 6: SKILL GAP ANALYSIS ---
    st.divider()
    st.subheader("🔍 Skill Gap Analysis")
    st.write("To succeed in these careers, here is what you need:")
    
    cols = st.columns(2)
    with cols[0]:
        st.success("**Skills You Have**")
        for skill, score in s.items():
            if score >= 2: st.markdown(f"✅ {skill.capitalize()}")
    with cols[1]:
        st.warning("**Skills to Develop**")
        for skill, score in s.items():
            if score < 2: st.markdown(f"⚠️ {skill.capitalize()}")
            
    st.info("**Why?** High-level roles require a balance of technical and soft skills. Strengthening your 'warning' areas will make you a 100% match for top companies.")

    if st.button("Find Colleges in Kerala"):
        next_step()

# --- STEP 7: COLLEGE RECOMMENDATION ---
elif st.session_state.step == 4:
    st.title("🏫 Recommended Colleges")
    district = st.selectbox("Select your preferred District in Kerala:", list(COLLEGE_DB.keys()))
    
    colleges = COLLEGE_DB.get(district, [])
    
    for col in colleges:
        with st.container():
            st.markdown(f"### {col['name']}")
            st.write(f"**Type:** {col['type']}")
            st.write(f"**Why this college:** {col['desc']}")
            st.markdown("---")

    if st.button("Start Over"):
        restart()
