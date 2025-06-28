#!/usr/bin/env python3
"""
Main.py - Data Collection and AI Integration for Underwriting Risk Assessment
Collects all form data and integrates with Gemini 2.0 Flash for AI analysis
"""

import json
import os
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Gemini AI imports
from google import genai
from google.genai import types


os.environ["GEMINI_API_KEY"] = "AIzaSyDIQVQ4a-n_cUxrUXJ5KAAng4diA9SL8Xkasdfghkckmlkm"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UnderwritingDataCollector:
    """Collects and structures underwriting data into comprehensive JSON format"""
    
    def __init__(self):
        """Initialize the data collector"""
        self.reports_dir = 'reports'
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def collect_all_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect and structure all form data into a comprehensive JSON format
        
        Args:
            session_data: Data from Flask session or any data source
            
        Returns:
            Structured JSON data ready for AI analysis
        """
        try:
            # Extract data from session
            basic_info = session_data.get('basic_info', {})
            additional_info = session_data.get('additional_info', {})
            family_info = session_data.get('family_info', {})
            financial_info = session_data.get('financial_info', {})
            coverage_info = session_data.get('coverage_info', {})
            medical_info = session_data.get('medical_info', {})
            preferences_info = session_data.get('preferences_info', {})
            
            # Calculate derived metrics
            calculated_metrics = self._calculate_derived_metrics(basic_info, medical_info, financial_info)
            
            # Structure comprehensive data for Gemini AI
            comprehensive_data = {
                "client_id": f"CL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "personal_information": {
                    "name": basic_info.get('fullName', ''),
                    "age": calculated_metrics.get('age', basic_info.get('age')),
                    "gender": basic_info.get('gender', ''),
                    "marital_status": basic_info.get('maritalStatus', ''),
                    "location": {
                        "city": basic_info.get('city', ''),
                        "state": basic_info.get('state', ''),
                        "tier": self._determine_location_tier(basic_info.get('city', ''))
                    }
                },
                "lifestyle_and_behavior": {
                    "occupation": additional_info.get('occupation', ''),
                    "working_type": additional_info.get('workingType', ''),
                    "daily_steps": additional_info.get('steps_per_day', 0),
                    "sleep_hours": additional_info.get('sleepHours', ''),
                    "bmi": calculated_metrics.get('bmi'),
                    "is_smoker": additional_info.get('smoker') == 'yes',
                    "alcohol_consumption": additional_info.get('alcohol', ''),
                    "commute_type": additional_info.get('commuteType', '')
                },
                "financial_information": {
                    "employment_status": financial_info.get('employmentStatus', ''),
                    "ctc_annual_lakhs": self._convert_to_lakhs(financial_info.get('totalCTC', 0)),
                    "disposable_income_percent": self._calculate_disposable_percentage(financial_info),
                    "emi_load_percent_of_income": self._calculate_emi_percentage(financial_info)
                },
                "medical_information": {
                    "pre_existing_conditions": self._parse_medical_conditions(medical_info.get('preExistingConditions', '')),
                    "last_health_checkup_months_ago": self._calculate_months_since_checkup(medical_info.get('lastHealthCheckup', '')),
                    "allergies": self._parse_allergies(medical_info.get('allergies', ''))
                },
                "preferences_and_risk_appetite": {
                    "budget_flexibility": preferences_info.get('deductibleFlexibility', ''),
                    "riders_willingness": preferences_info.get('willingnessForRiders') == 'yes',
                    "deductible_flexibility": preferences_info.get('deductibleFlexibility') != 'no',
                    "risk_tolerance": preferences_info.get('riskTolerance', '')
                },
                "dependents_information": {
                    "count": family_info.get('numDependents', 0),
                    "dependents": family_info.get('dependents', [])
                },
                "insurance_history": {
                    "has_life_insurance": len(coverage_info.get('existingLifePolicies', [])) > 0,
                    "has_health_insurance": len(coverage_info.get('existingHealthPolicies', [])) > 0,
                    "claim_history_last_5_yrs": len(coverage_info.get('claimHistory', [])),
                    "policy_lapse_history": len(coverage_info.get('policyLapseHistory', [])) > 0
                },
                "coverage_summary": {
                    "life_coverage_multiple_of_income": self._calculate_life_coverage_multiple(financial_info, coverage_info),
                    "health_coverage_lakhs": self._convert_to_lakhs(coverage_info.get('totalHealthCoverage', 0))
                }
            }
            
            logger.info(f"Data collected successfully. Client ID: {comprehensive_data['client_id']}")
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Error collecting data: {str(e)}")
            raise
    
    def _calculate_derived_metrics(self, basic_info: Dict, medical_info: Dict, financial_info: Dict) -> Dict[str, Any]:
        """Calculate derived metrics from raw data"""
        metrics = {}
        
        # Calculate age from DOB if available
        if basic_info.get('dob'):
            try:
                dob = datetime.strptime(basic_info['dob'], '%Y-%m-%d')
                metrics['age'] = datetime.now().year - dob.year
            except:
                metrics['age'] = basic_info.get('age')
        else:
            metrics['age'] = basic_info.get('age')
        
        # Calculate BMI if height and weight are available
        if medical_info.get('height') and medical_info.get('weight'):
            try:
                height_m = float(medical_info['height']) / 100
                weight_kg = float(medical_info['weight'])
                bmi = weight_kg / (height_m * height_m)
                metrics['bmi'] = round(bmi, 1)
            except:
                metrics['bmi'] = medical_info.get('bmi')
        else:
            metrics['bmi'] = medical_info.get('bmi')
        
        return metrics
    
    def _determine_location_tier(self, city: str) -> str:
        """Determine location tier based on city"""
        metro_cities = ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'ahmedabad']
        tier2_cities = ['nagpur', 'indore', 'bhopal', 'lucknow', 'kanpur', 'patna', 'chandigarh', 'amritsar']
        
        city_lower = city.lower()
        if city_lower in metro_cities:
            return "Metro"
        elif city_lower in tier2_cities:
            return "Tier-2 City"
        else:
            return "Rural"
    
    def _convert_to_lakhs(self, amount: float) -> float:
        """Convert amount to lakhs"""
        return round(amount / 100000, 1)
    
    def _calculate_disposable_percentage(self, financial_info: Dict) -> float:
        """Calculate disposable income percentage"""
        try:
            monthly_salary = float(financial_info.get('monthlySalary', 0))
            monthly_expenses = float(financial_info.get('monthlyExpenses', 0))
            existing_emis = float(financial_info.get('existingEMIs', 0))
            bnpl_obligations = float(financial_info.get('bnplObligations', 0))
            
            total_obligations = monthly_expenses + existing_emis + bnpl_obligations
            if monthly_salary > 0:
                disposable_percentage = ((monthly_salary - total_obligations) / monthly_salary) * 100
                return max(0, round(disposable_percentage, 1))
            return 0
        except:
            return 0
    
    def _calculate_emi_percentage(self, financial_info: Dict) -> float:
        """Calculate EMI load percentage of income"""
        try:
            monthly_salary = float(financial_info.get('monthlySalary', 0))
            existing_emis = float(financial_info.get('existingEMIs', 0))
            bnpl_obligations = float(financial_info.get('bnplObligations', 0))
            
            total_emi = existing_emis + bnpl_obligations
            if monthly_salary > 0:
                emi_percentage = (total_emi / monthly_salary) * 100
                return round(emi_percentage, 1)
            return 0
        except:
            return 0
    
    def _parse_medical_conditions(self, conditions: str) -> List[str]:
        """Parse medical conditions into list"""
        if not conditions or conditions.lower() in ['none', 'no', '']:
            return []
        return [conditions]
    
    def _calculate_months_since_checkup(self, checkup_date: str) -> int:
        """Calculate months since last health checkup"""
        if not checkup_date:
            return 36  # Default to 3 years if no date provided
        try:
            checkup = datetime.strptime(checkup_date, '%Y-%m-%d')
            months_diff = (datetime.now() - checkup).days / 30
            return int(months_diff)
        except:
            return 36
    
    def _parse_allergies(self, allergies: str) -> List[str]:
        """Parse allergies into list"""
        if not allergies or allergies.lower() in ['none', 'no', '']:
            return []
        return [allergies]
    
    def _calculate_life_coverage_multiple(self, financial_info: Dict, coverage_info: Dict) -> float:
        """Calculate life coverage as multiple of annual income"""
        try:
            annual_income = float(financial_info.get('totalCTC', 0))
            life_coverage = float(coverage_info.get('totalLifeCoverage', 0))
            
            if annual_income > 0:
                multiple = life_coverage / annual_income
                return round(multiple, 1)
            return 0
        except:
            return 0
    
    def save_json_data(self, data: Dict[str, Any], filename: str = None) -> str:
        """
        Save the structured data to a JSON file
        
        Args:
            data: Structured application data
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"underwriting_data_{timestamp}.json"
            
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data saved to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise

