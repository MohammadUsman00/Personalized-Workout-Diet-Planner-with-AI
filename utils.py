"""
Utility functions for the AI-Powered Workout & Diet Planner
"""

import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import pandas as pd


def calculate_bmi(height_cm: float, weight_kg: float) -> Tuple[float, str]:
    """
    Calculate BMI and return category
    
    Args:
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
        
    Returns:
        Tuple of (BMI value, BMI category)
    """
    if height_cm <= 0:
        return 0.0, "Invalid height"
    
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m * height_m)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return round(bmi, 1), category


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters  
        age: Age in years
        gender: Gender (Male/Female/Other)
        
    Returns:
        BMR in calories per day
    """
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:  # Female or Other
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    return round(bmr, 0)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculate Total Daily Energy Expenditure
    
    Args:
        bmr: Basal Metabolic Rate
        activity_level: Activity level (Sedentary, Light, Moderate, Active, Very Active)
        
    Returns:
        TDEE in calories per day
    """
    activity_multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375, 
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.2)
    return round(bmr * multiplier, 0)


def calculate_calorie_goals(tdee: float, goal: str) -> Dict[str, int]:
    """
    Calculate calorie goals based on fitness objective
    
    Args:
        tdee: Total Daily Energy Expenditure
        goal: Fitness goal (Weight Loss, Muscle Gain, etc.)
        
    Returns:
        Dictionary with calorie goals
    """
    if goal == "Weight Loss":
        return {
            "daily_calories": int(tdee - 500),  # 500 calorie deficit
            "deficit": 500
        }
    elif goal == "Muscle Gain":
        return {
            "daily_calories": int(tdee + 300),  # 300 calorie surplus
            "surplus": 300
        }
    else:  # Maintain Fitness
        return {
            "daily_calories": int(tdee),
            "deficit": 0,
            "surplus": 0
        }


def parse_workout_duration(duration_str: str) -> int:
    """
    Parse workout duration string to minutes
    
    Args:
        duration_str: Duration string (e.g., "45 minutes", "1 hour", "1h 30m")
        
    Returns:
        Duration in minutes
    """
    duration_str = duration_str.lower().strip()
    
    # Extract numbers and units
    numbers = re.findall(r'\d+', duration_str)
    if not numbers:
        return 0
    
    total_minutes = 0
    
    if 'hour' in duration_str or 'h' in duration_str:
        hours = int(numbers[0]) if numbers else 0
        total_minutes += hours * 60
        
        # Check for additional minutes
        if len(numbers) > 1:
            minutes = int(numbers[1])
            total_minutes += minutes
    else:
        # Assume minutes
        total_minutes = int(numbers[0])
    
    return total_minutes


def extract_exercises_from_text(text: str) -> List[Dict[str, str]]:
    """
    Extract exercise information from workout text
    
    Args:
        text: Workout plan text
        
    Returns:
        List of exercise dictionaries
    """
    exercises = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('*'):
            continue
            
        # Look for exercise patterns
        if any(keyword in line.lower() for keyword in ['push-up', 'squat', 'lunge', 'plank', 'burpee']):
            exercise = {
                'name': line.split('-')[0].strip() if '-' in line else line,
                'description': line,
                'sets': extract_sets_reps(line),
                'reps': extract_sets_reps(line, 'reps')
            }
            exercises.append(exercise)
    
    return exercises


def extract_sets_reps(text: str, target: str = 'sets') -> Optional[int]:
    """
    Extract sets or reps from exercise text
    
    Args:
        text: Exercise description
        target: 'sets' or 'reps'
        
    Returns:
        Number of sets or reps
    """
    if target == 'sets':
        pattern = r'(\d+)\s*sets?'
    else:
        pattern = r'(\d+)\s*reps?'
    
    match = re.search(pattern, text.lower())
    return int(match.group(1)) if match else None


def generate_weekly_schedule(workout_frequency: str, available_days: List[str] = None) -> List[str]:
    """
    Generate weekly workout schedule
    
    Args:
        workout_frequency: How many days per week
        available_days: Available days of the week
        
    Returns:
        List of scheduled workout days
    """
    if available_days is None:
        available_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    frequency_map = {
        "3 days/week": 3,
        "4 days/week": 4,
        "5 days/week": 5,
        "6 days/week": 6,
        "Daily": 7
    }
    
    num_days = frequency_map.get(workout_frequency, 3)
    
    # Simple scheduling - distribute evenly
    if num_days <= len(available_days):
        return available_days[:num_days]
    else:
        return available_days


def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to human-readable string
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted duration string
    """
    if minutes < 60:
        return f"{minutes} minutes"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours}h {remaining_minutes}m"


def validate_user_inputs(user_inputs: Dict) -> Tuple[bool, List[str]]:
    """
    Validate user input data
    
    Args:
        user_inputs: Dictionary of user inputs
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    required_fields = ['name', 'age', 'height_cm', 'weight_kg', 'goal']
    for field in required_fields:
        if not user_inputs.get(field):
            errors.append(f"{field} is required")
    
    # Validate age
    if user_inputs.get('age', 0) < 10 or user_inputs.get('age', 0) > 90:
        errors.append("Age must be between 10 and 90")
    
    # Validate height
    if user_inputs.get('height_cm', 0) < 100 or user_inputs.get('height_cm', 0) > 230:
        errors.append("Height must be between 100cm and 230cm")
    
    # Validate weight
    if user_inputs.get('weight_kg', 0) < 30 or user_inputs.get('weight_kg', 0) > 200:
        errors.append("Weight must be between 30kg and 200kg")
    
    return len(errors) == 0, errors


def create_progress_summary(progress_data: List[Dict]) -> Dict[str, float]:
    """
    Create progress summary from tracking data
    
    Args:
        progress_data: List of progress tracking entries
        
    Returns:
        Summary statistics
    """
    if not progress_data:
        return {}
    
    df = pd.DataFrame(progress_data)
    
    summary = {}
    
    # Calculate averages for numeric columns
    numeric_columns = ['weight', 'calories_burned', 'calories_consumed', 'water_intake', 'sleep_hours']
    for col in numeric_columns:
        if col in df.columns:
            summary[f'avg_{col}'] = df[col].mean()
    
    # Calculate completion rates
    if 'workouts_completed' in df.columns:
        summary['workout_completion_rate'] = df['workouts_completed'].mean()
    
    return summary
