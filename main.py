import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# --- CONFIG ---
st.set_page_config(page_title="Explainable AI Career Guide", layout="wide")

# --- DATA REPOSITORY (PLACEHOLDERS) ---
# Replace these with your actual database of 20 questions, careers, and colleges.
DISTRICTS = ["Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"]

# Career Data Structure
CAREER_DATABASE = {
    "Technology": {
        "Courses": ["B.Tech Computer Science", "BCA", "B.Tech AI & Data Science"],
        "Careers": ["Software Engineer", "Data Scientist", "Cybersecurity Analyst"],
        "Required_Skills": {"Logic": 90, "Coding": 85, "Math": 80, "Creative": 50, "Communication": 60}
    },
    "Healthcare": {
        "Courses": ["MBBS", "B.Sc Nursing", "B.Pharm"],
        "Careers": ["Doctor", "Clinical Researcher", "Pharmacist"],
        "Required_Skills": {"Logic": 70, "Biology": 95, "Empathy": 90, "Memory": 85, "Communication": 80}
    },
    # Add more fields like Commerce, Design, Humanities here...
}

COLLEGE_DB = {
    "Ernakulam": ["Model Engineering College", "CUSAT", "Maharajas College"],
    "Thiruvananthapuram": ["College of Engineering (CET)", "Govt. Barton Hill", "University College"],
    # Populate all 14 districts here...
}

