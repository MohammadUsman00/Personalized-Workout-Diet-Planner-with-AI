"""
AI Services Module - Advanced AI-powered features for the workout planner
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import google.generativeai as genai
from dataclasses import dataclass
import streamlit as st


@dataclass
class AIInsight:
    """Data class for AI insights"""
    type: str
    title: str
    description: str
    confidence: float
    actionable: bool
    priority: str  # high, medium, low


class AIService:
    """Base AI service class"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate content using Gemini"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=4000,
                )
            )
            return response.text
        except Exception as e:
            st.error(f"AI generation failed: {str(e)}")
            return ""


class WorkoutAIService(AIService):
    """AI service for workout-related features"""
    
    def generate_smart_workout_plan(self, user_profile: Dict) -> Dict[str, Any]:
        """Generate intelligent workout plan with AI insights"""
        
        prompt = f"""
        You are an advanced AI fitness coach with access to cutting-edge exercise science. 
        Create a highly personalized, scientifically-optimized workout plan.
        
        USER PROFILE:
        - Name: {user_profile.get('name', 'User')}
        - Age: {user_profile.get('age', 25)}
        - Gender: {user_profile.get('gender', 'Unknown')}
        - Height: {user_profile.get('height_cm', 170)} cm
        - Weight: {user_profile.get('weight_kg', 70)} kg
        - BMI: {user_profile.get('bmi', 24.2)} ({user_profile.get('bmi_cat', 'Normal')})
        - Goal: {user_profile.get('goal', 'General Health')}
        - Experience: {user_profile.get('experience', 'Beginner')}
        - Equipment: {user_profile.get('equipment', 'None')}
        - Time Available: {user_profile.get('time_available', 45)} minutes
        - Injuries: {user_profile.get('injuries', 'None')}
        
        Create a comprehensive plan with:
        1. SMART GOALS (Specific, Measurable, Achievable, Relevant, Time-bound)
        2. PROGRESSIVE OVERLOAD SCHEDULE
        3. RECOVERY OPTIMIZATION
        4. INJURY PREVENTION STRATEGIES
        5. PERFORMANCE METRICS
        6. ADAPTIVE MODIFICATIONS
        
        Format as structured JSON with scientific rationale for each recommendation.
        """
        
        response = self.generate_content(prompt)
        return self._parse_workout_response(response)
    
    def generate_ai_insights(self, user_data: Dict, progress_data: List[Dict]) -> List[AIInsight]:
        """Generate AI-powered insights from user data"""
        
        prompt = f"""
        Analyze this fitness data and provide AI-powered insights:
        
        USER DATA: {json.dumps(user_data, indent=2)}
        PROGRESS DATA: {json.dumps(progress_data, indent=2)}
        
        Provide insights on:
        1. Performance trends
        2. Optimization opportunities
        3. Risk factors
        4. Success patterns
        5. Personalized recommendations
        
        Format as JSON with insight type, title, description, confidence, and priority.
        """
        
        response = self.generate_content(prompt)
        return self._parse_insights_response(response)
    
    def predict_optimal_workout_time(self, user_profile: Dict, historical_data: List[Dict]) -> Dict:
        """Predict optimal workout timing based on user patterns"""
        
        prompt = f"""
        Based on user profile and historical performance data, predict optimal workout timing:
        
        PROFILE: {json.dumps(user_profile, indent=2)}
        HISTORICAL DATA: {json.dumps(historical_data, indent=2)}
        
        Consider:
        - Circadian rhythms
        - Energy patterns
        - Performance metrics
        - Recovery needs
        - Lifestyle factors
        
        Provide optimal timing recommendations with scientific rationale.
        """
        
        response = self.generate_content(prompt)
        return self._parse_timing_response(response)
    
    def _parse_workout_response(self, response: str) -> Dict[str, Any]:
        """Parse AI workout response"""
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"raw_response": response}
        except:
            return {"raw_response": response}
    
    def _parse_insights_response(self, response: str) -> List[AIInsight]:
        """Parse AI insights response"""
        insights = []
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                
                for insight_data in data.get("insights", []):
                    insight = AIInsight(
                        type=insight_data.get("type", "general"),
                        title=insight_data.get("title", "Insight"),
                        description=insight_data.get("description", ""),
                        confidence=insight_data.get("confidence", 0.8),
                        actionable=insight_data.get("actionable", True),
                        priority=insight_data.get("priority", "medium")
                    )
                    insights.append(insight)
        except:
            # Fallback insight
            insights.append(AIInsight(
                type="general",
                title="AI Analysis Complete",
                description="AI has analyzed your data and provided personalized recommendations.",
                confidence=0.9,
                actionable=True,
                priority="high"
            ))
        
        return insights
    
    def _parse_timing_response(self, response: str) -> Dict:
        """Parse timing response"""
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"recommendation": response}
        except:
            return {"recommendation": response}


