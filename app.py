import os
import io
import base64
from datetime import datetime
from typing import Dict, Tuple
import re

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from fpdf import FPDF
import google.generativeai as genai


def configure_page() -> None:
    st.set_page_config(
        page_title="AI-Powered Personalized Workout & Diet Planner",
        page_icon="🧘‍♀️",
        layout="centered",
    )

    # Animated gradient header
    st.markdown(
        """
        <style>
        .gradient-text {
            font-size: 2.0rem;
            font-weight: 800;
            background: linear-gradient(90deg, #7F7CFF, #00C2FF, #00E6A8, #FFC371);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: flow 6s ease-in-out infinite;
            background-size: 300% 300%;
        }
        @keyframes flow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .subtext { color: #5b5b5b; }
        .footer { text-align: center; color: #888; margin-top: 2rem; }
        </style>
        <div style="text-align:center; margin-bottom: 0.75rem;">
          <div class="gradient-text">🧘‍♀️ AI-Powered Personalized Workout & Diet Planner</div>
          <div class="subtext">Create tailored 7-day workout and meal plans using Gemini Flash</div>
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
    return f"""
You are a professional, empathetic fitness and diet coach. Create a practical, budget-friendly, culturally-aware 7-day plan for the following student. Use clear day-wise formatting, bullets, and concise explanations.

Student Profile:
- Name: {user_inputs['name']}
- Age: {user_inputs['age']} years
- Gender: {user_inputs['gender']}
- Height: {user_inputs['height_cm']} cm
- Weight: {user_inputs['weight_kg']} kg
- Fitness Goal: {user_inputs['goal']}
- Cultural / Regional Food Type: {user_inputs['cultural_food']}
- Dietary Preference: {user_inputs['dietary_pref']}
- Available Equipment: {user_inputs['equipment']}
- Daily Time Availability: {user_inputs['time_available']} minutes
- Budget: {user_inputs['budget']}

Output strictly structured as:
1. Workout Plan (Day-wise: Day 1..Day 7). For each day include: warm-up, main sets (with sets/reps or time), cool-down, and easy alternatives if short on time.
2. Meal Plan (Day-wise: Day 1..Day 7). For each day include: breakfast, lunch, dinner, and 1 snack. Respect cultural + dietary preferences and budget.
3. Motivation Quote (one short, uplifting line)

Keep the tone friendly and human. Avoid markdown tables; prefer bullet points.
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
    left_margin = 15
    right_margin = 15
    top_margin = 15
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    pdf.set_top_margin(top_margin)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    title_text = _sanitize_for_pdf(title)
    pdf.multi_cell(pdf.w - left_margin - right_margin, 8, txt=title_text)
    pdf.ln(2)

    # Body
    pdf.set_font("Arial", size=11)
    usable_width = pdf.w - left_margin - right_margin
    for raw_line in content.splitlines():
        text_line = _sanitize_for_pdf(raw_line)
        if not text_line.strip():
            text_line = " "
        pdf.multi_cell(usable_width, 6, txt=text_line)

    pdf_str = pdf.output(dest="S")  # may return str, bytes, or bytearray depending on fpdf version
    if isinstance(pdf_str, (bytes, bytearray)):
        return bytes(pdf_str)
    # Fallback for string output
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
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def sidebar_form() -> Dict[str, str]:
    with st.sidebar:
        st.header("Your Details")

        name = st.text_input("Name", value="")
        age = st.number_input("Age", min_value=10, max_value=90, value=22, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        c1, c2 = st.columns(2)
        with c1:
            height_cm = st.number_input("Height (cm)", min_value=100, max_value=230, value=170, step=1)
        with c2:
            weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, step=1)

        goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintain Fitness"])
        cultural_food = st.selectbox(
            "Cultural / Regional Food",
            ["Indian", "Mediterranean", "Continental", "East Asian", "Middle Eastern", "Latin American", "Other"],
        )
        dietary_pref = st.selectbox("Dietary Preference", ["Veg", "Non-Veg", "Vegan", "Eggetarian"]) 
        equipment = st.selectbox("Available Equipment", ["None", "Dumbbells", "Resistance Bands", "Gym Access"])
        time_available = st.slider("Daily Time Availability (minutes)", min_value=10, max_value=180, value=45, step=5)
        budget = st.selectbox("Budget", ["Low", "Moderate", "High"])

        # BMI quick view
        bmi, bmi_cat = compute_bmi(height_cm=height_cm, weight_kg=weight_kg)
        with st.expander("BMI Calculator"):
            st.write(f"BMI: **{bmi}** ({bmi_cat})")

        generate = st.button("✨ Generate My Plan", use_container_width=True, type="primary")

    return {
        "name": name,
        "age": int(age),
        "gender": gender,
        "height_cm": int(height_cm),
        "weight_kg": int(weight_kg),
        "goal": goal,
        "cultural_food": cultural_food,
        "dietary_pref": dietary_pref,
        "equipment": equipment,
        "time_available": int(time_available),
        "budget": budget,
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

    api_key = load_api_key()
    if not api_key:
        st.error("GEMINI_API_KEY is missing. Please set it in your .env file.")
    else:
        configure_gemini(api_key)

    user_inputs = sidebar_form()

    # Summary chips
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Goal", user_inputs["goal"]) 
    col2.metric("Time (min)", user_inputs["time_available"]) 
    col3.metric("Budget", user_inputs["budget"]) 
    col4.metric("BMI", f"{user_inputs['bmi']} ({user_inputs['bmi_cat']})")

    if user_inputs["generate"]:
        if not api_key:
            st.stop()
        prompt = build_prompt(user_inputs)
        with st.spinner("Generating your personalized 7-day plans with Gemini Flash..."):
            try:
                full = call_gemini(prompt)
                st.session_state.full_response = full
                workout, diet, motivation = parse_sections(full)
                st.session_state.workout_text = workout
                st.session_state.diet_text = diet
                st.session_state.motivation_text = motivation
            except Exception as e:
                st.error(f"Failed to generate plans: {e}")

    if st.session_state.workout_text or st.session_state.diet_text:
        tabs = st.tabs(["🏋️ Workout Plan", "🍽️ Diet Plan"])
        with tabs[0]:
            st.subheader("Your 7-Day Workout Plan")
            workout_text = ensure_section_text("workout", st.session_state.workout_text)
            st.write(workout_text)
            pdf_bytes = generate_pdf_bytes("Workout Plan", workout_text)
            st.download_button(
                "⬇️ Download Workout Plan (PDF)",
                data=io.BytesIO(pdf_bytes),
                file_name="workout_plan.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
            st.markdown(build_data_uri_pdf(pdf_bytes, "workout_plan.pdf"), unsafe_allow_html=True)
        with tabs[1]:
            st.subheader("Your 7-Day Meal Plan")
            meal_text = ensure_section_text("meal", st.session_state.diet_text)
            st.write(meal_text)
            pdf_bytes = generate_pdf_bytes("Meal Plan", meal_text)
            st.download_button(
                "⬇️ Download Meal Plan (PDF)",
                data=io.BytesIO(pdf_bytes),
                file_name="meal_plan.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
            st.markdown(build_data_uri_pdf(pdf_bytes, "meal_plan.pdf"), unsafe_allow_html=True)

        # Motivation of the day
        if st.session_state.motivation_text:
            st.markdown("---")
            st.markdown(f"### 💡 Motivation of the Day")
            st.info(st.session_state.motivation_text)

        save_to_csv_if_requested(user_inputs)

    st.markdown("---")
    st.markdown("<div class='footer'>Made with ❤️ using Gemini Flash + Streamlit</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()


