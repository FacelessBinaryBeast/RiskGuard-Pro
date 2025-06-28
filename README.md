# 🤖 AI-Powered Underwriting Risk Assessment System

A comprehensive insurance underwriting and risk assessment platform that integrates with **Gemini Flash 2.0** for advanced AI-powered analysis and recommendations.

## 🚀 Features

### 📋 Multi-Step Form System
- **Basic Information**: Personal details, contact info, location
- **Lifestyle Details**: Occupation, activity level, habits, commute
- **Family Information**: Dependents, family medical history
- **Financial Profile**: Employment, income, expenses, stability
- **Insurance Coverage**: Existing policies, claims history
- **Medical Information**: Health conditions, medications, BMI
- **Preferences**: Risk appetite, budget, insurance interests

### 🎯 Risk Assessment
- **100-Point Scoring System**: Comprehensive risk evaluation
- **5 Risk Categories**: Very Low to Very High
- **Detailed Breakdown**: Individual factor analysis
- **Visual Indicators**: Color-coded risk levels
- **Personalized Recommendations**: Actionable improvement suggestions

### 🤖 AI Integration
- **Gemini Flash 2.0**: Advanced AI analysis
- **Comprehensive Reports**: Detailed JSON analysis
- **Underwriting Decisions**: Accept/Decline/Refer recommendations
- **Coverage Suggestions**: Personalized insurance recommendations
- **Market Insights**: Industry comparison and trends

### 📄 Report Generation
- **PDF Reports**: Professional downloadable reports
- **JSON Export**: Structured data export
- **AI Analysis**: Comprehensive AI-powered insights
- **Risk Breakdown**: Detailed scoring explanation

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Gemini API key from Google AI Studio

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd UnderwriterRisk-Calc
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   echo "FLASK_SECRET_KEY=your_secret_key_here" >> .env
   ```

5. **Get Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Add it to your `.env` file

## 🚀 Usage

### Running the Web Application
```bash
python app.py
```
Access the application at: `http://localhost:5000`

### Running AI Analysis
```bash
python main.py
```

### API Endpoints

#### Web Application Routes
- `/` - Landing page
- `/basics` - Basic information form
- `/additional` - Lifestyle details form
- `/familydetails` - Family information form
- `/finances` - Financial information form
- `/coverage` - Insurance coverage form
- `/medical` - Medical information form
- `/preferences` - Preferences form
- `/summary` - Summary and risk assessment

#### API Endpoints
- `POST /api/save_basics` - Save basic information
- `POST /api/save_additional` - Save lifestyle information
- `POST /api/save_family` - Save family information
- `POST /api/save_finances` - Save financial information
- `POST /api/save_coverage` - Save coverage information
- `POST /api/save_medical` - Save medical information
- `POST /api/save_preferences` - Save preferences
- `GET /api/get_all_data` - Get all saved data
- `POST /api/generate_pdf` - Generate PDF report
- `POST /api/clear_session` - Clear session data

## 📊 Risk Assessment System

### Scoring Categories (100-Point Scale)

1. **Age Factor (20 points)**
   - < 25 years: 5 points
   - 25-29 years: 8 points
   - 30-34 years: 12 points
   - 35-39 years: 16 points
   - 40-44 years: 20 points
   - 45-49 years: 25 points
   - 50-54 years: 30 points
   - 55-59 years: 35 points
   - 60+ years: 40 points

2. **Lifestyle Factors (25 points)**
   - Smoking: 10 points
   - Alcohol: 0-5 points
   - Physical Activity: 0-5 points
   - BMI: 0-5 points

3. **Medical Factors (25 points)**
   - Pre-existing conditions: 15 points
   - Family history: 5 points
   - Recent hospitalizations: 5 points

4. **Occupation Factors (15 points)**
   - High-risk occupations: 10 points
   - High-risk work types: 5 points

5. **Financial Stability (15 points)**
   - Employment status: 0-10 points
   - Income stability: 0-5 points
   - Disposable income: 0-5 points

### Risk Levels
- **Very Low (0-20)**: A+ Rating, ₹15L coverage, ₹250 premium
- **Low (21-35)**: A Rating, ₹12L coverage, ₹350 premium
- **Moderate (36-50)**: B Rating, ₹10L coverage, ₹500 premium
- **High (51-70)**: C Rating, ₹7.5L coverage, ₹750 premium
- **Very High (71-100)**: D Rating, ₹5L coverage, ₹1,200 premium

## 🤖 AI Integration

### Gemini Flash 2.0 Analysis
The system uses Gemini Flash 2.0 for advanced analysis:

```python
from main import UnderwritingAIAnalyzer

# Initialize analyzer
analyzer = UnderwritingAIAnalyzer(api_key="your_gemini_api_key")

# Collect data
structured_data = analyzer.collect_all_data(session_data)

# Get AI analysis
ai_analysis = analyzer.analyze_with_gemini(structured_data)

# Generate comprehensive report
report = analyzer.generate_comprehensive_report(structured_data, ai_analysis)

# Save report
filepath = analyzer.save_report(report)
```

### AI Analysis Output
The AI provides:
- **Risk Assessment**: Overall risk level, score, rating
- **Coverage Recommendations**: Life, health, and additional coverage
- **Underwriting Decision**: Accept/Decline/Refer with conditions
- **AI Insights**: Risk trends, market comparison
- **Detailed Recommendations**: Actionable improvement strategies

## 📁 Project Structure

```
UnderwriterRisk-Calc/
├── app.py                 # Flask web application
├── main.py               # AI analysis and data processing
├── underwriting_agent.py # FastAPI alternative backend
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── landing.html
│   ├── basics.html
│   ├── additional.html
│   ├── familydetails.html
│   ├── finances.html
│   ├── coverage.html
│   ├── medical.html
│   ├── preferences.html
│   └── summary.html
├── static/              # CSS and static files
│   └── styles.css
├── reports/             # Generated reports (created automatically)
└── venv/               # Virtual environment
```

## 🔧 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Customization
- Modify risk scoring weights in `app.py` and `templates/summary.html`
- Adjust AI prompts in `main.py`
- Customize PDF templates in `app.py`
- Update form fields in HTML templates

## 📈 Data Flow

1. **Data Collection**: Multi-step form system collects comprehensive information
2. **Data Storage**: Information saved to localStorage and server session
3. **Risk Calculation**: 100-point scoring system applied
4. **AI Analysis**: Data sent to Gemini Flash 2.0 for advanced analysis
5. **Report Generation**: Comprehensive reports generated in PDF and JSON
6. **Recommendations**: Personalized suggestions for improvement

## 🛡️ Security Features

- **Session Management**: Secure session handling
- **Data Validation**: Input validation and sanitization
- **API Key Protection**: Environment variable storage
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging for debugging

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use production WSGI server (Gunicorn, uWSGI)
3. Set up reverse proxy (Nginx)
4. Configure SSL certificates
5. Set up monitoring and logging

## 📞 Support

For issues and questions:
1. Check the logs for error messages
2. Verify API key configuration
3. Ensure all dependencies are installed
4. Check network connectivity for AI API calls

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📊 Performance

- **Form Loading**: < 2 seconds
- **Risk Calculation**: < 1 second
- **AI Analysis**: 5-15 seconds (depending on data complexity)
- **PDF Generation**: 2-5 seconds
- **Report Saving**: < 1 second

---

**Built with ❤️ using Flask, Gemini Flash 2.0, and modern web technologies** 