# --- HELPER FUNCTIONS ---
def generate_radar_chart(student_skills, required_skills, career_name):
    categories = list(required_skills.keys())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[student_skills.get(s, 0) for s in categories],
        theta=categories, fill='toself', name='Your Skills'
    ))
    fig.add_trace(go.Scatterpolar(
        r=list(required_skills.values()),
        theta=categories, fill='toself', name=f'{career_name} Requirements'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, title="Skill Gap Visualization")
    return fig

# --- APP LOGIC & STATE ---
if 'step' not in st.session_state: st.session_state.step = "registration"
if 'scores' not in st.session_state: st.session_state.scores = {"Logic": 0, "Creative": 0, "Communication": 0, "Analytical": 0, "Biology": 0}
if 'test_idx' not in st.session_state: st.session_state.test_idx = 0

# --- STEP 1: REGISTRATION ---
if st.session_state.step == "registration":
    st.title("🎓 Student Profile Registration")
    with st.form("reg_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            age = st.number_input("Age", 15, 30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            email = st.text_input("Email")
            stream = st.selectbox("Plus Two Stream", ["Science (Bio)", "Science (CS)", "Commerce", "Humanities"])
            passed = st.radio("Passed Plus Two?", ["Yes", "No"])
        
        aware = st.radio("Are you aware of your skills and career interests?", ["Yes", "No"])
        
        if st.form_submit_button("Proceed"):
            st.session_state.user_data = {"name": name, "stream": stream, "aware": aware}
            st.session_state.step = "branching"
            st.rerun()

# --- STEP 2: BRANCHING (AWARE VS UNAWARE) ---
elif st.session_state.step == "branching":
    st.header(f"Welcome, {st.session_state.user_data['name']}")
    if st.session_state.user_data['aware'] == "Yes":
        st.info("Since you know your skills, please select your primary interest field.")
        field = st.selectbox("Select Field", list(CAREER_DATABASE.keys()))
        if st.button("See Courses"):
            st.session_state.field = field
            st.session_state.step = "course_recommendation"
            st.rerun()
    else:
        st.warning("You seem unsure. Let's start with an Aptitude Test to find your best field.")
        if st.button("Attend 20-Question Aptitude Test"):
            st.session_state.step = "field_aptitude_test"
            st.rerun()

# --- STEP 3: APTITUDE TEST (UNAWRE PATH) ---
elif st.session_state.step == "field_aptitude_test":
    st.subheader("Aptitude Test: Level 1 (Field Selection)")
    # (Simplified for Demo: You should put your 20 questions in a list)
    questions = [
        {"q": "How do you solve a complex puzzle?", "o": ["Logical steps", "Creative trial", "Ask for help"], "s": "Logic"},
        {"q": "Do you enjoy learning about human anatomy?", "o": ["Yes, very much", "No", "Maybe"], "s": "Biology"}
    ]
    
    q = questions[st.session_state.test_idx]
    ans = st.radio(q['q'], q['o'])
    
    if st.button("Next Question"):
        if ans == q['o'][0]: st.session_state.scores[q['s']] += 50 # Example scoring
        st.session_state.test_idx += 1
        if st.session_state.test_idx >= len(questions):
            st.session_state.step = "recommend_fields"
        st.rerun()

# --- STEP 4: FIELD RECOMMENDATION (XAI) ---
elif st.session_state.step == "recommend_fields":
    st.header("🔍 Field Recommendations")
    # Rule-based logic
    top_field = "Technology" if st.session_state.scores["Logic"] > st.session_state.scores["Biology"] else "Healthcare"
    st.success(f"We recommend: **{top_field}**")
    st.write(f"**Explainability:** Your logic score was {st.session_state.scores['Logic']}. This field requires structured thinking.")
    
    if st.button(f"Proceed to {top_field} Courses"):
        st.session_state.field = top_field
        st.session_state.step = "course_recommendation"
        st.rerun()

# --- STEP 5: SKILL GAP & GRAPH ---
elif st.session_state.step == "skill_gap":
    st.header("📊 Skill Gap Analysis")
    career = st.session_state.career
    req = CAREER_DATABASE[st.session_state.field]["Required_Skills"]
    
    # In 'Aware' path, user ticks skills they have
    if st.session_state.user_data['aware'] == "Yes":
        st.write("Tick the skills you already possess:")
        user_ticks = {}
        for skill in req.keys():
            user_ticks[skill] = 100 if st.checkbox(skill) else 20
        student_scores = user_ticks
    else:
        # In 'Unaware' path, use test scores
        student_scores = {s: random.randint(30, 90) for s in req.keys()}

    # Show Graph
    
    fig = generate_radar_chart(student_scores, req, career)
    st.plotly_chart(fig)
    
    # Explanation
    for skill, req_val in req.items():
        if student_scores[skill] < req_val:
            st.error(f"Gap in **{skill}**: You need {req_val}% but have {student_scores[skill]}%. Reason: Crucial for {career} success.")

    if st.button("Find Colleges in Kerala"):
        st.session_state.step = "colleges"
        st.rerun()

# --- STEP 6: DISTRICT & COLLEGES ---
elif st.session_state.step == "colleges":
    st.header("📍 Kerala College Recommendation")
    district = st.selectbox("Select your District", DISTRICTS)
    colleges = COLLEGE_DB.get(district, ["Govt. College " + district, "District Aided College"])
    
    st.subheader(f"Top Recommendations in {district}:")
    for c in colleges:
        st.info(f"🏫 **{c}** - Recommended because it offers your selected course and has high accreditation.")
        
    if st.button("Start New Session"):
        st.session_state.clear()
        st.rerun()

# Add missing intermediate steps (Course Selection, Career Selection) with similar logic...
elif st.session_state.step == "course_recommendation":
    st.header("Select a Course")
    courses = CAREER_DATABASE[st.session_state.field]["Courses"]
    sel_course = st.selectbox("Recommended Courses:", courses)
    if st.button("Recommend Careers"):
        st.session_state.course = sel_course
        st.session_state.step = "career_recommendation"
        st.rerun()

elif st.session_state.step == "career_recommendation":
    st.header("Career Path")
    careers = CAREER_DATABASE[st.session_state.field]["Careers"]
    sel_career = st.selectbox("Based on your course, here are the best careers:", careers)
    if st.button("Perform Skill Gap Analysis"):
        st.session_state.career = sel_career
        st.session_state.step = "skill_gap"
        st.rerun()
