# 🤖 AI-Powered Underwriting Risk Assessment System

A comprehensive insurance underwriting and risk assessment platform that integrates with **Gemini 2.0 Flash** for advanced AI-powered analysis and recommendations.
#BFSI Sector #banking #finance #insurance #fintech #solutions 

## Hosted At

https://riskguard-pro.onrender.com/


Note: Due to use of free tier for hosting it may take a minute or two for the first loading or loading after long time.
Also as it is free tier it can be stopped deployed so please reach out by submitting a pull request.
Or you can aslo try by running it locally by downloading it.
Also it may not runsometimes as API Keys free tier limit restriction may kick in or if key is deleted or removed.
Also it may be slow to slow to load during process as hosted on a less memory free service tier.


Important Note: This project was made to showcase the skill of making AI Agent to use for Dynamic Underwriting and Risk Assesment . So it is provided with input and AI Agent does analysis for underwriting and risk assesment .
It does not provide user and insurer side control ,basically it is to depict capability to use and develop it for further use.
Also Report examples which will be given after performing analysis and the summary report are attached for reference.

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
- **Gemini 2.0 Flash**: Advanced AI analysis
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
python main_updated.py --data-file path/to/your/data.json
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
- `/ai_analysis` - AI analysis results page

#### API Endpoints
- `POST /api/save_basics` - Save basic information
- `POST /api/save_additional` - Save lifestyle information
- `POST /api/save_family` - Save family information
- `POST /api/save_finances` - Save financial information
- `POST /api/save_coverage` - Save coverage information
- `POST /api/save_medical` - Save medical information
- `POST /api/save_preferences` - Save preferences
- `GET /api/get_all_data` - Get all saved data
- `GET /api/get_ai_analysis` - Get AI analysis results
- `POST /api/generate_pdf` - Generate PDF report
- `POST /api/download_ai_analysis_pdf` - Download AI analysis PDF
- `POST /api/clear_session` - Clear session data

## 📊 Risk Assessment System

### Scoring Categories (100-Point Scale)

1. **Personal Information (5 points)**
   - Age factor: 0-3 points
   - Marital status: 0-1 points
   - Location tier: 0-1 points

2. **Lifestyle & Behavior (8 points)**
   - Occupation risk: 0-2 points
   - Working type: 0-2 points
   - Daily steps: 0-2 points
   - Sleep hours: 0-2 points
   - BMI: 0-2 points
   - Smoking: 0-3 points
   - Alcohol consumption: 0-2 points
   - Commute type: 0-1 points

3. **Financial Information (8 points)**
   - Employment status: 0-2 points
   - CTC (Cost to Company): 0-2 points
   - Disposable income: 0-2 points
   - EMI load: 0-2 points

4. **Medical Information (8 points)**
   - Pre-existing conditions: 0-2 points
   - BMI (from lifestyle): 0-2 points
   - Family medical history: 0-2 points
   - Recent hospitalizations: 0-2 points

5. **Preferences & Risk Appetite (4 points)**
   - Risk tolerance: 0-2 points
   - Budget constraints: 0-2 points

6. **Dependents Information (6 points)**
   - Number of dependents: 0-3 points
   - Dependent ages: 0-3 points

7. **Insurance History (4 points)**
   - Existing policies: 0-2 points
   - Claims history: 0-2 points

8. **Coverage Summary (3 points)**
   - Coverage adequacy: 0-3 points

### Risk Levels
- **Very Low (0-20)**: A+ Rating, ₹15L coverage, ₹250 premium
- **Low (21-35)**: A Rating, ₹12L coverage, ₹350 premium
- **Moderate (36-50)**: B Rating, ₹10L coverage, ₹500 premium
- **High (51-70)**: C Rating, ₹7.5L coverage, ₹750 premium
- **Very High (71-100)**: D Rating, ₹5L coverage, ₹1,200 premium

## 🤖 AI Integration

### Gemini 2.0 Flash Analysis
The system uses Gemini 2.0 Flash for advanced analysis:

```python
from main_updated import analyze_with_gemini

# Analyze data with AI
ai_analysis = analyze_with_gemini(client_data)
```

### AI Analysis Output
The AI provides:
- **Detailed Analysis**: Age, occupation, lifestyle, medical, and financial factors
- **Risk Factors**: Specific risk factors and their impact
- **Positive Indicators**: Beneficial factors from the client's profile
- **Areas of Concern**: Specific concerns and additional requirements
- **Recommendations**: Policy recommendations, coverage amounts, medical requirements
- **Conclusion**: Personalized risk profile and next steps

## 📁 Project Structure

```
UnderwriterRisk-Calc/
├── app.py                 # Flask web application
├── main_updated.py        # AI analysis module
├── scoring_functions.py   # Risk scoring calculations
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── landing.html
│   ├── basics.html
│   ├── additional.html
│   ├── familydetails.html
│   ├── finances.html
│   ├── coverage.html
│   ├── medical.html
│   ├── preferences.html
│   ├── summary.html
│   ├── ai_analysis.html
│   └── index.html
├── static/               # CSS and static files
│   ├── base.css
│   ├── landing.css
│   ├── styles.css
│   └── forms.css
├── reports/              # Generated reports (created automatically)
└── venv/                # Virtual environment
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
- Modify risk scoring weights in `scoring_functions.py`
- Adjust AI prompts in `main_updated.py`
- Customize PDF templates in `app.py`
- Update form fields in HTML templates

## 📈 Data Flow

1. **Data Collection**: Multi-step form system collects comprehensive information
2. **Data Storage**: Information saved to server session
3. **Risk Calculation**: 100-point scoring system applied using `scoring_functions.py`
4. **AI Analysis**: Data sent to Gemini 2.0 Flash for advanced analysis via `main_updated.py`
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

**Built with ❤️ using Flask, Gemini 2.0 Flash, and modern web technologies** 
