# 🧘‍♀️ AI-Powered Personalized Workout & Diet Planner v2.0

Create comprehensive, science-based 7-day workout and meal plans using advanced AI technology with enhanced features for progress tracking and personalized recommendations.

## ✨ Enhanced Features

### 🎯 Core Functionality
- **Advanced AI Prompts**: Enhanced prompts with detailed instructions for comprehensive plans
- **Personalized Profiles**: Detailed user profiling with health metrics and preferences
- **Progress Tracking**: Interactive dashboard for monitoring fitness and nutrition progress
- **Enhanced UI/UX**: Modern, responsive design with beautiful animations and styling

### 🏋️ Workout Features
- **7-Day Workout Plans**: Detailed daily workout routines with warm-up, main exercises, and cool-down
- **Equipment-Based Plans**: Customized based on available equipment (home gym, dumbbells, resistance bands, etc.)
- **Experience Levels**: Plans tailored for beginners, intermediate, and advanced users
- **Exercise Alternatives**: Alternative exercises for limited equipment or time constraints
- **Calorie Tracking**: Estimated calories burned for each workout

### 🍽️ Nutrition Features
- **Cultural Food Preferences**: Plans respecting cultural and regional food preferences
- **Dietary Restrictions**: Support for vegetarian, vegan, keto, paleo, and other dietary preferences
- **Budget-Conscious Planning**: Meal plans based on budget levels (low, moderate, high)
- **Macro Tracking**: Detailed macronutrient breakdown and calorie counting
- **Shopping Lists**: Weekly shopping lists for meal preparation

### 📊 Progress & Analytics
- **Progress Dashboard**: Interactive tracking of workouts, nutrition, and health metrics
- **Weekly Overview**: Summary of completed workouts and nutrition adherence
- **Workout Logging**: Daily workout tracking with duration, intensity, and notes
- **Nutrition Logging**: Track calories, macros, and water intake
- **Analytics**: Progress trends and insights for motivation

### 📄 Enhanced PDF Generation
- **Professional Formatting**: Beautiful PDFs with headers, colors, and proper formatting
- **Generation Timestamps**: Automatic date and time stamps
- **Branded Footers**: Professional branding in generated documents
- **Improved Layout**: Better spacing and typography for readability

## 📦 Tech Stack

### Core Technologies
- **Frontend**: Streamlit with enhanced UI components
- **Backend**: Python with modular architecture
- **AI**: Google Gemini 2.0 Flash for intelligent plan generation
- **Data**: Pandas for data manipulation and CSV storage
- **PDF**: FPDF2 for professional document generation

### Additional Libraries
- **Plotly**: For interactive charts and visualizations
- **Streamlit Extras**: Enhanced UI components
- **Python-dotenv**: Environment variable management

## 📁 Project Structure
```
workout-ai/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── utils.py              # Utility functions
├── test_app.py           # Unit tests
├── requirements.txt      # Python dependencies
├── plans_history.csv    # User plan history
├── .env                  # Environment variables
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone or download the project
cd workout-ai

# Install dependencies
pip install -r requirements.txt
```

### 2. API Configuration
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run the Application
```bash
streamlit run app.py
```

## 🎯 Usage Guide

### 1. Profile Setup
- Fill in personal details (name, age, height, weight)
- Select fitness goals and experience level
- Specify dietary preferences and cultural food types
- Choose available equipment and time constraints
- Set budget level for meal planning

### 2. Plan Generation
- Click "Generate My Personalized Plan" to create your 7-day plan
- Review the comprehensive workout and nutrition plans
- Download PDF versions for offline access

### 3. Progress Tracking
- Use the Progress Tracking tab to log daily activities
- Monitor workout completion and nutrition adherence
- View analytics and progress trends
- Set and track weekly goals

## 🔧 Configuration

### Customizing the App
Edit `config.py` to modify:
- Fitness goals and dietary preferences
- Equipment options and workout frequencies
- Color schemes and UI settings
- PDF formatting options

### Adding New Features
- Extend the utility functions in `utils.py`
- Add new tracking metrics in the progress dashboard
- Customize AI prompts for different plan types

## 🧪 Testing

Run the test suite to ensure everything works correctly:
```bash
python test_app.py
```

## 📊 Data Storage

### Current Implementation
- **CSV Storage**: User plans saved to `plans_history.csv`
- **Session State**: Temporary data stored in Streamlit session
- **Progress Tracking**: In-memory storage (can be extended to database)

### Future Enhancements
- Database integration (SQLite, PostgreSQL)
- User authentication and profiles
- Cloud storage for plan backups
- Social features and community sharing

## 🎨 UI/UX Features

### Modern Design
- **Gradient Headers**: Beautiful animated gradient text
- **Card-Based Layout**: Clean, organized information display
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects and smooth transitions

### Enhanced Navigation
- **Tabbed Interface**: Organized content in easy-to-navigate tabs
- **Expandable Sections**: Collapsible sidebar sections for better organization
- **Progress Indicators**: Visual feedback for user actions
- **Color-Coded Metrics**: BMI and health metrics with appropriate colors

## 🔒 Privacy & Security

- **Local Data Storage**: All data stored locally on your device
- **No User Tracking**: No personal data sent to external services
- **Secure API Usage**: API keys stored in environment variables
- **Data Control**: Users can delete their data at any time

## 🚀 Future Roadmap

### Phase 1 (Current)
- ✅ Enhanced UI/UX design
- ✅ Progress tracking dashboard
- ✅ Improved PDF generation
- ✅ Better AI prompts

### Phase 2 (Planned)
- 🔄 Database integration
- 🔄 User authentication
- 🔄 Advanced analytics
- 🔄 Social features

### Phase 3 (Future)
- 📱 Mobile app version
- 🌐 Web deployment
- 🤖 Advanced AI features
- 📊 Machine learning insights

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## ❤️ Acknowledgments

- **Google Gemini**: For powerful AI capabilities
- **Streamlit**: For the amazing web framework
- **Open Source Community**: For the incredible libraries and tools

---

**Made with ❤️ using Gemini Flash + Streamlit + Advanced AI**

*Transform your fitness journey with personalized, science-based workout and nutrition plans!*


