import streamlit as st

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="XAI Career Guide 2026", layout="wide")

# Corrected CSS with the fixed 'unsafe_allow_html' parameter
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #2e7d32; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #1b5e20; border: none; }
    .explanation-box { background-color: #ffffff; padding: 20px; border-left: 6px solid #1976d2; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 15px 0; }
    .skill-tag { display: inline-block; padding: 5px 15px; margin: 4px; border-radius: 20px; background: #e3f2fd; color: #1565c0; font-weight: 500; font-size: 0.85em; }
    .missing-skill { background-color: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.scores = {"logical": 0, "creative": 0, "comm": 0, "prob_solve": 0, "analytical": 0}
    st.session_state.user_data = {}
    st.session_state.recommended_fields = []
    st.session_state.top_courses = []

# --- DATA: KERALA COLLEGES (2026 Update) ---
COLLEGE_DB = {
    "Thiruvananthapuram": [
        {"name": "College of Engineering (CET)", "type": "Govt", "fields": ["Engineering & Technology", "Design & Innovation"]},
        {"name": "University College", "type": "Govt", "fields": ["Humanities", "General Academics"]},
        {"name": "Government Medical College", "type": "Govt", "fields": ["Medical & Healthcare"]}
    ],
    "Ernakulam": [
        {"name": "Model Engineering College (MEC)", "type": "Govt-Aided", "fields": ["Engineering & Technology"]},
        {"name": "Maharajas College", "type": "Govt", "fields": ["Humanities", "Management & Law"]},
        {"name": "CUSAT", "type": "Govt", "fields": ["Engineering & Technology", "Management & Law"]}
    ],
    "Kozhikode": [
        {"name": "NIT Calicut", "type": "Central Govt", "fields": ["Engineering & Technology", "Design & Innovation"]},
        {"name": "Farook College", "type": "Aided", "fields": ["Management & Law", "Humanities"]},
        {"name": "IIM Kozhikode", "type": "Central Govt", "fields": ["Management & Law"]}
    ],
    "Thrissur": [
        {"name": "Govt. Engineering College (GECT)", "type": "Govt", "fields": ["Engineering & Technology"]},
        {"name": "Kerala Agricultural University", "type": "Govt", "fields": ["General Academics"]}
    ]
}

# --- STEP 1: WELCOME & STREAM ---
if st.session_state.step == 1:
    st.title("🎓 Explainable AI: Career & College Guide")
    st.write("Welcome! This system uses **Rule-Based Inference** to map your skills to the best possible career.")
    
    with st.container():
        name = st.text_input("What is your name?")
        stream = st.selectbox("Select your Plus Two stream:", 
                             ["Science (Biology)", "Science (Computer Science)", "Commerce", "Humanities"])
        
        if st.button("Proceed to Aptitude Test") and name:
            st.session_state.user_data['name'] = name
            st.session_state.user_data['stream'] = stream
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: INTEREST TEST (Indirect Evaluation) ---
elif st.session_state.step == 2:
    st.header("🧠 Step 2: Aptitude Evaluation")
    st.info("Choose the option that best describes your natural reaction.")

    q1 = st.radio("1. When you get a new LEGO set or a complex puzzle, you:",
                 ["Follow the manual exactly (Logical)", "Build something entirely new (Creative)", "Look for the most efficient way to finish (Analytical)"])
    q2 = st.radio("2. If your friend is upset, you usually:",
                 ["Listen and find the right words to help (Communication)", "Think of a practical solution to their problem (Problem Solving)", "Analyze why they are feeling that way (Analytical)"])
    q3 = st.radio("3. You are given a mystery box. You prefer to:",
                 ["Guess the contents based on weight and sound (Analytical)", "Try different ways to pry it open (Problem Solving)", "Draw what you think is inside (Creative)"])
    q4 = st.radio("4. In a group debate, you are the one who:",
                 ["Organizes the facts and evidence (Logical)", "Convinces others with your speech (Communication)", "Sees a perspective no one else noticed (Creative)"])

    if st.button("Analyze My Aptitude"):
        # Rule-based scoring logic
        if "Logical" in q1 or "Logical" in q4: st.session_state.scores["logical"] += 3
        if "Creative" in q1 or "Creative" in q3 or "Creative" in q4: st.session_state.scores["creative"] += 3
        if "Analytical" in q1 or "Analytical" in q2 or "Analytical" in q3: st.session_state.scores["analytical"] += 3
        if "Communication" in q2 or "Communication" in q4: st.session_state.scores["comm"] += 3
        if "Problem Solving" in q2 or "Problem Solving" in q3: st.session_state.scores["prob_solve"] += 3
        
        st.session_state.step = 3
        st.rerun()

# --- STEP 3: FIELD RECOMMENDATION (Explainable AI) ---
elif st.session_state.step == 3:
    st.header("🎯 Recommended Fields")
    s = st.session_state.scores
    
    # Inference Engine
    fields = []
    if s["logical"] >= 3 or s["analytical"] >= 3:
        fields.append({"name": "Engineering & Technology", "reason": "Your high scores in Logical and Analytical thinking indicate a strong ability to handle structured systems and data."})
    if s["comm"] >= 3:
        fields.append({"name": "Management & Law", "reason": "Your communication aptitude suggests you excel at negotiation, leadership, and articulating complex ideas."})
    if s["creative"] >= 3:
        fields.append({"name": "Design & Innovation", "reason": "Your creative score shows a preference for non-linear thinking and visual problem-solving."})
    if s["prob_solve"] >= 3 and st.session_state.user_data['stream'] == "Science (Biology)":
        fields.append({"name": "Medical & Healthcare", "reason": "Your problem-solving skills combined with your biology background make you a fit for diagnostic roles."})

    st.session_state.recommended_fields = fields[:3]
    
    for f in st.session_state.recommended_fields:
        st.markdown(f"""
        <div class="explanation-box">
            <h3>{f['name']}</h3>
            <p><b>Why?</b> {f['reason']}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Move to Course Selection"):
        st.session_state.step = 4
        st.rerun()

# --- STEP 4 & 5: COURSE & CAREER RECOMMENDATION ---
elif st.session_state.step == 4:
    st.header("📚 Course & Career Roadmap")
    
    # Mapping logic for Courses and Careers
    course_map = {
        "Engineering & Technology": [
            {"course": "B.Tech Computer Science", "career": "Software Architect", "skills": ["Coding", "Logic", "Math"]},
            {"course": "Data Science", "career": "Data Analyst", "skills": ["Statistics", "SQL", "Python"]}
        ],
        "Management & Law": [
            {"course": "BBA / MBA", "career": "Project Manager", "skills": ["Leadership", "Planning", "Comm"]},
            {"course": "Integrated LLB", "career": "Corporate Lawyer", "skills": ["Legal Research", "Drafting", "Oratory"]}
        ],
        "Design & Innovation": [
            {"course": "B.Des (UI/UX)", "career": "Product Designer", "skills": ["Adobe Suite", "Empathy", "Prototyping"]},
            {"course": "B.Arch", "career": "Urban Planner", "skills": ["Spatial Awareness", "Sketching", "CAD"]}
        ]
    }

    selected_courses = []
    for f in st.session_state.recommended_fields:
        field_courses = course_map.get(f['name'], [])
        for c in field_courses:
            selected_courses.append(c)
    
    st.session_state.top_courses = selected_courses[:4]

    for item in st.session_state.top_courses:
        with st.expander(f"📖 {item['course']} ➔ {item['career']}"):
            st.write(f"**Career Path:** This course leads to a career as a **{item['career']}**.")
            st.write("**Required Skills:**")
            for sk in item['skills']:
                st.markdown(f'<span class="skill-tag">{sk}</span>', unsafe_allow_html=True)
            
            # STEP 6: Skill Gap Analysis
            st.write("**Skill Gap Analysis:**")
            user_has = ["Logic", "Comm", "Planning"] # Example inferred skills
            for sk in item['skills']:
                if sk in user_has:
                    st.write(f"✅ You already possess: {sk}")
                else:
                    st.markdown(f'<span class="skill-tag missing-skill">⚠️ Missing: {sk}</span>', unsafe_allow_html=True)
                    st.caption(f"Reason: {sk} is critical for technical precision in this career.")

    if st.button("Final Step: Find Colleges"):
        st.session_state.step = 5
        st.rerun()

# --- STEP 7: COLLEGE RECOMMENDATION (KERALA) ---
elif st.session_state.step == 5:
    st.header("🏫 Local College Recommendations (Kerala)")
    district = st.selectbox("Select your District:", list(COLLEGE_DB.keys()))
    
    recs = COLLEGE_DB.get(district, [])
    user_fields = [f['name'] for f in st.session_state.recommended_fields]
    
    found = False
    for col in recs:
        # Check if college offers courses in user's recommended fields
        match = any(field in col['fields'] for field in user_fields)
        if match:
            found = True
            st.markdown(f"""
            <div class="explanation-box" style="border-left-color: #2e7d32;">
                <h3>{col['name']} ({col['type']})</h3>
                <p><b>Suitability:</b> This is a top institution in {district} offering excellence in your recommended paths.</p>
            </div>
            """, unsafe_allow_html=True)
            
    if not found:
        st.warning("No direct match in this district. Consider exploring neighboring districts like Ernakulam or TVM for specialized institutes.")

    if st.button("Restart System"):
        st.session_state.step = 1
        st.rerun()