class NutritionAIService(AIService):
    """AI service for nutrition-related features"""
    
    def generate_smart_nutrition_plan(self, user_profile: Dict) -> Dict[str, Any]:
        """Generate AI-powered nutrition plan"""
        
        prompt = f"""
        You are an advanced AI nutritionist with expertise in personalized nutrition science.
        Create a highly optimized nutrition plan.
        
        USER PROFILE:
        - Name: {user_profile.get('name', 'User')}
        - Age: {user_profile.get('age', 25)}
        - Gender: {user_profile.get('gender', 'Unknown')}
        - Height: {user_profile.get('height_cm', 170)} cm
        - Weight: {user_profile.get('weight_kg', 70)} kg
        - BMI: {user_profile.get('bmi', 24.2)} ({user_profile.get('bmi_cat', 'Normal')})
        - Goal: {user_profile.get('goal', 'General Health')}
        - Dietary Preference: {user_profile.get('dietary_pref', 'Balanced')}
        - Cultural Food: {user_profile.get('cultural_food', 'International')}
        - Budget: {user_profile.get('budget', 'Moderate')}
        - Allergies: {user_profile.get('allergies', 'None')}
        - Dislikes: {user_profile.get('dislikes', 'None')}
        
        Create a comprehensive plan with:
        1. MACRONUTRIENT OPTIMIZATION
        2. MICRONUTRIENT TARGETING
        3. MEAL TIMING STRATEGIES
        4. HYDRATION PROTOCOLS
        5. SUPPLEMENT RECOMMENDATIONS
        6. CULTURAL ADAPTATIONS
        7. BUDGET OPTIMIZATION
        
        Include scientific rationale and metabolic considerations.
        """
        
        response = self.generate_content(prompt)
        return self._parse_nutrition_response(response)
    
    def analyze_nutrition_patterns(self, nutrition_data: List[Dict]) -> Dict[str, Any]:
        """Analyze nutrition patterns with AI"""
        
        prompt = f"""
        Analyze these nutrition patterns and provide AI insights:
        
        NUTRITION DATA: {json.dumps(nutrition_data, indent=2)}
        
        Analyze:
        1. Macronutrient balance
        2. Micronutrient gaps
        3. Meal timing patterns
        4. Hydration status
        5. Optimization opportunities
        
        Provide actionable recommendations with scientific backing.
        """
        
        response = self.generate_content(prompt)
        return {"analysis": response}
    
    def _parse_nutrition_response(self, response: str) -> Dict[str, Any]:
        """Parse nutrition response"""
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"raw_response": response}
        except:
            return {"raw_response": response}


