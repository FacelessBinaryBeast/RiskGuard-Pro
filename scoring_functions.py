#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scoring Functions for Underwriting Risk Assessment
Calculates detailed scoring breakdown based on the methodology
"""

def calculate_detailed_scoring(data: dict) -> dict:
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
    personal = data.get('basic_info', {})
    age = personal.get('age', 0)
    
    if age < 30:
        scoring["personal_information"]["breakdown"]["age"] = 1
    elif age < 50:
        scoring["personal_information"]["breakdown"]["age"] = 2
    else:
        scoring["personal_information"]["breakdown"]["age"] = 3
    
    scoring["personal_information"]["breakdown"]["gender"] = 0  # All → 0
    
    marital_status = personal.get('maritalStatus', '').lower()
    if marital_status == 'single':
        scoring["personal_information"]["breakdown"]["marital_status"] = 1
    else:
        scoring["personal_information"]["breakdown"]["marital_status"] = 0
    
    # Derive location tier from city/state
    city = personal.get('city', '').lower()
    state = personal.get('state', '').lower()
    
    # Metro cities
    metro_cities = ['mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'pune', 'ahmedabad', 'surat', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'indore', 'thane', 'bhopal', 'visakhapatnam', 'patna', 'vadodara', 'ghaziabad', 'ludhiana', 'agra', 'nashik', 'faridabad', 'meerut', 'rajkot', 'kalyan', 'vasai', 'srinagar', 'aurangabad', 'dhanbad', 'amritsar', 'allahabad', 'ranchi', 'howrah', 'coimbatore', 'jabalpur', 'gwalior', 'vijayawada', 'jodhpur', 'madurai', 'raipur', 'kota', 'guwahati', 'chandigarh', 'solapur', 'hubli', 'bareilly', 'moradabad', 'gurgaon', 'aligarh', 'jalandhar', 'tiruchirappalli', 'bhubaneswar', 'salem', 'warangal', 'mira', 'thiruvananthapuram', 'bhiwandi', 'saharanpur', 'guntur', 'amravati', 'bikaner', 'noida', 'jamshedpur', 'bhilai', 'cuttack', 'firozabad', 'kochi', 'nellore', 'bhavnagar', 'dehradun', 'durgapur', 'asansol', 'rourkela', 'bhagalpur', 'mangalore', 'bellary', 'mysore', 'tiruppur', 'gulbarga', 'bhubaneshwar', 'pimpri', 'panchkula', 'bathinda', 'karnal', 'hisar', 'baramula', 'ambala', 'vapi', 'bhagalpur', 'rohtak', 'firozpur', 'hissar', 'panipat', 'karnal', 'sonipat', 'yamunanagar', 'panchkula', 'ambala', 'kaithal', 'kurukshetra', 'yamunanagar', 'panipat', 'karnal', 'sonipat', 'rohtak', 'bhiwani', 'hisar', 'fatehabad', 'jind', 'sirsa', 'firozpur', 'faridkot', 'moga', 'ludhiana', 'patiala', 'sangrur', 'bathinda', 'muktsar', 'fazilka', 'amritsar', 'tarn taran', 'kapurthala', 'hoshiarpur', 'jalandhar', 'nawanshahr', 'rupnagar', 'sahibzada ajit singh nagar', 'fatehgarh sahib', 'gurdaspur', 'pathankot', 'shahid bhagat singh nagar', 'barnala', 'mansa', 'sangrur', 'bathinda', 'muktsar', 'fazilka', 'amritsar', 'tarn taran', 'kapurthala', 'hoshiarpur', 'jalandhar', 'nawanshahr', 'rupnagar', 'sahibzada ajit singh nagar', 'fatehgarh sahib', 'gurdaspur', 'pathankot', 'shahid bhagat singh nagar', 'barnala', 'mansa']
    
    if city in metro_cities or any(metro in city for metro in ['mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'pune', 'ahmedabad', 'surat', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'indore', 'thane', 'bhopal', 'visakhapatnam', 'patna', 'vadodara', 'ghaziabad', 'ludhiana', 'agra', 'nashik', 'faridabad', 'meerut', 'rajkot', 'kalyan', 'vasai', 'srinagar', 'aurangabad', 'dhanbad', 'amritsar', 'allahabad', 'ranchi', 'howrah', 'coimbatore', 'jabalpur', 'gwalior', 'vijayawada', 'jodhpur', 'madurai', 'raipur', 'kota', 'guwahati', 'chandigarh', 'solapur', 'hubli', 'bareilly', 'moradabad', 'gurgaon', 'aligarh', 'jalandhar', 'tiruchirappalli', 'bhubaneswar', 'salem', 'warangal', 'mira', 'thiruvananthapuram', 'bhiwandi', 'saharanpur', 'guntur', 'amravati', 'bikaner', 'noida', 'jamshedpur', 'bhilai', 'cuttack', 'firozabad', 'kochi', 'nellore', 'bhavnagar', 'dehradun', 'durgapur', 'asansol', 'rourkela', 'bhagalpur', 'mangalore', 'bellary', 'mysore', 'tiruppur', 'gulbarga', 'bhubaneshwar', 'pimpri', 'panchkula', 'bathinda', 'karnal', 'hisar', 'baramula', 'ambala', 'vapi', 'bhagalpur', 'rohtak', 'firozpur', 'hissar', 'panipat', 'karnal', 'sonipat', 'yamunanagar', 'panchkula', 'ambala', 'kaithal', 'kurukshetra', 'yamunanagar', 'panipat', 'karnal', 'sonipat', 'rohtak', 'bhiwani', 'hisar', 'fatehabad', 'jind', 'sirsa', 'firozpur', 'faridkot', 'moga', 'ludhiana', 'patiala', 'sangrur', 'bathinda', 'muktsar', 'fazilka', 'amritsar', 'tarn taran', 'kapurthala', 'hoshiarpur', 'jalandhar', 'nawanshahr', 'rupnagar', 'sahibzada ajit singh nagar', 'fatehgarh sahib', 'gurdaspur', 'pathankot', 'shahid bhagat singh nagar', 'barnala', 'mansa', 'sangrur', 'bathinda', 'muktsar', 'fazilka', 'amritsar', 'tarn taran', 'kapurthala', 'hoshiarpur', 'jalandhar', 'nawanshahr', 'rupnagar', 'sahibzada ajit singh nagar', 'fatehgarh sahib', 'gurdaspur', 'pathankot', 'shahid bhagat singh nagar', 'barnala', 'mansa']):
        scoring["personal_information"]["breakdown"]["location_tier"] = 1
    elif any(tier2 in city for tier2 in ['vadodara', 'lucknow', 'kanpur', 'nagpur', 'indore', 'visakhapatnam', 'patna', 'bhopal', 'ludhiana', 'agra', 'nashik', 'faridabad', 'meerut', 'rajkot', 'aurangabad', 'dhanbad', 'ranchi', 'coimbatore', 'jabalpur', 'gwalior', 'vijayawada', 'jodhpur', 'madurai', 'raipur', 'kota', 'guwahati', 'solapur', 'bareilly', 'moradabad', 'aligarh', 'tiruchirappalli', 'salem', 'warangal', 'bhiwandi', 'saharanpur', 'guntur', 'amravati', 'bikaner', 'jamshedpur', 'bhilai', 'cuttack', 'firozabad', 'nellore', 'bhavnagar', 'dehradun', 'durgapur', 'asansol', 'rourkela', 'bhagalpur', 'mangalore', 'bellary', 'mysore', 'tiruppur', 'gulbarga', 'pimpri', 'bathinda', 'hisar', 'ambala', 'vapi', 'rohtak', 'firozpur', 'panipat', 'sonipat', 'yamunanagar', 'kaithal', 'kurukshetra', 'bhiwani', 'fatehabad', 'jind', 'sirsa', 'faridkot', 'moga', 'patiala', 'sangrur', 'muktsar', 'fazilka', 'tarn taran', 'kapurthala', 'hoshiarpur', 'nawanshahr', 'rupnagar', 'barnala', 'mansa']):
        scoring["personal_information"]["breakdown"]["location_tier"] = 0.5
    else:
        scoring["personal_information"]["breakdown"]["location_tier"] = 0
    
    scoring["personal_information"]["score"] = sum(scoring["personal_information"]["breakdown"].values())
    
    # II. Lifestyle & Behavior (Max 8 Points)
    lifestyle = data.get('additional_info', {})
    occupation = lifestyle.get('occupation', '').lower()
    
    if any(job in occupation for job in ['driver', 'construction', 'delivery', 'miner', 'pilot', 'firefighter', 'police']):
        scoring["lifestyle_behavior"]["breakdown"]["occupation"] = 2
    elif any(job in occupation for job in ['field', 'onsite', 'sales']):
        scoring["lifestyle_behavior"]["breakdown"]["occupation"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["occupation"] = 0
    
    working_type = lifestyle.get('workingType', '').lower()
    if 'hazardous' in working_type or 'driver' in working_type:
        scoring["lifestyle_behavior"]["breakdown"]["working_type"] = 2
    elif 'onsite' in working_type or 'field' in working_type:
        scoring["lifestyle_behavior"]["breakdown"]["working_type"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["working_type"] = 0
    
    daily_steps = lifestyle.get('steps_per_day', 0)
    if daily_steps < 5000:
        scoring["lifestyle_behavior"]["breakdown"]["daily_steps"] = 2
    elif daily_steps < 10000:
        scoring["lifestyle_behavior"]["breakdown"]["daily_steps"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["daily_steps"] = 0
    
    sleep_hours = lifestyle.get('sleep', '')
    if sleep_hours:
        sleep_val = float(sleep_hours)
        if sleep_val >= 7:
            scoring["lifestyle_behavior"]["breakdown"]["sleep_hours"] = 0
        elif sleep_val >= 5:
            scoring["lifestyle_behavior"]["breakdown"]["sleep_hours"] = 1
        else:
            scoring["lifestyle_behavior"]["breakdown"]["sleep_hours"] = 2
    else:
        scoring["lifestyle_behavior"]["breakdown"]["sleep_hours"] = 1  # Default if not provided
    
    bmi = lifestyle.get('bmi', 0)
    if bmi:
        bmi_val = float(bmi)
        if 18.5 <= bmi_val <= 24.9:
            scoring["lifestyle_behavior"]["breakdown"]["bmi"] = 0
        elif 25 <= bmi_val <= 29.9:
            scoring["lifestyle_behavior"]["breakdown"]["bmi"] = 1
        else:
            scoring["lifestyle_behavior"]["breakdown"]["bmi"] = 2
    else:
        scoring["lifestyle_behavior"]["breakdown"]["bmi"] = 1  # Default if not provided
    
    if lifestyle.get('smoker', '') == 'yes':
        scoring["lifestyle_behavior"]["breakdown"]["smoker"] = 3
    else:
        scoring["lifestyle_behavior"]["breakdown"]["smoker"] = 0
    
    alcohol = lifestyle.get('alcohol', '').lower()
    if 'regularly' in alcohol or 'daily' in alcohol:
        scoring["lifestyle_behavior"]["breakdown"]["alcohol"] = 2
    elif 'occasionally' in alcohol:
        scoring["lifestyle_behavior"]["breakdown"]["alcohol"] = 1
    else:
        scoring["lifestyle_behavior"]["breakdown"]["alcohol"] = 0
    
    commute = lifestyle.get('commute', '').lower()
    if 'heavy' in commute or 'truck' in commute or 'bike' in commute:
        scoring["lifestyle_behavior"]["breakdown"]["commute"] = 1
    elif 'car' in commute or 'public' in commute:
        scoring["lifestyle_behavior"]["breakdown"]["commute"] = 0
    else:
        scoring["lifestyle_behavior"]["breakdown"]["commute"] = 0
    
    scoring["lifestyle_behavior"]["score"] = sum(scoring["lifestyle_behavior"]["breakdown"].values())
    
    # III. Financial Information (Max 8 Points)
    financial = data.get('financial_info', {})
    employment = financial.get('employmentStatus', '').lower()
    
    if employment == 'unemployed':
        scoring["financial_information"]["breakdown"]["employment_status"] = 2
    elif employment in ['freelancer', 'business']:
        scoring["financial_information"]["breakdown"]["employment_status"] = 1
    else:
        scoring["financial_information"]["breakdown"]["employment_status"] = 0
    
    ctc = financial.get('totalCTC', 0)
    if ctc >= 1000000:  # 10L
        scoring["financial_information"]["breakdown"]["ctc"] = 0
    elif ctc >= 500000:  # 5L
        scoring["financial_information"]["breakdown"]["ctc"] = 1
    else:
        scoring["financial_information"]["breakdown"]["ctc"] = 2
    
    # Calculate disposable income percentage
    monthly_salary = financial.get('monthlySalary', 0)
    disposable_income = financial.get('disposableIncome', 0)
    
    if monthly_salary > 0:
        disposable_percentage = (disposable_income / monthly_salary) * 100
        if disposable_percentage >= 30:
            scoring["financial_information"]["breakdown"]["disposable_income"] = 0
        elif disposable_percentage >= 15:
            scoring["financial_information"]["breakdown"]["disposable_income"] = 1
        else:
            scoring["financial_information"]["breakdown"]["disposable_income"] = 2
    else:
        scoring["financial_information"]["breakdown"]["disposable_income"] = 2
    
    # Calculate EMI load percentage
    existing_emis = financial.get('existingEMIs', 0)
    if monthly_salary > 0:
        emi_load_percentage = (existing_emis / monthly_salary) * 100
        if emi_load_percentage < 30:
            scoring["financial_information"]["breakdown"]["emi_load"] = 0
        elif emi_load_percentage <= 50:
            scoring["financial_information"]["breakdown"]["emi_load"] = 1
        else:
            scoring["financial_information"]["breakdown"]["emi_load"] = 2
    else:
        scoring["financial_information"]["breakdown"]["emi_load"] = 2
    
    scoring["financial_information"]["score"] = sum(scoring["financial_information"]["breakdown"].values())
    
    # IV. Medical Information (Max 8 Points)
    medical = data.get('medical_info', {})
    conditions = medical.get('preExistingConditions', '')
    
    if not conditions:
        scoring["medical_information"]["breakdown"]["pre_existing_conditions"] = 0
    elif any('diabetes' in conditions.lower() or 'heart' in conditions.lower() or 'cancer' in conditions.lower()):
        scoring["medical_information"]["breakdown"]["pre_existing_conditions"] = 2
    else:
        scoring["medical_information"]["breakdown"]["pre_existing_conditions"] = 1
    
    # BMI is already calculated in lifestyle section
    scoring["medical_information"]["breakdown"]["bmi"] = scoring["lifestyle_behavior"]["breakdown"]["bmi"]
    
    last_checkup = medical.get('lastCheckup', '')
    if last_checkup:
        # Calculate months since last checkup
        from datetime import datetime
        try:
            checkup_date = datetime.strptime(last_checkup, '%Y-%m-%d')
            months_ago = (datetime.now() - checkup_date).days / 30
            if months_ago < 12:
                scoring["medical_information"]["breakdown"]["health_checkup"] = 0
            elif months_ago <= 36:
                scoring["medical_information"]["breakdown"]["health_checkup"] = 1
            else:
                scoring["medical_information"]["breakdown"]["health_checkup"] = 2
        except:
            scoring["medical_information"]["breakdown"]["health_checkup"] = 2
    else:
        scoring["medical_information"]["breakdown"]["health_checkup"] = 2
    
    allergies = medical.get('allergies', '')
    if not allergies:
        scoring["medical_information"]["breakdown"]["allergies"] = 0
    elif len(allergies.split(',')) > 1:
        scoring["medical_information"]["breakdown"]["allergies"] = 1
    else:
        scoring["medical_information"]["breakdown"]["allergies"] = 0.5
    
    scoring["medical_information"]["score"] = sum(scoring["medical_information"]["breakdown"].values())
    
    # V. Preferences & Risk Appetite (Max 4 Points)
    preferences = data.get('preferences_info', {})
    budget_flex = preferences.get('budgetFlexibility', '').lower()
    
    if 'high' in budget_flex:
        scoring["preferences_risk_appetite"]["breakdown"]["budget_flexibility"] = 0
    elif 'moderate' in budget_flex:
        scoring["preferences_risk_appetite"]["breakdown"]["budget_flexibility"] = 0.5
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["budget_flexibility"] = 1
    
    if preferences.get('willingToBuyRiders', '') == 'yes':
        scoring["preferences_risk_appetite"]["breakdown"]["riders_willingness"] = 0
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["riders_willingness"] = 1
    
    if preferences.get('flexibleDeductibles', '') == 'yes':
        scoring["preferences_risk_appetite"]["breakdown"]["deductible_flexibility"] = 0
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["deductible_flexibility"] = 1
    
    risk_tolerance = preferences.get('riskTolerance', '').lower()
    if 'conservative' in risk_tolerance:
        scoring["preferences_risk_appetite"]["breakdown"]["risk_tolerance"] = 0
    elif 'moderate' in risk_tolerance:
        scoring["preferences_risk_appetite"]["breakdown"]["risk_tolerance"] = 0.5
    else:
        scoring["preferences_risk_appetite"]["breakdown"]["risk_tolerance"] = 1
    
    scoring["preferences_risk_appetite"]["score"] = sum(scoring["preferences_risk_appetite"]["breakdown"].values())
    
    # VI. Dependents Information (Max 6 Points)
    dependents = data.get('family_info', {})
    dep_count = dependents.get('numDependents', 0)
    
    if dep_count == 0:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 0
    elif dep_count <= 2:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 1
    elif dep_count <= 4:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 2
    else:
        scoring["dependents_information"]["breakdown"]["number_of_dependents"] = 3
    
    # Calculate dependency level from dynamic form data
    dependency_score = 0
    for key in dependents.keys():
        if key.startswith('dependent_') and key.endswith('_dependency'):
            dependency_level = dependents[key]
            if dependency_level == 'full':
                dependency_score += 1.5
            elif dependency_level == 'partial':
                dependency_score += 1.0
            elif dependency_level == 'minimal':
                dependency_score += 0.5
    
    # Cap dependency score at 2.5
    dependency_score = min(dependency_score, 2.5)
    scoring["dependents_information"]["breakdown"]["dependency_level"] = dependency_score
    
    # Calculate age risk of dependents
    age_risk_score = 0
    for key in dependents.keys():
        if key.startswith('dependent_') and key.endswith('_age'):
            age = int(dependents[key]) if dependents[key] else 0
            if age >= 60:
                age_risk_score += 0.5
    
    # Cap age risk score at 1.5
    age_risk_score = min(age_risk_score, 1.5)
    scoring["dependents_information"]["breakdown"]["age_risk_dependents"] = age_risk_score
    
    scoring["dependents_information"]["score"] = sum(scoring["dependents_information"]["breakdown"].values())
    
    # VII. Insurance History (Max 4 Points)
    insurance = data.get('coverage_info', {})
    
    if insurance.get('hasLifeInsurance', '') != 'yes':
        scoring["insurance_history"]["breakdown"]["life_insurance"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["life_insurance"] = 0
    
    if insurance.get('hasHealthInsurance', '') != 'yes':
        scoring["insurance_history"]["breakdown"]["health_insurance"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["health_insurance"] = 0
    
    # Count claims from dynamic form data
    claims_count = 0
    for key in insurance.keys():
        if key.startswith('claim_amount_') and insurance[key]:
            claims_count += 1
    
    if claims_count == 0:
        scoring["insurance_history"]["breakdown"]["claim_history"] = 0
    elif claims_count <= 2:
        scoring["insurance_history"]["breakdown"]["claim_history"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["claim_history"] = 2
    
    if insurance.get('hasLapsedPolicies', '') == 'yes':
        scoring["insurance_history"]["breakdown"]["policy_lapse"] = 1
    else:
        scoring["insurance_history"]["breakdown"]["policy_lapse"] = 0
    
    scoring["insurance_history"]["score"] = sum(scoring["insurance_history"]["breakdown"].values())
    
    # VIII. Coverage Summary (Max 3 Points)
    coverage = data.get('coverage_info', {})
    
    # Calculate total life coverage from dynamic form data
    total_life_coverage = 0
    for key in coverage.keys():
        if key.startswith('life_sum_') and coverage[key]:
            total_life_coverage += float(coverage[key])
    
    # Calculate life coverage multiple of income
    annual_income = data.get('financial_info', {}).get('totalCTC', 0)
    if annual_income > 0:
        life_multiple = total_life_coverage / annual_income
        if life_multiple >= 10:
            scoring["coverage_summary"]["breakdown"]["life_coverage"] = 0
        elif life_multiple >= 5:
            scoring["coverage_summary"]["breakdown"]["life_coverage"] = 1
        else:
            scoring["coverage_summary"]["breakdown"]["life_coverage"] = 2
    else:
        scoring["coverage_summary"]["breakdown"]["life_coverage"] = 2
    
    # Calculate total health coverage from dynamic form data
    total_health_coverage = 0
    for key in coverage.keys():
        if key.startswith('health_sum_') and coverage[key]:
            total_health_coverage += float(coverage[key])
    
    if total_health_coverage >= 500000:  # 5L
        scoring["coverage_summary"]["breakdown"]["health_coverage"] = 0
    elif total_health_coverage >= 200000:  # 2L
        scoring["coverage_summary"]["breakdown"]["health_coverage"] = 0.5
    else:
        scoring["coverage_summary"]["breakdown"]["health_coverage"] = 1
    
    scoring["coverage_summary"]["score"] = sum(scoring["coverage_summary"]["breakdown"].values())
    
    # Calculate total score
    total_score = sum(category["score"] for category in scoring.values())
    max_possible_score = 53  # Fixed maximum score
    
    return {
        "detailed_scoring": scoring,
        "total_score": total_score,
        "max_possible_score": max_possible_score,
        "risk_percentage": round((total_score / max_possible_score) * 100, 1)
    }

def determine_risk_class(risk_percentage: float) -> dict:
    """Determine risk class based on percentage"""
    if risk_percentage <= 20:
        return {
            "class": "Very Low Risk",
            "rating": "A+",
            "description": "Excellent risk profile with minimal underwriting considerations",
            "recommended_cover": "Standard coverage with minimal loading",
            "suggested_premium": "Standard rates"
        }
    elif risk_percentage <= 40:
        return {
            "class": "Low Risk",
            "rating": "A",
            "description": "Good risk profile with standard underwriting considerations",
            "recommended_cover": "Standard coverage with slight loading",
            "suggested_premium": "Standard rates with minor adjustments"
        }
    elif risk_percentage <= 60:
        return {
            "class": "Moderate Risk",
            "rating": "B",
            "description": "Standard risk profile with moderate underwriting considerations",
            "recommended_cover": "Standard coverage with moderate loading",
            "suggested_premium": "Standard rates with moderate loading"
        }
    elif risk_percentage <= 80:
        return {
            "class": "High Risk",
            "rating": "C",
            "description": "Higher risk profile requiring detailed underwriting review",
            "recommended_cover": "Limited coverage with significant loading",
            "suggested_premium": "Higher rates with significant loading"
        }
    else:
        return {
            "class": "Very High Risk",
            "rating": "D",
            "description": "High-risk profile requiring specialized underwriting and medical review",
            "recommended_cover": "Specialized coverage with maximum loading",
            "suggested_premium": "Maximum rates with specialized underwriting"
        } 