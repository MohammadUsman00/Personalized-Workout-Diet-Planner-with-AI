import os
import io
import base64
from datetime import datetime
from typing import Dict, Tuple, List, Any
import re

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from fpdf import FPDF
import google.generativeai as genai

# Import our AI modules
from ai_services import AIOrchestrator, WorkoutAIService, NutritionAIService, AnalyticsAIService, AIChatService
from ai_dashboard import AIDashboard
from ui_components import AIUIComponents
from utils import calculate_bmi, calculate_bmr, calculate_tdee, validate_user_inputs
import config


def configure_page() -> None:
    st.set_page_config(
        page_title="AI-Powered Fitness Planner",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Futuristic AI styling
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');
        
        /* Global AI Theme */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 1400px;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
        }
        
        /* AI Header */
        .ai-main-header {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
            padding: 3rem 2rem;
            border-radius: 25px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            border: 2px solid #00d4ff;
        }
        
        .ai-main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,212,255,0.1), transparent);
            animation: ai-scan 4s infinite;
        }
        
        @keyframes ai-scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .ai-title {
            font-family: 'Orbitron', monospace;
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(45deg, #00d4ff, #00ff88, #ff6b6b, #ffd93d, #9d4edd);
            background-size: 500% 500%;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: ai-gradient-flow 6s ease-in-out infinite;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 0 0 40px rgba(0, 212, 255, 0.6);
            letter-spacing: 2px;
        }
        
        @keyframes ai-gradient-flow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .ai-subtitle {
            font-family: 'Exo 2', sans-serif;
            font-size: 1.3rem;
            color: #a0a0a0;
            text-align: center;
            font-weight: 300;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }
        
        .ai-badge {
            display: inline-block;
            background: linear-gradient(135deg, #00d4ff, #00ff88);
            color: #0f0f23;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 0.5rem;
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
        }
        
        /* AI Particles */
        .ai-particles {
            position: absolute;
            width: 6px;
            height: 6px;
            background: #00d4ff;
            border-radius: 50%;
            animation: ai-float 8s infinite ease-in-out;
            box-shadow: 0 0 10px #00d4ff;
        }
        
        .ai-particles:nth-child(1) { top: 15%; left: 10%; animation-delay: 0s; }
        .ai-particles:nth-child(2) { top: 25%; left: 85%; animation-delay: 2s; }
        .ai-particles:nth-child(3) { top: 60%; left: 15%; animation-delay: 4s; }
        .ai-particles:nth-child(4) { top: 70%; left: 80%; animation-delay: 6s; }
        
        @keyframes ai-float {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.6; }
            50% { transform: translateY(-30px) rotate(180deg); opacity: 1; }
        }
        
        /* Enhanced Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: #1e1e2e;
            border-radius: 15px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            color: #a0a0a0;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #00d4ff, #00ff88);
            color: #0f0f23;
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
        }
        
        /* Enhanced Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #00d4ff, #00ff88);
            color: #0f0f23;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
        }
        
        /* AI Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            border-right: 3px solid #00d4ff;
        }
        
        .stSidebar .stSelectbox > div > div {
            background: #1e1e2e;
            border: 2px solid #00d4ff;
            border-radius: 10px;
            color: #e0e0e0;
        }
        
        .stSidebar .stTextInput > div > div > input {
            background: #1e1e2e;
            border: 2px solid #00d4ff;
            border-radius: 10px;
            color: #e0e0e0;
            font-family: 'Exo 2', sans-serif;
        }
        
        .stSidebar .stButton > button {
            background: linear-gradient(135deg, #00d4ff, #00ff88);
            color: #0f0f23;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stSidebar .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 212, 255, 0.4);
        }
        
        /* AI Footer */
        .ai-footer {
            text-align: center;
            color: #a0a0a0;
            margin-top: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            border-radius: 20px;
            border: 1px solid #00d4ff;
            font-family: 'Exo 2', sans-serif;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .ai-title { font-size: 2rem; }
            .ai-subtitle { font-size: 1rem; }
        }
        </style>
        
        <div class="ai-main-header">
            <div class="ai-particles"></div>
            <div class="ai-particles"></div>
            <div class="ai-particles"></div>
            <div class="ai-particles"></div>
            <div class="ai-title">🤖 AI-POWERED FITNESS PLANNER</div>
            <div class="ai-subtitle">Advanced Artificial Intelligence for Personalized Health & Fitness</div>
            <div style="text-align: center; margin-top: 1rem;">
                <span class="ai-badge">🧠 AI-Powered</span>
                <span class="ai-badge">⚡ Real-time</span>
                <span class="ai-badge">🎯 Personalized</span>
                <span class="ai-badge">📊 Analytics</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    return api_key


def configure_gemini(api_key: str) -> None:
    genai.configure(api_key=api_key)


def build_prompt(user_inputs: Dict[str, str]) -> str:
    # Enhanced prompt with more detailed instructions
    return f"""
You are an expert fitness and nutrition coach with 15+ years of experience. Create a comprehensive, science-based 7-day plan for the following individual. Focus on sustainability, safety, and realistic progression.

CLIENT PROFILE:
- Name: {user_inputs['name']}
- Age: {user_inputs['age']} years
- Gender: {user_inputs['gender']}
- Height: {user_inputs['height_cm']} cm
- Weight: {user_inputs['weight_kg']} kg
- BMI: {user_inputs['bmi']} ({user_inputs['bmi_cat']})
- Primary Goal: {user_inputs['goal']}
- Cultural Food Preferences: {user_inputs['cultural_food']}
- Dietary Restrictions: {user_inputs['dietary_pref']}
- Available Equipment: {user_inputs['equipment']}
- Daily Time Commitment: {user_inputs['time_available']} minutes
- Budget Level: {user_inputs['budget']}

REQUIRED OUTPUT FORMAT:

1. WORKOUT PLAN (Day 1-7)
   For each day, provide:
   - Warm-up (5-10 minutes)
   - Main workout with specific exercises, sets, reps, and rest periods
   - Cool-down and stretching
   - Alternative exercises if equipment is limited
   - Estimated calories burned
   - Difficulty level (Beginner/Intermediate/Advanced)

2. NUTRITION PLAN (Day 1-7)
   For each day, provide:
   - Breakfast with portion sizes and calories
   - Lunch with portion sizes and calories
   - Dinner with portion sizes and calories
   - 1-2 healthy snacks with calories
   - Hydration goals (water intake)
   - Total daily calories and macronutrient breakdown
   - Shopping list for the week

3. PROGRESS TRACKING
   - Weekly milestones
   - Key metrics to monitor
   - Success indicators

4. MOTIVATION & TIPS
   - Daily motivational quote
   - 3 practical tips for success
   - Common challenges and solutions

5. SAFETY NOTES
   - Important safety considerations
   - When to consult a healthcare provider
   - Warning signs to watch for

Use clear, actionable language. Include specific measurements and timing. Make it practical and achievable for their lifestyle and constraints.
""".strip()


def call_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    # google-generativeai returns .text on the response
    return getattr(response, "text", "").strip()


def parse_sections(full_text: str) -> Tuple[str, str, str]:
    # Try to split by the required headings; fall back gracefully.
    lower = full_text.lower()
    workout_text = ""
    meal_text = ""
    motivation = ""

    # Identify indices for sections
    i_workout = lower.find("1. workout")
    i_meal = lower.find("2. meal")
    i_mot = lower.find("3. motivation")

    if i_workout != -1 and i_meal != -1:
        workout_text = full_text[i_workout:i_meal].strip()
    if i_meal != -1 and i_mot != -1:
        meal_text = full_text[i_meal:i_mot].strip()
    if i_mot != -1:
        motivation = full_text[i_mot:].strip()

    # Regex-based robust fallback extraction
    def extract_regex(pattern: str) -> str:
        match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        return match.group(1).strip() if match else ""

    if not workout_text or len(workout_text) < 120:
        workout_pattern = r"(?:^|\n)\s*1\s*[\).:-]?\s*[^\n]*workout[^\n]*\n(.*?)(?=\n\s*2\s*[\).:-]?\s*[^\n]*meal|\Z)"
        rx = extract_regex(workout_pattern)
        if rx:
            workout_text = f"Workout Plan\n{rx}"

    if not meal_text or len(meal_text) < 120:
        meal_pattern = r"(?:^|\n)\s*2\s*[\).:-]?\s*[^\n]*meal[^\n]*\n(.*?)(?=\n\s*3\s*[\).:-]?\s*[^\n]*motivation|\Z)"
        rx = extract_regex(meal_pattern)
        if rx:
            meal_text = f"Meal Plan\n{rx}"

    if not motivation:
        mot_pattern = r"(?:^|\n)\s*3\s*[\).:-]?\s*[^\n]*motivation[^\n]*\n(.*)$"
        rx = extract_regex(mot_pattern)
        if rx:
            motivation = rx

    # Final fallback split into thirds
    if not workout_text or not meal_text:
        parts = full_text.split("\n\n")
        if len(parts) >= 3:
            workout_text = workout_text or "\n\n".join(parts[: max(1, len(parts)//3)])
            meal_text = meal_text or "\n\n".join(parts[max(1, len(parts)//3): max(2, 2*len(parts)//3)])
            motivation = motivation or "\n\n".join(parts[max(2, 2*len(parts)//3):])
        else:
            workout_text = workout_text or full_text

    # Clean motivation: reduce to a single line if possible
    if motivation:
        lines = [l.strip("- • ") for l in motivation.splitlines() if l.strip()]
        last_line = lines[-1] if lines else motivation
        motivation = last_line

    return workout_text, meal_text, motivation


def ensure_section_text(section: str, displayed_text: str) -> str:
    # If the displayed text is too short, try re-extracting from full response
    txt = (displayed_text or "").strip()
    if len(txt) >= 200 or not st.session_state.get("full_response"):
        return txt
    full = st.session_state.get("full_response")
    if section == "workout":
        match = re.search(r"(?:^|\n)\s*1\s*[\).:-]?\s*[^\n]*workout[^\n]*\n(.*?)(?=\n\s*2\s*[\).:-]?\s*[^\n]*meal|\Z)", full, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        return (match.group(1).strip() if match else full)
    if section == "meal":
        match = re.search(r"(?:^|\n)\s*2\s*[\).:-]?\s*[^\n]*meal[^\n]*\n(.*?)(?=\n\s*3\s*[\).:-]?\s*[^\n]*motivation|\Z)", full, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        return (match.group(1).strip() if match else full)
    return txt


def _sanitize_for_pdf(text: str) -> str:
    # Replace common non-latin chars and bullets/em dashes; drop emojis
    replacements = {
        "•": "-",
        "–": "-",
        "—": "-",
        "●": "-",
        "✔": "*",
        "✦": "*",
        "✅": "*",
        "✗": "x",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Strip any characters unsupported by latin-1 used by default FPDF core fonts
    text_bytes = text.encode("latin-1", errors="ignore")
    return text_bytes.decode("latin-1", errors="ignore")


def generate_pdf_bytes(title: str, content: str) -> bytes:
    pdf = FPDF()
    # Set margins explicitly to avoid layout issues
    left_margin = 20
    right_margin = 20
    top_margin = 20
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    pdf.set_top_margin(top_margin)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Enhanced title with styling
    pdf.set_font("Arial", "B", 18)
    title_text = _sanitize_for_pdf(title)
    pdf.set_fill_color(102, 126, 234)  # Blue background
    pdf.set_text_color(255, 255, 255)  # White text
    pdf.cell(pdf.w - left_margin - right_margin, 12, txt=title_text, fill=True, align="C")
    pdf.ln(8)
    
    # Reset colors for body text
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)

    # Add generation date
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 6, txt=f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", align="R")
    pdf.ln(8)

    # Enhanced body formatting
    pdf.set_font("Arial", size=11)
    usable_width = pdf.w - left_margin - right_margin
    
    # Process content with better formatting
    lines = content.splitlines()
    for i, raw_line in enumerate(lines):
        text_line = _sanitize_for_pdf(raw_line)
        if not text_line.strip():
            pdf.ln(3)
            continue
            
        # Check if line is a header (starts with Day, contains numbers, or is all caps)
        if (text_line.startswith("Day") or 
            any(word.isupper() and len(word) > 3 for word in text_line.split()) or
            text_line.startswith("**") or text_line.startswith("##")):
            pdf.ln(4)
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(102, 126, 234)  # Blue color for headers
            pdf.multi_cell(usable_width, 7, txt=text_line.replace("*", "").replace("#", ""))
            pdf.set_font("Arial", size=11)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
        else:
            # Regular content
            if text_line.startswith("- ") or text_line.startswith("• "):
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(usable_width, 5, txt=text_line)
            else:
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(usable_width, 6, txt=text_line)

    # Add footer
    pdf.set_y(-20)
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 6, txt="Generated by AI-Powered Workout & Diet Planner", align="C")

    pdf_str = pdf.output(dest="S")
    if isinstance(pdf_str, (bytes, bytearray)):
        return bytes(pdf_str)
    return str(pdf_str).encode("latin1", errors="ignore")


def build_data_uri_pdf(pdf_bytes: bytes, filename: str) -> str:
    b64 = base64.b64encode(pdf_bytes).decode("ascii")
    # Use download attribute to hint filename
    return f"<a download=\"{filename}\" href=\"data:application/pdf;base64,{b64}\">⬇️ Alternate download link (click if normal download fails)</a>"


def compute_bmi(height_cm: float, weight_kg: float) -> Tuple[float, str]:
    if height_cm <= 0:
        return 0.0, "Invalid height"
    m = height_cm / 100.0
    bmi = weight_kg / (m * m)
    if bmi < 18.5:
        cat = "Underweight"
    elif bmi < 25:
        cat = "Normal"
    elif bmi < 30:
        cat = "Overweight"
    else:
        cat = "Obese"
    return round(bmi, 1), cat


def init_session_state() -> None:
    defaults = {
        "full_response": "",
        "workout_text": "",
        "diet_text": "",
        "motivation_text": "",
        "plans_df": None,
        "show_progress": False,
        "progress_data": [],
        "current_week": 1,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def create_progress_dashboard():
    """Create an interactive progress tracking dashboard"""
    st.markdown("### 📈 Progress Tracking Dashboard")
    
    # Create tabs for different tracking views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Weekly Overview", "🏋️ Workout Log", "🍽️ Nutrition Log", "📈 Analytics"])
    
    with tab1:
        st.markdown("#### Weekly Progress Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Week", f"Week {st.session_state.get('current_week', 1)}")
        with col2:
            st.metric("Workouts Completed", "0/7")
        with col3:
            st.metric("Average Daily Calories", "0")
        
        # Progress bars
        st.markdown("#### Progress Bars")
        st.markdown(
            """
            <div class="progress-container">
                <div class="progress-bar" style="width: 0%;"></div>
            </div>
            <p>Workout Completion: 0%</p>
            """,
            unsafe_allow_html=True
        )
    
    with tab2:
        st.markdown("#### Workout Log")
        st.info("Log your daily workouts here to track progress!")
        
        with st.form("workout_log"):
            date = st.date_input("Date")
            workout_type = st.selectbox("Workout Type", ["Cardio", "Strength", "Flexibility", "Mixed"])
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=300)
            intensity = st.select_slider("Intensity", options=["Low", "Medium", "High"])
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Log Workout"):
                st.success("Workout logged successfully!")
    
    with tab3:
        st.markdown("#### Nutrition Log")
        st.info("Track your daily nutrition intake!")
        
        with st.form("nutrition_log"):
            date = st.date_input("Date")
            calories = st.number_input("Calories Consumed", min_value=0, max_value=5000)
            protein = st.number_input("Protein (g)", min_value=0, max_value=500)
            carbs = st.number_input("Carbs (g)", min_value=0, max_value=1000)
            fat = st.number_input("Fat (g)", min_value=0, max_value=500)
            water = st.number_input("Water (glasses)", min_value=0, max_value=20)
            
            if st.form_submit_button("Log Nutrition"):
                st.success("Nutrition logged successfully!")
    
    with tab4:
        st.markdown("#### Analytics & Insights")
        st.info("View your progress trends and get insights!")
        
        # Placeholder for charts
        st.markdown("📊 **Progress Charts will appear here**")
        st.markdown("- Weight tracking over time")
        st.markdown("- Workout frequency trends")
        st.markdown("- Nutrition adherence")
        st.markdown("- Goal achievement rate")


def sidebar_form() -> Dict[str, str]:
    with st.sidebar:
        st.header("🎯 Your Profile")
        
        # Personal Information
        with st.expander("👤 Personal Details", expanded=True):
            name = st.text_input("Full Name", value="", placeholder="Enter your name")
            age = st.number_input("Age", min_value=10, max_value=90, value=22, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

            c1, c2 = st.columns(2)
            with c1:
                height_cm = st.number_input("Height (cm)", min_value=100, max_value=230, value=170, step=1)
            with c2:
                weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, step=1)

        # Fitness Goals
        with st.expander("🏋️ Fitness Goals", expanded=True):
            goal = st.selectbox("Primary Goal", [
                "Weight Loss", 
                "Muscle Gain", 
                "Maintain Fitness",
                "Improve Endurance",
                "Build Strength",
                "General Health"
            ])
            
            experience = st.selectbox("Fitness Experience", [
                "Beginner (0-6 months)",
                "Intermediate (6 months - 2 years)", 
                "Advanced (2+ years)"
            ])
            
            injuries = st.text_area("Any Injuries/Concerns", placeholder="List any injuries or health concerns...")

        # Nutrition Preferences
        with st.expander("🍽️ Nutrition Preferences", expanded=True):
            cultural_food = st.selectbox(
                "Cultural / Regional Food",
                ["Indian", "Mediterranean", "Continental", "East Asian", "Middle Eastern", "Latin American", "Other"],
            )
            dietary_pref = st.selectbox("Dietary Preference", [
                "Vegetarian", 
                "Non-Vegetarian", 
                "Vegan", 
                "Eggetarian",
                "Pescatarian",
                "Keto",
                "Paleo"
            ])
            
            allergies = st.text_area("Food Allergies", placeholder="List any food allergies...")
            dislikes = st.text_area("Food Dislikes", placeholder="Foods you don't like...")

        # Equipment & Schedule
        with st.expander("⚙️ Equipment & Schedule"):
            equipment = st.multiselect(
                "Available Equipment", 
                ["None", "Dumbbells", "Resistance Bands", "Gym Access", "Yoga Mat", "Pull-up Bar", "Kettlebell"],
                default=["None"]
            )
            time_available = st.slider("Daily Time Availability (minutes)", min_value=10, max_value=180, value=45, step=5)
            budget = st.selectbox("Budget Level", ["Low", "Moderate", "High"])
            
            workout_frequency = st.selectbox("Workout Frequency", [
                "3 days/week",
                "4 days/week", 
                "5 days/week",
                "6 days/week",
                "Daily"
            ])

        # BMI Calculator with enhanced display
        bmi, bmi_cat = compute_bmi(height_cm=height_cm, weight_kg=weight_kg)
        with st.expander("📊 Health Metrics"):
            st.metric("BMI", f"{bmi}", f"{bmi_cat}")
            
            # BMI color coding
            if bmi_cat == "Normal":
                st.success("✅ Healthy BMI range!")
            elif bmi_cat == "Underweight":
                st.warning("⚠️ Consider consulting a healthcare provider")
            elif bmi_cat == "Overweight":
                st.warning("⚠️ Focus on balanced nutrition and regular exercise")
            else:
                st.error("🚨 Please consult a healthcare provider before starting any fitness program")

        # Progress Tracking
        with st.expander("📈 Progress Tracking"):
            st.info("Track your progress weekly to stay motivated!")
            if st.button("📊 View Progress Dashboard"):
                st.session_state.show_progress = True

        generate = st.button("✨ Generate My Personalized Plan", use_container_width=True, type="primary")

    return {
        "name": name,
        "age": int(age),
        "gender": gender,
        "height_cm": int(height_cm),
        "weight_kg": int(weight_kg),
        "goal": goal,
        "experience": experience,
        "injuries": injuries,
        "cultural_food": cultural_food,
        "dietary_pref": dietary_pref,
        "allergies": allergies,
        "dislikes": dislikes,
        "equipment": ", ".join(equipment),
        "time_available": int(time_available),
        "budget": budget,
        "workout_frequency": workout_frequency,
        "generate": generate,
        "bmi": bmi,
        "bmi_cat": bmi_cat,
    }


def save_to_csv_if_requested(user_inputs: Dict[str, str]) -> None:
    with st.expander("Save Plan History"):
        if st.button("💾 Save this plan to CSV", use_container_width=True, disabled=not bool(st.session_state.get("full_response"))):
            row = {
                "timestamp": datetime.utcnow().isoformat(),
                "name": user_inputs["name"],
                "age": user_inputs["age"],
                "gender": user_inputs["gender"],
                "height_cm": user_inputs["height_cm"],
                "weight_kg": user_inputs["weight_kg"],
                "goal": user_inputs["goal"],
                "cultural_food": user_inputs["cultural_food"],
                "dietary_pref": user_inputs["dietary_pref"],
                "equipment": user_inputs["equipment"],
                "time_available": user_inputs["time_available"],
                "budget": user_inputs["budget"],
                "bmi": user_inputs["bmi"],
                "bmi_cat": user_inputs["bmi_cat"],
                "motivation": st.session_state.get("motivation_text", ""),
            }
            df_row = pd.DataFrame([row])
            csv_path = "plans_history.csv"
            if os.path.exists(csv_path):
                existing = pd.read_csv(csv_path)
                combined = pd.concat([existing, df_row], ignore_index=True)
            else:
                combined = df_row
            combined.to_csv(csv_path, index=False)
            st.success(f"Saved to {csv_path}")


def main() -> None:
    configure_page()
    init_session_state()

    # Initialize AI services
    api_key = load_api_key()
    if not api_key:
        st.error("🚨 GEMINI_API_KEY is missing. Please set it in your .env file.")
        st.stop()
    
    # Initialize AI orchestrator and components
    ai_orchestrator = AIOrchestrator(api_key)
    ai_dashboard = AIDashboard(ai_orchestrator)
    ui_components = AIUIComponents()
    
    # Apply AI sidebar styling
    ui_components.ai_sidebar_style()

    # Get user inputs with enhanced AI sidebar
    user_inputs = enhanced_sidebar_form(ui_components)

    # Display AI-powered profile summary
    display_ai_profile_summary(user_inputs, ui_components)

    # Main AI-powered interface
    if user_inputs["generate"]:
        generate_ai_plan(user_inputs, ai_orchestrator, ui_components)

    # Display AI dashboard
    if st.session_state.get("show_ai_dashboard", False):
        display_ai_dashboard(user_inputs, ai_dashboard, ui_components)

    # Display generated plans with AI features
    if st.session_state.get("ai_plan_generated", False):
        display_ai_plans(user_inputs, ai_orchestrator, ui_components)

    # AI Footer
    st.markdown("""
    <div class="ai-footer">
        <h3>🤖 Powered by Advanced AI</h3>
        <p>Made with ❤️ using Gemini Flash + Streamlit + Modular AI Architecture</p>
        <p>Transform your fitness journey with cutting-edge artificial intelligence!</p>
    </div>
    """, unsafe_allow_html=True)


def enhanced_sidebar_form(ui_components: AIUIComponents) -> Dict[str, Any]:
    """Enhanced sidebar with AI-powered styling"""
    with st.sidebar:
        ui_components.ai_header("🎯 AI Profile", "Configure your AI-powered fitness profile")
        
        # Personal Information
        with st.expander("👤 Personal Details", expanded=True):
            name = st.text_input("Full Name", value="", placeholder="Enter your name")
            age = st.number_input("Age", min_value=10, max_value=90, value=22, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

            c1, c2 = st.columns(2)
            with c1:
                height_cm = st.number_input("Height (cm)", min_value=100, max_value=230, value=170, step=1)
            with c2:
                weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, step=1)

        # AI-Enhanced Fitness Goals
        with st.expander("🏋️ AI Fitness Goals", expanded=True):
            goal = st.selectbox("Primary Goal", config.FITNESS_GOALS)
            experience = st.selectbox("Fitness Experience", config.EXPERIENCE_LEVELS)
            injuries = st.text_area("Injuries/Concerns", placeholder="List any injuries or health concerns...")

        # AI Nutrition Preferences
        with st.expander("🍽️ AI Nutrition", expanded=True):
            cultural_food = st.selectbox("Cultural Food", config.CULTURAL_FOOD_TYPES)
            dietary_pref = st.selectbox("Dietary Preference", config.DIETARY_PREFERENCES)
            allergies = st.text_area("Food Allergies", placeholder="List any food allergies...")
            dislikes = st.text_area("Food Dislikes", placeholder="Foods you don't like...")

        # AI Equipment & Schedule
        with st.expander("⚙️ AI Equipment & Schedule"):
            equipment = st.multiselect("Available Equipment", config.EQUIPMENT_OPTIONS, default=["None"])
            time_available = st.slider("Daily Time (minutes)", min_value=10, max_value=180, value=45, step=5)
            budget = st.selectbox("Budget Level", config.BUDGET_LEVELS)
            workout_frequency = st.selectbox("Workout Frequency", config.WORKOUT_FREQUENCY)

        # AI Health Metrics
        bmi, bmi_cat = calculate_bmi(height_cm=height_cm, weight_kg=weight_kg)
        with st.expander("📊 AI Health Metrics"):
            ui_components.ai_metric_card("BMI", f"{bmi}", f"{bmi_cat}", "📏")
            
            # BMI color coding
            if bmi_cat == "Normal":
                st.success("✅ AI Analysis: Healthy BMI range!")
            elif bmi_cat == "Underweight":
                st.warning("⚠️ AI Recommendation: Consider consulting a healthcare provider")
            elif bmi_cat == "Overweight":
                st.warning("⚠️ AI Suggestion: Focus on balanced nutrition and regular exercise")
            else:
                st.error("🚨 AI Alert: Please consult a healthcare provider before starting any fitness program")

        # AI Dashboard Access
        with st.expander("🧠 AI Dashboard"):
            st.info("Access advanced AI analytics and insights!")
            if st.button("📊 Open AI Dashboard", use_container_width=True):
                st.session_state.show_ai_dashboard = True
                st.rerun()

        # Generate AI Plan
        generate = st.button("🤖 Generate AI-Powered Plan", use_container_width=True, type="primary")

    return {
        "name": name,
        "age": int(age),
        "gender": gender,
        "height_cm": int(height_cm),
        "weight_kg": int(weight_kg),
        "goal": goal,
        "experience": experience,
        "injuries": injuries,
        "cultural_food": cultural_food,
        "dietary_pref": dietary_pref,
        "allergies": allergies,
        "dislikes": dislikes,
        "equipment": ", ".join(equipment),
        "time_available": int(time_available),
        "budget": budget,
        "workout_frequency": workout_frequency,
        "generate": generate,
        "bmi": bmi,
        "bmi_cat": bmi_cat,
    }


def display_ai_profile_summary(user_inputs: Dict, ui_components: AIUIComponents):
    """Display AI-powered profile summary"""
    st.markdown("### 🤖 AI Profile Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ui_components.ai_metric_card(
            "🎯 Goal",
            user_inputs["goal"],
            "AI Optimized",
            "🎯"
        )
    
    with col2:
        ui_components.ai_metric_card(
            "⏱️ Time",
            f"{user_inputs['time_available']} min",
            "AI Scheduled",
            "⏱️"
        )
    
    with col3:
        ui_components.ai_metric_card(
            "💰 Budget",
            user_inputs["budget"],
            "AI Optimized",
            "💰"
        )
    
    with col4:
        bmi_color = "#00ff88" if user_inputs["bmi_cat"] == "Normal" else "#ffd93d" if user_inputs["bmi_cat"] == "Overweight" else "#ff6b6b"
        ui_components.ai_metric_card(
            "📏 BMI",
            f"{user_inputs['bmi']}",
            f"{user_inputs['bmi_cat']}",
            "📏"
        )


def generate_ai_plan(user_inputs: Dict, ai_orchestrator: AIOrchestrator, ui_components: AIUIComponents):
    """Generate AI-powered comprehensive plan"""
    with st.spinner("🤖 AI is analyzing your profile and generating personalized plans..."):
        ui_components.ai_loading_spinner("AI is thinking...")
        
        try:
            # Generate comprehensive AI plan
            ai_plan = ai_orchestrator.generate_comprehensive_plan(user_inputs)
            
            # Store in session state
            st.session_state.ai_plan = ai_plan
            st.session_state.ai_plan_generated = True
            st.session_state.user_profile = user_inputs
            
            st.success("🎉 AI has generated your personalized plan!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ AI generation failed: {str(e)}")


def display_ai_dashboard(user_inputs: Dict, ai_dashboard: AIDashboard, ui_components: AIUIComponents):
    """Display AI dashboard"""
    ai_dashboard.render_ai_overview(user_inputs, [])
    
    if st.button("← Back to Main"):
        st.session_state.show_ai_dashboard = False
        st.rerun()


def display_ai_plans(user_inputs: Dict, ai_orchestrator: AIOrchestrator, ui_components: AIUIComponents):
    """Display AI-generated plans with advanced features"""
    ai_plan = st.session_state.get("ai_plan", {})
    
    # Enhanced tabs with AI features
    tabs = st.tabs([
        "🤖 AI Workout Plan", 
        "🍽️ AI Nutrition Plan", 
        "📊 AI Analytics", 
        "💬 AI Coach Chat",
        "📋 AI Summary"
    ])
    
    with tabs[0]:
        ui_components.ai_header("🏋️ AI-Powered Workout Plan", "Scientifically optimized by advanced AI")
        
        workout_plan = ai_plan.get("workout_plan", {})
        if workout_plan:
            st.json(workout_plan)  # Display structured workout plan
        else:
            st.info("🤖 AI is preparing your workout plan...")
    
    with tabs[1]:
        ui_components.ai_header("🍽️ AI-Powered Nutrition Plan", "Metabolically optimized by advanced AI")
        
        nutrition_plan = ai_plan.get("nutrition_plan", {})
        if nutrition_plan:
            st.json(nutrition_plan)  # Display structured nutrition plan
        else:
            st.info("🤖 AI is preparing your nutrition plan...")
    
    with tabs[2]:
        ai_dashboard = AIDashboard(ai_orchestrator)
        ai_dashboard.render_ai_overview(user_inputs, [])
    
    with tabs[3]:
        ai_dashboard = AIDashboard(ai_orchestrator)
        ai_dashboard.render_ai_chat(user_inputs)
    
    with tabs[4]:
        ui_components.ai_header("📋 AI Plan Summary", "Comprehensive overview of your AI-generated plan")
        
        # Display AI insights
        insights = ai_plan.get("ai_insights", [])
        for insight in insights:
            ui_components.ai_insight_card({
                "title": insight.title,
                "description": insight.description,
                "confidence": insight.confidence,
                "priority": insight.priority
            })
        
        # Display recommendations
        recommendations = ai_plan.get("recommendations", [])
        st.markdown("#### 🎯 AI Recommendations")
        for i, rec in enumerate(recommendations[:3], 1):
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
                border-left: 4px solid #00d4ff;
                border-radius: 10px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            ">
                <h4 style="color: #00d4ff; margin-bottom: 0.5rem;">{i}. {rec.get('title', 'AI Recommendation')}</h4>
                <p style="color: #e0e0e0; margin: 0;">{rec.get('description', 'No description available.')}</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


