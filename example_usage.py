#!/usr/bin/env python3
"""
Example Usage - How to use the Underwriting Data Collector with Gemini AI
"""

import os
from main import UnderwritingDataCollector, analyze_with_gemini, generate_comprehensive_report

def example_usage():
    """Example of how to use the system"""
    
    # Set your Gemini API key
    os.environ["GEMINI_API_KEY"] = "your_gemini_api_key_here"
    
    # Initialize the data collector
    collector = UnderwritingDataCollector()
    
    # Sample data from your forms (this would come from your Flask session)
    sample_data = {
        'basic_info': {
            'fullName': 'Priya Singh',
            'age': 34,
            'dob': '1990-03-15',
            'gender': 'female',
            'maritalStatus': 'single',
            'city': 'Pune',
            'state': 'Maharashtra'
        },
        'additional_info': {
            'occupation': 'Marketing Manager',
            'workingType': 'Onsite',
            'steps_per_day': 6200,
            'sleepHours': '6 hours',
            'smoker': 'no',
            'alcohol': 'Occasionally',
            'commuteType': 'Bike'
        },
        'family_info': {
            'numDependents': 1,
            'dependents': [
                {'relationship': 'Mother', 'age': 62, 'dependency_level': 'Partial'}
            ],
            'familyMedicalHistory': ['diabetes', 'hypertension']
        },
        'financial_info': {
            'employmentStatus': 'salaried',
            'totalCTC': 950000,
            'monthlySalary': 65000,
            'existingEMIs': 20000,
            'monthlyExpenses': 40000
        },
        'coverage_info': {
            'existingLifePolicies': [],
            'existingHealthPolicies': [{'sumAssured': 400000}],
            'totalLifeCoverage': 0,
            'totalHealthCoverage': 400000,
            'claimHistory': [{'year': 2023, 'amount': 50000}],
            'policyLapseHistory': []
        },
        'medical_info': {
            'height': 165,
            'weight': 75,
            'preExistingConditions': 'Mild BP (controlled)',
            'lastHealthCheckup': '2022-06-15',
            'allergies': 'Pollen (Mild)'
        },
        'preferences_info': {
            'deductibleFlexibility': 'moderate',
            'willingnessForRiders': 'yes',
            'riskTolerance': 'moderate'
        }
    }
    
    # Step 1: Collect and structure the data
    print("📊 Collecting and structuring data...")
    structured_data = collector.collect_all_data(sample_data)
    
    # Step 2: Save the structured data
    data_file = collector.save_json_data(structured_data)
    print(f"✅ Data saved to: {data_file}")
    
    # Step 3: Analyze with Gemini AI
    print("🤖 Analyzing with Gemini AI...")
    ai_analysis = analyze_with_gemini(structured_data)
    
    # Step 4: Generate comprehensive report
    print("📋 Generating comprehensive report...")
    report = generate_comprehensive_report(structured_data, ai_analysis)
    
    # Step 5: Save the report
    report_file = collector.save_json_data(report, f"ai_report_{structured_data['client_id']}.json")
    print(f"✅ Report saved to: {report_file}")
    
    # Step 6: Display results
    print("\n" + "="*60)
    print("📋 FINAL RESULTS")
    print("="*60)
    print(f"Client ID: {structured_data['client_id']}")
    print(f"Name: {structured_data['personal_information']['name']}")
    print(f"Age: {structured_data['personal_information']['age']}")
    print(f"Occupation: {structured_data['lifestyle_and_behavior']['occupation']}")
    print(f"Annual Income: {structured_data['financial_information']['ctc_annual_lakhs']}L")
    
    print("\n" + "="*60)
    print("🤖 AI ANALYSIS")
    print("="*60)
    print(ai_analysis)

if __name__ == "__main__":
    example_usage() 