# ============================================================================
# SCORING CALCULATION
# ============================================================================

def calculate_detailed_scoring(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate detailed scoring breakdown based on the methodology
    
    Args:
        data: Structured client data
        
    Returns:
        Detailed scoring breakdown
    """
    scoring = {
        "personal_information": {"score": 0, "max": 5, "breakdown": {}},
        "lifestyle_behavior": {"score": 0, "max": 8, "breakdown": {}},
        "financial_information": {"score": 0, "max": 8, "breakdown": {}},
        "medical_information": {"score": 0, "max": 8, "breakdown": {}},
        "preferences_risk_appetite": {"score": 0, "max": 4, "breakdown": {}},
        "dependents_information": {"score": 0, "max": 6, "breakdown": {}},
        "insurance_history": {"score": 0, "max": 4, "breakdown": {}},
        "coverage_summary": {"score": 0, "max": 3, "breakdown": {}}
    }
    
    # I. Personal Information (Max 5 Points)
    personal = data.get('personal_information', {})
    age = personal.get('age', 0)
    
    if age < 30:
        scoring["personal_information"]["breakdown"]["age"] = 1
    elif age < 50:
        scoring["personal_information"]["breakdown"]["age"] = 2
    else:
        scoring["personal_information"]["breakdown"]["age"] = 3
    
    scoring["personal_information"]["breakdown"]["gender"] = 0  # All → 0
    
    marital_status = personal.get('marital_status', '').lower()
    if marital_status == 'single':
        scoring["personal_information"]["breakdown"]["marital_status"] = 1
    else:
        scoring["personal_information"]["breakdown"]["marital_status"] = 0
    
    location_tier = personal.get('location', {}).get('tier', '')
    if location_tier == 'Metro':
        scoring["personal_information"]["breakdown"]["location_tier"] = 1
    elif location_tier == 'Tier-2 City':
        scoring["personal_information"]["breakdown"]["location_tier"] = 0.5
    else:
        scoring["personal_information"]["breakdown"]["location_tier"] = 0
    
    scoring["personal_information"]["score"] = sum(scoring["personal_information"]["breakdown"].values())
    
    # II. Lifestyle & Behavior (Max 8 Points)
    lifestyle = data.get('lifestyle_and_behavior', {})
    occupation = lifestyle.get('occupation', '').lower()
    
    if any(job in occupation for job in ['driver', 'construction', 'delivery', 'miner', 'pilot', 'firefighter', 'police']):
        scoring["lifestyle_behavior"]["breakdown"]["occupation"] = 2
    elif any(job in occupation for job in ['field', 'onsite', 'sales']):
        scoring["lifestyle_behavior"]["breakdown"]["occupation"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["occupation"] = 0
    
    working_type = lifestyle.get('working_type', '').lower()
    if 'hazardous' in working_type:
        scoring["lifestyle_behavior"]["breakdown"]["working_type"] = 2
    elif 'onsite' in working_type:
        scoring["lifestyle_behavior"]["breakdown"]["working_type"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["working_type"] = 0
    
    daily_steps = lifestyle.get('daily_steps', 0)
    if daily_steps < 5000:
        scoring["lifestyle_behavior"]["breakdown"]["daily_steps"] = 2
    elif daily_steps < 10000:
        scoring["lifestyle_behavior"]["breakdown"]["daily_steps"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["daily_steps"] = 0
    
    sleep_hours = lifestyle.get('sleep_hours', '')
    if '7' in sleep_hours or '8' in sleep_hours:
        scoring["lifestyle_behavior"]["breakdown"]["sleep_hours"] = 0
    elif '5' in sleep_hours or '6' in sleep_hours:
        scoring["lifestyle_behavior"]["breakdown"]["sleep_hours"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["sleep_hours"] = 2
    
    bmi = lifestyle.get('bmi', 0)
    if 18.5 <= bmi <= 24.9:
        scoring["lifestyle_behavior"]["breakdown"]["bmi"] = 0
    elif 25 <= bmi <= 29.9:
        scoring["lifestyle_behavior"]["breakdown"]["bmi"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["bmi"] = 2
    
    if lifestyle.get('is_smoker', False):
        scoring["lifestyle_behavior"]["breakdown"]["smoker"] = 3
    else:
        scoring["lifestyle_behavior"]["breakdown"]["smoker"] = 0
    
    alcohol = lifestyle.get('alcohol_consumption', '').lower()
    if 'daily' in alcohol:
        scoring["lifestyle_behavior"]["breakdown"]["alcohol"] = 2
    elif 'occasionally' in alcohol:
        scoring["lifestyle_behavior"]["breakdown"]["alcohol"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["alcohol"] = 0
    
    commute = lifestyle.get('commute_type', '').lower()
    if 'heavy' in commute or 'truck' in commute:
        scoring["lifestyle_behavior"]["breakdown"]["commute"] = 2
    elif 'bike' in commute or 'motorcycle' in commute:
        scoring["lifestyle_behavior"]["breakdown"]["commute"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["commute"] = 0
    
    scoring["lifestyle_behavior"]["score"] = sum(scoring["lifestyle_behavior"]["breakdown"].values())
    
    # III. Financial Information (Max 8 Points)
    financial = data.get('financial_information', {})
    employment = financial.get('employment_status', '').lower()
    
    if employment == 'unemployed':
        scoring["financial_information"]["breakdown"]["employment_status"] = 2
    elif employment in ['freelancer', 'seasonal']:
        scoring["financial_information"]["breakdown"]["employment_status"] = 1
    else:
        scoring["financial_information"]["breakdown"]["employment_status"] = 0
    
    ctc = financial.get('ctc_annual_lakhs', 0)
    if ctc >= 10:
        scoring["financial_information"]["breakdown"]["ctc"] = 0
    elif ctc >= 5:
        scoring["financial_information"]["breakdown"]["ctc"] = 1
    else:
        scoring["financial_information"]["breakdown"]["ctc"] = 2
    
    disposable = financial.get('disposable_income_percent', 0)
    if disposable >= 30:
        scoring["financial_information"]["breakdown"]["disposable_income"] = 0
    elif disposable >= 15:
        scoring["financial_information"]["breakdown"]["disposable_income"] = 1
    else:
        scoring["financial_information"]["breakdown"]["disposable_income"] = 2
    
    emi_load = financial.get('emi_load_percent_of_income', 0)
    if emi_load < 30:
        scoring["financial_information"]["breakdown"]["emi_load"] = 0
    elif emi_load <= 50:
        scoring["financial_information"]["breakdown"]["emi_load"] = 1
    else:
        scoring["financial_information"]["breakdown"]["emi_load"] = 2
    
    scoring["financial_information"]["score"] = sum(scoring["financial_information"]["breakdown"].values())
    
    # IV. Medical Information (Max 8 Points)
    medical = data.get('medical_information', {})
    conditions = medical.get('pre_existing_conditions', [])
    
    if not conditions:
        scoring["medical_information"]["breakdown"]["pre_existing_conditions"] = 0
    elif any('diabetes' in cond.lower() or 'heart' in cond.lower() for cond in conditions):
        scoring["medical_information"]["breakdown"]["pre_existing_conditions"] = 2
    else:
        scoring["medical_information"]["breakdown"]["pre_existing_conditions"] = 1
    
    # BMI is already calculated in lifestyle section
    scoring["medical_information"]["breakdown"]["bmi"] = scoring["lifestyle_behavior"]["breakdown"]["bmi"]
    
    checkup_months = medical.get('last_health_checkup_months_ago', 36)
    if checkup_months < 12:
        scoring["medical_information"]["breakdown"]["health_checkup"] = 0
    elif checkup_months <= 36:
        scoring["medical_information"]["breakdown"]["health_checkup"] = 1
    else:
        scoring["medical_information"]["breakdown"]["health_checkup"] = 2
    
    allergies = medical.get('allergies', [])
    if not allergies:
        scoring["medical_information"]["breakdown"]["allergies"] = 0
    elif len(allergies) > 1:
        scoring["medical_information"]["breakdown"]["allergies"] = 1
    else:
        scoring["medical_information"]["breakdown"]["allergies"] = 0.5
    
    scoring["medical_information"]["score"] = sum(scoring["medical_information"]["breakdown"].values())
    
    # V. Preferences & Risk Appetite (Max 4 Points)
    preferences = data.get('preferences_and_risk_appetite', {})
    budget_flex = preferences.get('budget_flexibility', '').lower()
    
    if 'high' in budget_flex:
        scoring["preferences_risk_appetite"]["breakdown"]["budget_flexibility"] = 0
    elif 'moderate' in budget_flex:
        scoring["preferences_risk_appetite"]["breakdown"]["budget_flexibility"] = 0.5
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["budget_flexibility"] = 1
    
    if preferences.get('riders_willingness', False):
        scoring["preferences_risk_appetite"]["breakdown"]["riders_willingness"] = 0
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["riders_willingness"] = 1
    
    if preferences.get('deductible_flexibility', True):
        scoring["preferences_risk_appetite"]["breakdown"]["deductible_flexibility"] = 0
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["deductible_flexibility"] = 1
    
    risk_tolerance = preferences.get('risk_tolerance', '').lower()
    if 'conservative' in risk_tolerance:
        scoring["preferences_risk_appetite"]["breakdown"]["risk_tolerance"] = 0
    elif 'moderate' in risk_tolerance:
        scoring["preferences_risk_appetite"]["breakdown"]["risk_tolerance"] = 0.5
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["risk_tolerance"] = 1
    
    scoring["preferences_risk_appetite"]["score"] = sum(scoring["preferences_risk_appetite"]["breakdown"].values())
    
    # VI. Dependents Information (Max 6 Points)
    dependents = data.get('dependents_information', {})
    dep_count = dependents.get('count', 0)
    
    if dep_count == 0:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 0
    elif dep_count <= 2:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 1
    elif dep_count <= 4:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 2
    else:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 3
    
    # Calculate dependency level (simplified)
    dependency_score = 0
    for dep in dependents.get('dependents', []):
        if dep.get('age', 0) >= 60:
            dependency_score += 0.5
    
    scoring["dependents_information"]["breakdown"]["age_risk_dependents"] = min(dependency_score, 1.5)
    scoring["dependents_information"]["score"] = sum(scoring["dependents_information"]["breakdown"].values())
    
    # VII. Insurance History (Max 4 Points)
    insurance = data.get('insurance_history', {})
    
    if not insurance.get('has_life_insurance', False):
        scoring["insurance_history"]["breakdown"]["life_insurance"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["life_insurance"] = 0
    
    if not insurance.get('has_health_insurance', False):
        scoring["insurance_history"]["breakdown"]["health_insurance"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["health_insurance"] = 0
    
    claims = insurance.get('claim_history_last_5_yrs', 0)
    if claims == 0:
        scoring["insurance_history"]["breakdown"]["claim_history"] = 0
    elif claims <= 2:
        scoring["insurance_history"]["breakdown"]["claim_history"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["claim_history"] = 2
    
    if insurance.get('policy_lapse_history', False):
        scoring["insurance_history"]["breakdown"]["policy_lapse"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["policy_lapse"] = 0
    
    scoring["insurance_history"]["score"] = sum(scoring["insurance_history"]["breakdown"].values())
    
    # VIII. Coverage Summary (Max 3 Points)
    coverage = data.get('coverage_summary', {})
    life_multiple = coverage.get('life_coverage_multiple_of_income', 0)
    
    if life_multiple >= 10:
        scoring["coverage_summary"]["breakdown"]["life_coverage"] = 0
    elif life_multiple >= 5:
        scoring["coverage_summary"]["breakdown"]["life_coverage"] = 1
    else:
        scoring["coverage_summary"]["breakdown"]["life_coverage"] = 2
    
    health_coverage = coverage.get('health_coverage_lakhs', 0)
    if health_coverage >= 5:
        scoring["coverage_summary"]["breakdown"]["health_coverage"] = 0
    elif health_coverage >= 2:
        scoring["coverage_summary"]["breakdown"]["health_coverage"] = 0.5
    else:
        scoring["coverage_summary"]["breakdown"]["health_coverage"] = 1
    
    scoring["coverage_summary"]["score"] = sum(scoring["coverage_summary"]["breakdown"].values())
    
    # Calculate total score
    total_score = sum(category["score"] for category in scoring.values())
    max_possible_score = sum(category["max"] for category in scoring.values())
    
    return {
        "detailed_scoring": scoring,
        "total_score": total_score,
        "max_possible_score": max_possible_score,
        "risk_percentage": round((total_score / max_possible_score) * 100, 1)
    }

def determine_risk_class(risk_percentage: float) -> Dict[str, Any]:
    """Determine risk class based on percentage"""
    if risk_percentage <= 20:
        return {
            "class": "Very Low Risk",
            "rating": "A+",
            "description": "Excellent risk profile with minimal underwriting considerations",
            "recommended_cover": "₹15L",
            "suggested_premium": "₹250/month",
            "favorable": True
        }
    elif risk_percentage <= 40:
        return {
            "class": "Low Risk",
            "rating": "A",
            "description": "Good risk profile with standard underwriting considerations",
            "recommended_cover": "₹12L",
            "suggested_premium": "₹350/month",
            "favorable": True
        }
    elif risk_percentage <= 60:
        return {
            "class": "Moderate Risk",
            "rating": "B",
            "description": "Standard risk profile with moderate underwriting considerations",
            "recommended_cover": "₹10L",
            "suggested_premium": "₹500/month",
            "favorable": True
        }
    elif risk_percentage <= 80:
        return {
            "class": "High Risk",
            "rating": "C",
            "description": "Higher risk profile requiring detailed underwriting review",
            "recommended_cover": "₹7.5L",
            "suggested_premium": "₹750/month",
            "favorable": False
        }
    else:
        return {
            "class": "Very High Risk",
            "rating": "D",
            "description": "High-risk profile requiring specialized underwriting and medical review",
            "recommended_cover": "₹5L",
            "suggested_premium": "₹1,200/month",
            "favorable": False
        }

# ============================================================================
# GEMINI AI INTEGRATION
# ============================================================================

def analyze_with_gemini(data: Dict[str, Any]) -> str:
    """
    Analyze data using Gemini 2.0 Flash AI model
    
    Args:
        data: Structured JSON data from UnderwritingDataCollector
        
    Returns:
        AI analysis result as string
    """
    try:
        # Initialize Gemini client
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        
        model = "gemini-2.0-flash"
        
        # Convert data to JSON string
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="""Analyze this underwriting data and provide key insights about the client's risk profile. Focus on:

1. Key risk factors and their impact
2. Positive indicators in the profile
3. Areas of concern that need attention
4. Overall assessment of insurability
5. Specific recommendations for risk mitigation

Provide a concise analysis in 3-4 paragraphs focusing on the most important insights."""),
                ],
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=json_data),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )
        
        logger.info("Starting Gemini AI analysis...")
        
        # Collect all chunks
        full_response = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            full_response += chunk.text
        
        logger.info("Gemini AI analysis completed successfully")
        return full_response
        
    except Exception as e:
        logger.error(f"Error in Gemini AI analysis: {str(e)}")
        return "AI analysis not available due to configuration issues."

def generate_comprehensive_report(data: Dict[str, Any], scoring_results: Dict[str, Any], ai_insights: str) -> Dict[str, Any]:
    """
    Generate a comprehensive report combining data, scoring, and AI analysis
    
    Args:
        data: Original application data
        scoring_results: Detailed scoring results
        ai_insights: AI analysis results as string
        
    Returns:
        Comprehensive report
    """
    try:
        risk_class = determine_risk_class(scoring_results["risk_percentage"])
        
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_id": f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "ai_model": "Gemini 2.0 Flash",
                "version": "1.0"
            },
            "client_summary": {
                "client_id": data.get('client_id', 'N/A'),
                "name": data.get('personal_information', {}).get('name', 'N/A'),
                "age": data.get('personal_information', {}).get('age', 'N/A'),
                "occupation": data.get('lifestyle_and_behavior', {}).get('occupation', 'N/A'),
                "employment_status": data.get('financial_information', {}).get('employment_status', 'N/A'),
                "annual_income_lakhs": data.get('financial_information', {}).get('ctc_annual_lakhs', 'N/A')
            },
            "risk_assessment": {
                "total_score": scoring_results["total_score"],
                "max_possible_score": scoring_results["max_possible_score"],
                "risk_percentage": scoring_results["risk_percentage"],
                "risk_class": risk_class["class"],
                "risk_rating": risk_class["rating"],
                "favorable_profile": risk_class["favorable"],
                "recommended_cover": risk_class["recommended_cover"],
                "suggested_premium": risk_class["suggested_premium"]
            },
            "detailed_scoring": scoring_results["detailed_scoring"],
            "ai_insights": ai_insights,
            "original_data": data
        }
        
        logger.info(f"Comprehensive report generated. Report ID: {report['report_metadata']['report_id']}")
        return report
        
    except Exception as e:
        logger.error(f"Error generating comprehensive report: {str(e)}")
        raise

# ============================================================================
# MAIN FUNCTION AND EXAMPLE USAGE
# ============================================================================

def main():
    """Main function to demonstrate the complete workflow"""
    try:
        # Initialize the data collector
        collector = UnderwritingDataCollector()
        
        # Example usage with sample data
        sample_session_data = {
            'basic_info': {
                'fullName': 'John Doe',
                'age': 35,
                'dob': '1989-05-15',
                'gender': 'male',
                'email': 'john.doe@example.com',
                'phone': '9876543210',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'maritalStatus': 'married'
            },
            'additional_info': {
                'occupation': 'Software Engineer',
                'workingType': 'Remote job',
                'steps_per_day': 8000,
                'smoker': 'no',
                'alcohol': 'Occasionally',
                'bmi': 24.5,
                'sleepHours': '7-8 hours',
                'commuteType': 'Work from home'
            },
            'family_info': {
                'numDependents': 2,
                'familyMedicalHistory': ['diabetes', 'hypertension'],
                'dependents': [
                    {'relationship': 'Spouse', 'age': 32, 'gender': 'female', 'financialDependency': 'yes'},
                    {'relationship': 'Child', 'age': 5, 'gender': 'male', 'financialDependency': 'yes'}
                ]
            },
            'financial_info': {
                'employmentStatus': 'salaried',
                'companyName': 'Tech Corp',
                'totalCTC': 1200000,
                'monthlySalary': 73000,
                'incomeStability': 'high',
                'yearsOfExperience': 8,
                'existingEMIs': 15000,
                'monthlyExpenses': 35000,
                'disposableIncome': 23000
            },
            'coverage_info': {
                'existingLifePolicies': [
                    {'policyType': 'Term', 'sumAssured': 500000, 'premium': 3000}
                ],
                'existingHealthPolicies': [
                    {'policyType': 'Individual', 'sumAssured': 300000, 'premium': 5000}
                ],
                'totalLifeCoverage': 500000,
                'totalHealthCoverage': 300000,
                'claimHistory': [],
                'policyLapseHistory': []
            },
            'medical_info': {
                'height': 175,
                'weight': 75,
                'preExistingConditions': 'None',
                'hasHospitalizations': 'no',
                'currentMedications': [],
                'allergies': 'None',
                'recentHospitalizations': [],
                'lastHealthCheckup': '2024-01-15'
            },
            'preferences_info': {
                'premiumBudget': 5000,
                'primaryInterest': 'health_insurance',
                'willingnessForRiders': 'yes',
                'deductibleFlexibility': 'moderate',
                'longTermGoals': ['retirement', 'child_education'],
                'riskTolerance': 'moderate',
                'investmentHorizon': '10-15 years',
                'financialGoals': ['wealth_creation', 'tax_savings']
            }
        }
        
        # Collect and structure data
        structured_data = collector.collect_all_data(sample_session_data)
        
        # Calculate detailed scoring
        scoring_results = calculate_detailed_scoring(structured_data)
        
        # Save data
        data_filepath = collector.save_json_data(structured_data)
        
        print("=" * 60)
        print("📊 DATA COLLECTION COMPLETED")
        print("=" * 60)
        print(f"✅ Data saved to: {data_filepath}")
        print(f"📋 Client ID: {structured_data['client_id']}")
        print(f"👤 Applicant: {structured_data['personal_information']['name']}")
        print(f"🎯 Age: {structured_data['personal_information']['age']}")
        print(f"💼 Occupation: {structured_data['lifestyle_and_behavior']['occupation']}")
        print(f"💰 Annual Income: {structured_data['financial_information']['ctc_annual_lakhs']}L")
        
        print("\n" + "=" * 60)
        print("📊 DETAILED SCORING BREAKDOWN")
        print("=" * 60)
        
        # Display scoring breakdown
        for category, details in scoring_results["detailed_scoring"].items():
            category_name = category.replace("_", " ").title()
            print(f"\n{category_name}: {details['score']}/{details['max']} points")
            for factor, score in details['breakdown'].items():
                factor_name = factor.replace("_", " ").title()
                print(f"  • {factor_name}: {score} points")
        
        print(f"\n📊 TOTAL SCORE: {scoring_results['total_score']}/{scoring_results['max_possible_score']}")
        print(f"📊 RISK PERCENTAGE: {scoring_results['risk_percentage']}%")
        
        # Determine risk class
        risk_class = determine_risk_class(scoring_results["risk_percentage"])
        
        print("\n" + "=" * 60)
        print("🎯 RISK ASSESSMENT SUMMARY")
        print("=" * 60)
        print(f"Risk Class: {risk_class['class']}")
        print(f"Risk Rating: {risk_class['rating']}")
        print(f"Favorable Profile: {'✅ YES' if risk_class['favorable'] else '❌ NO'}")
        print(f"Recommended Cover: {risk_class['recommended_cover']}")
        print(f"Suggested Premium: {risk_class['suggested_premium']}")
        print(f"Description: {risk_class['description']}")
        
        print("\n" + "=" * 60)
        print("🤖 AI INSIGHTS")
        print("=" * 60)
        
        # Perform AI analysis
        ai_insights = analyze_with_gemini(structured_data)
        
        # Generate comprehensive report
        comprehensive_report = generate_comprehensive_report(structured_data, scoring_results, ai_insights)
        
        # Save report
        report_filepath = collector.save_json_data(comprehensive_report, f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        print(f"✅ AI Analysis completed!")
        print(f"📄 Report saved to: {report_filepath}")
        print("\n" + "=" * 60)
        print("📋 AI INSIGHTS")
        print("=" * 60)
        print(ai_insights)
        
        print("\n" + "=" * 60)
        print("🎯 FINAL CONCLUSION")
        print("=" * 60)
        print(f"Client: {structured_data['personal_information']['name']}")
        print(f"Risk Score: {scoring_results['total_score']}/{scoring_results['max_possible_score']} ({scoring_results['risk_percentage']}%)")
        print(f"Risk Class: {risk_class['class']} ({risk_class['rating']})")
        print(f"Profile Assessment: {'✅ FAVORABLE' if risk_class['favorable'] else '❌ UNFAVORABLE'}")
        print(f"Recommendation: {risk_class['recommended_cover']} coverage at {risk_class['suggested_premium']}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
