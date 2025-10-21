"""
Basic tests for the AI-Powered Workout & Diet Planner
"""

import unittest
from utils import calculate_bmi, calculate_bmr, calculate_tdee, validate_user_inputs


class TestWorkoutPlanner(unittest.TestCase):
    """Test cases for the workout planner utilities"""
    
    def test_calculate_bmi(self):
        """Test BMI calculation"""
        # Normal weight
        bmi, category = calculate_bmi(170, 70)
        self.assertAlmostEqual(bmi, 24.2, places=1)
        self.assertEqual(category, "Normal")
        
        # Underweight
        bmi, category = calculate_bmi(170, 50)
        self.assertAlmostEqual(bmi, 17.3, places=1)
        self.assertEqual(category, "Underweight")
        
        # Overweight
        bmi, category = calculate_bmi(170, 80)
        self.assertAlmostEqual(bmi, 27.7, places=1)
        self.assertEqual(category, "Overweight")
    
    def test_calculate_bmr(self):
        """Test BMR calculation"""
        # Male
        bmr_male = calculate_bmr(70, 170, 25, "Male")
        self.assertGreater(bmr_male, 1600)
        self.assertLess(bmr_male, 1800)
        
        # Female
        bmr_female = calculate_bmr(60, 160, 25, "Female")
        self.assertGreater(bmr_female, 1200)
        self.assertLess(bmr_female, 1400)
    
    def test_calculate_tdee(self):
        """Test TDEE calculation"""
        bmr = 1500
        tdee = calculate_tdee(bmr, "Moderate")
        self.assertAlmostEqual(tdee, 2325, places=0)
    
    def test_validate_user_inputs(self):
        """Test user input validation"""
        # Valid inputs
        valid_inputs = {
            'name': 'John Doe',
            'age': 25,
            'height_cm': 170,
            'weight_kg': 70,
            'goal': 'Weight Loss'
        }
        is_valid, errors = validate_user_inputs(valid_inputs)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Invalid age
        invalid_inputs = {
            'name': 'John Doe',
            'age': 5,  # Too young
            'height_cm': 170,
            'weight_kg': 70,
            'goal': 'Weight Loss'
        }
        is_valid, errors = validate_user_inputs(invalid_inputs)
        self.assertFalse(is_valid)
        self.assertIn("Age must be between 10 and 90", errors)
        
        # Missing required field
        incomplete_inputs = {
            'name': 'John Doe',
            'age': 25,
            'height_cm': 170,
            'weight_kg': 70
            # Missing 'goal'
        }
        is_valid, errors = validate_user_inputs(incomplete_inputs)
        self.assertFalse(is_valid)
        self.assertIn("goal is required", errors)


if __name__ == '__main__':
    unittest.main()