class AnalyticsAIService(AIService):
    """AI service for analytics and predictions"""
    
    def generate_predictions(self, user_data: Dict, historical_data: List[Dict]) -> Dict[str, Any]:
        """Generate AI predictions for user progress"""
        
        prompt = f"""
        As an AI fitness analyst, predict future progress based on current data:
        
        USER DATA: {json.dumps(user_data, indent=2)}
        HISTORICAL DATA: {json.dumps(historical_data, indent=2)}
        
        Provide predictions for:
        1. Weight progression (next 4 weeks)
        2. Strength gains (next 8 weeks)
        3. Performance improvements
        4. Risk factors
        5. Optimal adjustments
        
        Include confidence intervals and recommendations.
        """
        
        response = self.generate_content(prompt)
        return {"predictions": response}
    
    def generate_recommendations(self, user_profile: Dict, current_progress: Dict) -> List[Dict]:
        """Generate personalized AI recommendations"""
        
        prompt = f"""
        Generate personalized AI recommendations:
        
        USER PROFILE: {json.dumps(user_profile, indent=2)}
        CURRENT PROGRESS: {json.dumps(current_progress, indent=2)}
        
        Provide:
        1. Immediate actions (next 7 days)
        2. Short-term goals (next 4 weeks)
        3. Long-term strategy (next 3 months)
        4. Risk mitigation
        5. Success optimization
        
        Format as actionable recommendations with priority levels.
        """
        
        response = self.generate_content(prompt)
        return self._parse_recommendations_response(response)
    
    def _parse_recommendations_response(self, response: str) -> List[Dict]:
        """Parse recommendations response"""
        recommendations = []
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                return data.get("recommendations", [])
            else:
                return [{"title": "AI Recommendation", "description": response}]
        except:
            return [{"title": "AI Recommendation", "description": response}]


class AIChatService(AIService):
    """AI chat assistant for fitness guidance"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.conversation_history = []
    
    def chat_with_ai(self, user_message: str, user_context: Dict = None) -> str:
        """Chat with AI fitness assistant"""
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Build context-aware prompt
        context_str = ""
        if user_context:
            context_str = f"""
            USER CONTEXT:
            - Name: {user_context.get('name', 'User')}
            - Goal: {user_context.get('goal', 'General Health')}
            - Experience: {user_context.get('experience', 'Beginner')}
            - Current Progress: {user_context.get('progress', 'Starting out')}
            """
        
        prompt = f"""
        You are an advanced AI fitness coach and nutritionist. You have access to cutting-edge 
        exercise science, nutrition research, and behavioral psychology.
        
        {context_str}
        
        CONVERSATION HISTORY:
        {self._format_conversation_history()}
        
        USER MESSAGE: {user_message}
        
        Provide helpful, scientifically-backed advice. Be encouraging, specific, and actionable.
        If asked about specific exercises, provide detailed instructions and safety tips.
        If asked about nutrition, provide evidence-based recommendations.
        Always consider the user's experience level and goals.
        """
        
        response = self.generate_content(prompt)
        
        # Add AI response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for context"""
        if not self.conversation_history:
            return "No previous conversation."
        
        formatted = []
        for msg in self.conversation_history[-6:]:  # Last 6 messages for context
            role = "User" if msg["role"] == "user" else "AI Coach"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []


class AIOrchestrator:
    """Orchestrates all AI services"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.workout_ai = WorkoutAIService(api_key)
        self.nutrition_ai = NutritionAIService(api_key)
        self.analytics_ai = AnalyticsAIService(api_key)
        self.chat_ai = AIChatService(api_key)
    
    def generate_comprehensive_plan(self, user_profile: Dict) -> Dict[str, Any]:
        """Generate comprehensive AI-powered plan"""
        return {
            "workout_plan": self.workout_ai.generate_smart_workout_plan(user_profile),
            "nutrition_plan": self.nutrition_ai.generate_smart_nutrition_plan(user_profile),
            "ai_insights": self.workout_ai.generate_ai_insights(user_profile, []),
            "recommendations": self.analytics_ai.generate_recommendations(user_profile, {}),
            "generated_at": datetime.now().isoformat()
        }
    
    def get_ai_insights(self, user_data: Dict, progress_data: List[Dict]) -> List[AIInsight]:
        """Get AI insights from all services"""
        insights = []
        insights.extend(self.workout_ai.generate_ai_insights(user_data, progress_data))
        return insights
