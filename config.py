"""
Configuration settings for the AI-Powered Workout & Diet Planner
"""

# App Configuration
APP_NAME = "AI-Powered Personalized Workout & Diet Planner"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Create tailored 7-day workout and meal plans using advanced AI"

# UI Configuration
PAGE_ICON = "🧘‍♀️"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# AI Model Configuration
GEMINI_MODEL = "gemini-2.0-flash"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# Plan Configuration
DEFAULT_PLAN_DURATION = 7  # days
MAX_PLAN_DURATION = 30
MIN_TIME_AVAILABLE = 10  # minutes
MAX_TIME_AVAILABLE = 180  # minutes

# BMI Categories
BMI_CATEGORIES = {
    "Underweight": {"min": 0, "max": 18.5, "color": "#3b82f6"},
    "Normal": {"min": 18.5, "max": 25, "color": "#10b981"},
    "Overweight": {"min": 25, "max": 30, "color": "#f59e0b"},
    "Obese": {"min": 30, "max": 100, "color": "#ef4444"}
}

# Fitness Goals
FITNESS_GOALS = [
    "Weight Loss",
    "Muscle Gain", 
    "Maintain Fitness",
    "Improve Endurance",
    "Build Strength",
    "General Health"
]

# Dietary Preferences
DIETARY_PREFERENCES = [
    "Vegetarian",
    "Non-Vegetarian", 
    "Vegan",
    "Eggetarian",
    "Pescatarian",
    "Keto",
    "Paleo"
]

# Cultural Food Types
CULTURAL_FOOD_TYPES = [
    "Indian",
    "Mediterranean", 
    "Continental",
    "East Asian",
    "Middle Eastern",
    "Latin American",
    "Other"
]

# Equipment Options
EQUIPMENT_OPTIONS = [
    "None",
    "Dumbbells",
    "Resistance Bands", 
    "Gym Access",
    "Yoga Mat",
    "Pull-up Bar",
    "Kettlebell"
]

# Workout Frequency Options
WORKOUT_FREQUENCY = [
    "3 days/week",
    "4 days/week",
    "5 days/week", 
    "6 days/week",
    "Daily"
]

# Budget Levels
BUDGET_LEVELS = ["Low", "Moderate", "High"]

# Experience Levels
EXPERIENCE_LEVELS = [
    "Beginner (0-6 months)",
    "Intermediate (6 months - 2 years)",
    "Advanced (2+ years)"
]

# Progress Tracking Configuration
TRACKING_METRICS = [
    "weight",
    "workouts_completed", 
    "calories_burned",
    "calories_consumed",
    "water_intake",
    "sleep_hours",
    "mood_rating"
]

# PDF Configuration
PDF_MARGINS = {
    "left": 20,
    "right": 20, 
    "top": 20,
    "bottom": 20
}

PDF_FONTS = {
    "title": ("Arial", "B", 18),
    "header": ("Arial", "B", 12),
    "body": ("Arial", "", 11),
    "small": ("Arial", "", 10)
}

# Color Scheme
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2", 
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6"
}
