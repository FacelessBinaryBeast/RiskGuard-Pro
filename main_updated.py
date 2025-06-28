#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Updated - Simple AI Analysis for Underwriting Risk Assessment
Gets JSON data, passes it to Gemini AI, and returns the assessment
"""

import json
import os
import argparse
import sys
from datetime import datetime
from typing import Dict, Any
import logging

# Gemini AI imports - using the correct import for google-genai==0.3.2
import google.generativeai as genai

# Set API key
os.environ["GEMINI_API_KEY"] = "Your_API_KEY"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_with_gemini(data: Dict[str, Any]) -> str:
    """
    Analyze data using Gemini 2.0 Flash AI model
    
    Args:
        data: JSON data from the forms
        
    Returns:
        AI analysis result as string
    """
    try:
        # Configure Gemini
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        
        # Use Gemini 2.0 Flash model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Convert data to JSON string
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        
        # AI prompt for underwriting risk assessment
        prompt = f"""You are an expert insurance underwriter. Analyze this client's data and provide a personalized, comprehensive risk assessment.

**CLIENT DATA:**
{json_data}

**REQUIRED ANALYSIS FORMAT:**

**DETAILED ANALYSIS:**
• [Analyze age, occupation, and lifestyle factors - be specific to this client's data]
• [Evaluate medical history and current health status - reference specific conditions if any]
• [Assess financial stability and income capacity - mention specific amounts]
• [Review insurance history and claims experience - be specific about their history]
• [Identify any high-risk factors specific to this client]
• [Highlight positive indicators unique to this client's profile]

**RISK FACTORS:**
• [List specific risk factors found in this client's data - one line each]
• [Explain how each factor impacts their insurability]

**POSITIVE INDICATORS:**
• [List positive factors from this client's profile - one line each]
• [Explain how these factors benefit their insurance application]

**AREAS OF CONCERN:**
• [Identify specific concerns from their data - one line each]
• [Explain what additional information or actions might be needed]

**RECOMMENDATIONS:**
• [Provide specific policy recommendations based on their profile]
• [Suggest appropriate coverage amounts based on their income and needs]
• [Recommend any medical requirements or checkups needed]
• [Suggest premium payment options suitable for their financial situation]
• [Recommend any riders or additional coverage they should consider]

**CONCLUSION:**
[Provide a personalized conclusion about this specific client's risk profile, insurability, and recommended next steps in 2-3 detailed lines]

Please make this analysis highly personalized to the specific data provided. Reference their actual age, occupation, income, medical conditions, and other specific details from their profile."""
        
        logger.info("Starting Gemini 2.0 Flash AI analysis...")
        
        # Generate response
        response = model.generate_content(prompt)
        
        logger.info("Gemini 2.0 Flash AI analysis completed successfully")
        
        return response.text
        
    except Exception as e:
        logger.error(f"Error in Gemini 2.0 Flash AI analysis: {str(e)}")
        return f"AI analysis not available due to configuration issues: {str(e)}"

def main():
    """Main function to process JSON data and return AI analysis"""
    parser = argparse.ArgumentParser(description='AI Risk Assessment Tool')
    parser.add_argument('--data-file', help='Path to JSON data file', required=True)
    args = parser.parse_args()
    
    try:
        # Load data from file with better error handling
        data = None
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(args.data_file, 'r', encoding=encoding) as f:
                    data = json.load(f)
                logger.info(f"Successfully loaded data with {encoding} encoding")
                break
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode with {encoding} encoding, trying next...")
                continue
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error with {encoding} encoding: {e}")
                continue
        
        if data is None:
            raise Exception("Failed to load JSON data with any encoding")
        
        # Perform AI analysis
        ai_analysis = analyze_with_gemini(data)
        
        # Output the analysis
        print("AI Analysis:")
        print(ai_analysis)
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
