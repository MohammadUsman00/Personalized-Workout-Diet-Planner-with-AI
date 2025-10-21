"""
Futuristic UI Components for AI-Powered Workout Planner
"""

import streamlit as st
from typing import Dict, List, Any, Optional
import time
import random


class AIUIComponents:
    """Futuristic UI components with AI-powered styling"""
    
    @staticmethod
    def ai_header(title: str, subtitle: str = ""):
        """Create futuristic AI header with animations"""
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');
        
        .ai-header {{
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }}
        
        .ai-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: scan 3s infinite;
        }}
        
        @keyframes scan {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        
        .ai-title {{
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #00d4ff, #00ff88, #ff6b6b, #ffd93d);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: gradient-shift 4s ease-in-out infinite;
            text-align: center;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        }}
        
        @keyframes gradient-shift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .ai-subtitle {{
            font-family: 'Exo 2', sans-serif;
            font-size: 1.2rem;
            color: #a0a0a0;
            text-align: center;
            font-weight: 300;
            letter-spacing: 1px;
        }}
        
        .ai-particles {{
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00d4ff;
            border-radius: 50%;
            animation: float 6s infinite ease-in-out;
        }}
        
        .ai-particles:nth-child(1) {{ top: 20%; left: 10%; animation-delay: 0s; }}
        .ai-particles:nth-child(2) {{ top: 60%; left: 80%; animation-delay: 2s; }}
        .ai-particles:nth-child(3) {{ top: 30%; left: 60%; animation-delay: 4s; }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); opacity: 0.7; }}
            50% {{ transform: translateY(-20px) rotate(180deg); opacity: 1; }}
        }}
        </style>
        
        <div class="ai-header">
            <div class="ai-particles"></div>
            <div class="ai-particles"></div>
            <div class="ai-particles"></div>
            <div class="ai-title">{title}</div>
            <div class="ai-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def ai_metric_card(title: str, value: str, change: str = "", icon: str = "🤖"):
        """Create futuristic metric card"""
        st.markdown(f"""
        <style>
        .ai-metric-card {{
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            border: 1px solid #00d4ff;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px rgba(0, 212, 255, 0.1);
        }}
        
        .ai-metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 212, 255, 0.2);
            border-color: #00ff88;
        }}
        
        .ai-metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #00d4ff, #00ff88, #ff6b6b);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
        }}
        
        .ai-metric-title {{
            font-family: 'Exo 2', sans-serif;
            font-size: 0.9rem;
            color: #a0a0a0;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .ai-metric-value {{
            font-family: 'Orbitron', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            color: #00d4ff;
            margin-bottom: 0.25rem;
        }}
        
        .ai-metric-change {{
            font-family: 'Exo 2', sans-serif;
            font-size: 0.8rem;
            color: #00ff88;
        }}
        
        .ai-metric-icon {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            font-size: 1.5rem;
            opacity: 0.3;
        }}
        </style>
        
        <div class="ai-metric-card">
            <div class="ai-metric-icon">{icon}</div>
            <div class="ai-metric-title">{title}</div>
            <div class="ai-metric-value">{value}</div>
            <div class="ai-metric-change">{change}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def ai_progress_bar(progress: float, label: str = "", color: str = "#00d4ff"):
        """Create futuristic progress bar"""
        st.markdown(f"""
        <style>
        .ai-progress-container {{
            background: #1e1e2e;
            border-radius: 25px;
            padding: 4px;
            margin: 1rem 0;
            border: 1px solid #333;
            position: relative;
            overflow: hidden;
        }}
        
        .ai-progress-bar {{
            background: linear-gradient(90deg, {color}, #00ff88);
            height: 20px;
            border-radius: 20px;
            position: relative;
            transition: width 1s ease;
            box-shadow: 0 0 20px {color}40;
        }}
        
        .ai-progress-bar::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        .ai-progress-label {{
            font-family: 'Exo 2', sans-serif;
            color: #a0a0a0;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}
        </style>
        
        <div class="ai-progress-label">{label}</div>
        <div class="ai-progress-container">
            <div class="ai-progress-bar" style="width: {progress}%;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def ai_loading_spinner(message: str = "AI is thinking..."):
        """Create futuristic loading spinner"""
        st.markdown(f"""
        <style>
        .ai-loading {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem;
        }}
        
        .ai-spinner {{
            width: 60px;
            height: 60px;
            border: 3px solid #1e1e2e;
            border-top: 3px solid #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .ai-loading-text {{
            font-family: 'Exo 2', sans-serif;
            color: #00d4ff;
            font-size: 1.1rem;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.7; }}
            50% {{ opacity: 1; }}
        }}
        </style>
        
        <div class="ai-loading">
            <div class="ai-spinner"></div>
            <div class="ai-loading-text">{message}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def ai_insight_card(insight: Dict):
        """Create AI insight card"""
        priority_colors = {
            "high": "#ff6b6b",
            "medium": "#ffd93d", 
            "low": "#00ff88"
        }
        
        color = priority_colors.get(insight.get("priority", "medium"), "#ffd93d")
        
        st.markdown(f"""
        <style>
        .ai-insight-card {{
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            border-left: 4px solid {color};
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .ai-insight-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }}
        
        .ai-insight-title {{
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            color: {color};
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}
        
        .ai-insight-description {{
            font-family: 'Exo 2', sans-serif;
            color: #e0e0e0;
            line-height: 1.6;
            margin-bottom: 1rem;
        }}
        
        .ai-insight-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'Exo 2', sans-serif;
            font-size: 0.8rem;
            color: #a0a0a0;
        }}
        
        .ai-confidence {{
            background: {color}20;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            border: 1px solid {color};
        }}
        </style>
        
        <div class="ai-insight-card">
            <div class="ai-insight-title">{insight.get('title', 'AI Insight')}</div>
            <div class="ai-insight-description">{insight.get('description', 'No description available.')}</div>
            <div class="ai-insight-meta">
                <span>Confidence: {insight.get('confidence', 0.8):.0%}</span>
                <span class="ai-confidence">{insight.get('priority', 'medium').upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def ai_chat_bubble(message: str, is_user: bool = True):
        """Create AI chat bubble"""
        if is_user:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                <div style="
                    background: linear-gradient(135deg, #00d4ff, #00ff88);
                    color: #1e1e2e;
                    padding: 1rem 1.5rem;
                    border-radius: 20px 20px 5px 20px;
                    max-width: 70%;
                    font-family: 'Exo 2', sans-serif;
                    box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
                ">
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                <div style="
                    background: linear-gradient(135deg, #2d2d44, #1e1e2e);
                    color: #e0e0e0;
                    padding: 1rem 1.5rem;
                    border-radius: 20px 20px 20px 5px;
                    max-width: 70%;
                    font-family: 'Exo 2', sans-serif;
                    border: 1px solid #00d4ff;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                ">
                    <div style="color: #00d4ff; font-weight: 600; margin-bottom: 0.5rem;">🤖 AI Coach</div>
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def ai_tab_selector(tabs: List[str], active_tab: int = 0):
        """Create futuristic tab selector"""
        st.markdown(f"""
        <style>
        .ai-tab-container {{
            display: flex;
            background: #1e1e2e;
            border-radius: 15px;
            padding: 0.5rem;
            margin: 1rem 0;
            border: 1px solid #333;
        }}
        
        .ai-tab {{
            flex: 1;
            padding: 1rem;
            text-align: center;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            color: #a0a0a0;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .ai-tab.active {{
            background: linear-gradient(135deg, #00d4ff, #00ff88);
            color: #1e1e2e;
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
        }}
        
        .ai-tab:hover:not(.active) {{
            background: #2d2d44;
            color: #e0e0e0;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Create tabs using Streamlit's native tabs
        return st.tabs(tabs)
    
    @staticmethod
    def ai_sidebar_style():
        """Apply futuristic styling to sidebar"""
        st.markdown("""
        <style>
        .css-1d391kg {
            background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            border-right: 2px solid #00d4ff;
        }
        
        .stSidebar .stSelectbox > div > div {
            background: #1e1e2e;
            border: 1px solid #00d4ff;
            border-radius: 8px;
        }
        
        .stSidebar .stTextInput > div > div > input {
            background: #1e1e2e;
            border: 1px solid #00d4ff;
            border-radius: 8px;
            color: #e0e0e0;
        }
        
        .stSidebar .stButton > button {
            background: linear-gradient(135deg, #00d4ff, #00ff88);
            color: #1e1e2e;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stSidebar .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
        }
        </style>
        """, unsafe_allow_html=True)
