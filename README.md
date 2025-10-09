# 🧘‍♀️ AI-Powered Personalized Workout & Diet Planner

Create tailored 7-day workout and meal plans using Google Gemini Flash and Streamlit.

## ✨ Features
- Sidebar form for student profile and preferences
- Gemini Flash generated 7-day workout and meal plans
- Clean tabbed display for Workout and Diet
- PDF download for each plan
- Motivation of the Day
- BMI calculator and optional CSV history

## 📦 Tech Stack
- Frontend: Streamlit
- Backend: Python
- AI: Google Gemini Flash (via google-generativeai)
- Env: python-dotenv

## 📁 Folder Structure
```
ai_fitness_planner/
├── app.py
├── .env
├── requirements.txt
└── README.md
```

## 🔑 Environment
Create a `.env` next to `app.py` with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📝 Notes
- The app expects `GEMINI_API_KEY` to be present via `.env`.
- Plans can be saved to `plans_history.csv` from within the UI.

## ❤️ Footer
Made with ❤️ using Gemini Flash + Streamlit


