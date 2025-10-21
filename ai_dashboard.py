"""
AI-Powered Dashboard for Advanced Analytics and Insights
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
from ai_services import AIOrchestrator, AIInsight
from ui_components import AIUIComponents


class AIDashboard:
    """AI-powered dashboard with advanced analytics"""
    
    def __init__(self, ai_orchestrator: AIOrchestrator):
        self.ai = ai_orchestrator
        self.ui = AIUIComponents()
    
    def render_ai_overview(self, user_profile: Dict, progress_data: List[Dict]):
        """Render AI overview dashboard"""
        self.ui.ai_header("🧠 AI-Powered Analytics", "Advanced insights powered by artificial intelligence")
        
        # Get AI insights
        insights = self.ai.get_ai_insights(user_profile, progress_data)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.ui.ai_metric_card(
                "AI Confidence",
                f"{len(insights)}",
                "Active Insights",
                "🤖"
            )
        
        with col2:
            self.ui.ai_metric_card(
                "Progress Score",
                "87%",
                "+12% this week",
                "📈"
            )
        
        with col3:
            self.ui.ai_metric_card(
                "Optimization",
                "5",
                "AI Recommendations",
                "⚡"
            )
        
        with col4:
            self.ui.ai_metric_card(
                "Risk Level",
                "Low",
                "All systems optimal",
                "🛡️"
            )
        
        # Display AI insights
        st.markdown("### 🔍 AI Insights & Recommendations")
        for insight in insights:
            self.ui.ai_insight_card({
                "title": insight.title,
                "description": insight.description,
                "confidence": insight.confidence,
                "priority": insight.priority
            })
    
    def render_predictions_dashboard(self, user_profile: Dict, historical_data: List[Dict]):
        """Render AI predictions dashboard"""
        self.ui.ai_header("🔮 AI Predictions", "Future progress predictions based on your data")
        
        # Generate predictions
        predictions = self.ai.analytics_ai.generate_predictions(user_profile, historical_data)
        
        # Create prediction charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Weight Progression Prediction")
            self._create_weight_prediction_chart()
        
        with col2:
            st.markdown("#### 💪 Strength Gains Prediction")
            self._create_strength_prediction_chart()
        
        # AI recommendations
        st.markdown("#### 🎯 AI Recommendations")
        recommendations = self.ai.analytics_ai.generate_recommendations(user_profile, {})
        
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
    
    def render_nutrition_analytics(self, nutrition_data: List[Dict]):
        """Render AI nutrition analytics"""
        self.ui.ai_header("🍽️ AI Nutrition Analytics", "Smart nutrition insights and optimization")
        
        if not nutrition_data:
            st.info("No nutrition data available. Start logging your meals to get AI insights!")
            return
        
        # Create nutrition charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Macronutrient Distribution")
            self._create_macro_chart(nutrition_data)
        
        with col2:
            st.markdown("#### 📈 Calorie Trends")
            self._create_calorie_trend_chart(nutrition_data)
        
        # AI nutrition analysis
        analysis = self.ai.nutrition_ai.analyze_nutrition_patterns(nutrition_data)
        
        st.markdown("#### 🧠 AI Nutrition Analysis")
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid #00d4ff;
            box-shadow: 0 10px 25px rgba(0, 212, 255, 0.1);
        ">
            <h4 style="color: #00d4ff; margin-bottom: 1rem;">🤖 AI Analysis</h4>
            <p style="color: #e0e0e0; line-height: 1.6;">{analysis.get('analysis', 'No analysis available.')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_workout_analytics(self, workout_data: List[Dict]):
        """Render AI workout analytics"""
        self.ui.ai_header("🏋️ AI Workout Analytics", "Smart workout insights and performance optimization")
        
        if not workout_data:
            st.info("No workout data available. Start logging your workouts to get AI insights!")
            return
        
        # Workout performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_workouts = len(workout_data)
            self.ui.ai_metric_card(
                "Total Workouts",
                str(total_workouts),
                "This month",
                "🏋️"
            )
        
        with col2:
            avg_duration = sum(w.get('duration', 0) for w in workout_data) / len(workout_data)
            self.ui.ai_metric_card(
                "Avg Duration",
                f"{avg_duration:.0f} min",
                "Per workout",
                "⏱️"
            )
        
        with col3:
            high_intensity = len([w for w in workout_data if w.get('intensity') == 'High'])
            self.ui.ai_metric_card(
                "High Intensity",
                f"{high_intensity}",
                f"{high_intensity/len(workout_data)*100:.0f}% of workouts",
                "🔥"
            )
        
        # Workout trends chart
        st.markdown("#### 📈 Workout Performance Trends")
        self._create_workout_trends_chart(workout_data)
    
    def render_ai_chat(self, user_context: Dict):
        """Render AI chat interface"""
        self.ui.ai_header("💬 AI Fitness Coach", "Chat with your personal AI fitness coach")
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        for message in st.session_state.chat_history:
            self.ui.ai_chat_bubble(message["content"], message["is_user"])
        
        # Chat input
        with st.form("ai_chat_form"):
            user_input = st.text_area(
                "Ask your AI coach anything about fitness, nutrition, or your progress:",
                placeholder="e.g., 'How can I improve my bench press?' or 'What should I eat before a workout?'",
                height=100
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                send_button = st.form_submit_button("Send", use_container_width=True)
            with col2:
                clear_button = st.form_submit_button("Clear Chat", use_container_width=True)
        
        if send_button and user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                "content": user_input,
                "is_user": True
            })
            
            # Get AI response
            with st.spinner("AI Coach is thinking..."):
                ai_response = self.ai.chat_ai.chat_with_ai(user_input, user_context)
            
            # Add AI response to history
            st.session_state.chat_history.append({
                "content": ai_response,
                "is_user": False
            })
            
            st.rerun()
        
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()
    
    def _create_weight_prediction_chart(self):
        """Create weight prediction chart"""
        # Sample data - in real app, this would come from AI predictions
        weeks = list(range(1, 9))
        predicted_weights = [70, 69.5, 69, 68.5, 68, 67.5, 67, 66.5]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weeks,
            y=predicted_weights,
            mode='lines+markers',
            name='AI Prediction',
            line=dict(color='#00d4ff', width=3),
            marker=dict(size=8, color='#00d4ff')
        ))
        
        fig.update_layout(
            title="Weight Progression Forecast",
            xaxis_title="Weeks",
            yaxis_title="Weight (kg)",
            plot_bgcolor='#1e1e2e',
            paper_bgcolor='#1e1e2e',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _create_strength_prediction_chart(self):
        """Create strength prediction chart"""
        weeks = list(range(1, 9))
        bench_press = [60, 65, 70, 75, 80, 85, 90, 95]
        squat = [80, 85, 90, 95, 100, 105, 110, 115]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weeks,
            y=bench_press,
            mode='lines+markers',
            name='Bench Press',
            line=dict(color='#00ff88', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=weeks,
            y=squat,
            mode='lines+markers',
            name='Squat',
            line=dict(color='#ff6b6b', width=3)
        ))
        
        fig.update_layout(
            title="Strength Gains Forecast",
            xaxis_title="Weeks",
            yaxis_title="Weight (kg)",
            plot_bgcolor='#1e1e2e',
            paper_bgcolor='#1e1e2e',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _create_macro_chart(self, nutrition_data: List[Dict]):
        """Create macronutrient chart"""
        # Sample data - in real app, calculate from nutrition_data
        labels = ['Protein', 'Carbs', 'Fat']
        values = [30, 45, 25]
        colors = ['#00d4ff', '#00ff88', '#ff6b6b']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.4
        )])
        
        fig.update_layout(
            title="Macronutrient Distribution",
            plot_bgcolor='#1e1e2e',
            paper_bgcolor='#1e1e2e',
            font=dict(color='#e0e0e0')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _create_calorie_trend_chart(self, nutrition_data: List[Dict]):
        """Create calorie trend chart"""
        # Sample data - in real app, use actual nutrition_data
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        calories = [2000, 2200, 1800, 2400, 2100, 1900, 2300]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=days,
            y=calories,
            mode='lines+markers',
            name='Daily Calories',
            line=dict(color='#00d4ff', width=3),
            marker=dict(size=8, color='#00d4ff')
        ))
        
        fig.update_layout(
            title="Daily Calorie Intake",
            xaxis_title="Day",
            yaxis_title="Calories",
            plot_bgcolor='#1e1e2e',
            paper_bgcolor='#1e1e2e',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _create_workout_trends_chart(self, workout_data: List[Dict]):
        """Create workout trends chart"""
        # Sample data - in real app, use actual workout_data
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        duration = [45, 60, 30, 75, 50, 40, 65]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=days,
            y=duration,
            name='Workout Duration',
            marker=dict(color='#00d4ff')
        ))
        
        fig.update_layout(
            title="Weekly Workout Duration",
            xaxis_title="Day",
            yaxis_title="Duration (minutes)",
            plot_bgcolor='#1e1e2e',
            paper_bgcolor='#1e1e2e',
            font=dict(color='#e0e0e0'),
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
