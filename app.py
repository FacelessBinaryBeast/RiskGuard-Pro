#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Application for Underwriting Risk Assessment
Handles form data collection and AI analysis
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import subprocess
import sys
from scoring_functions import calculate_detailed_scoring, determine_risk_class

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Ensure templates and static directories exist
if not os.path.exists('templates'):
    os.makedirs('templates')
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def landing_page():
    """Landing page with navigation to all forms"""
    return render_template('landing.html')

@app.route('/basics')
def basics_form():
    """Basic personal information form"""
    return render_template('basics.html')

@app.route('/additional')
def additional_form():
    """Additional lifestyle details form"""
    return render_template('additional.html')

@app.route('/familydetails')
def family_details_form():
    """Family and dependents information form"""
    return render_template('familydetails.html')

@app.route('/finances')
def finances_form():
    """Financial and employment information form"""
    return render_template('finances.html')

@app.route('/coverage')
def coverage_form():
    """Insurance coverage history form"""
    return render_template('coverage.html')

@app.route('/medical')
def medical_form():
    """Medical information form"""
    return render_template('medical.html')

@app.route('/preferences')
def preferences_form():
    """Preferences and risk appetite form"""
    return render_template('preferences.html')

@app.route('/summary')
def summary_page():
    """Summary page with all collected data"""
    return render_template('summary.html')

@app.route('/ai_analysis')
def ai_analysis():
    """Display AI analysis results page"""
    return render_template('ai_analysis.html')

@app.route('/api/get_ai_analysis')
def get_ai_analysis():
    """Get AI analysis using main_updated.py"""
    try:
        # Collect all data from session
        data = {
            'basic_info': session.get('basic_info', {}),
            'additional_info': session.get('additional_info', {}),
            'financial_info': session.get('financial_info', {}),
            'medical_info': session.get('medical_info', {}),
            'preferences_info': session.get('preferences_info', {}),
            'family_info': session.get('family_info', {}),
            'coverage_info': session.get('coverage_info', {})
        }
        
        # Check if we have enough data
        if not any(data.values()):
            return jsonify({
                'success': False,
                'error': 'No data found. Please complete the assessment first.'
            })
        
        # Log data for debugging
        print(f"Data being sent to AI analysis: {json.dumps(data, indent=2)}")
        
        # Generate AI analysis using main_updated.py
        temp_data_file = f"temp_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(temp_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Temporary file created: {temp_data_file}")
        except Exception as e:
            raise Exception(f"Failed to save temporary data file: {str(e)}")
        
        try:
            # Call main_updated.py as a subprocess
            print(f"Calling main_updated.py with file: {temp_data_file}")
            result = subprocess.run([
                sys.executable, 'main_updated.py', '--data-file', temp_data_file
            ], capture_output=True, text=True, timeout=60, encoding='utf-8')
            
            print(f"Subprocess return code: {result.returncode}")
            print(f"Subprocess stdout: {result.stdout}")
            print(f"Subprocess stderr: {result.stderr}")
            
            if result.returncode != 0:
                raise Exception(f"AI analysis failed: {result.stderr}")
            
            # Get the AI analysis output
            ai_analysis = result.stdout.strip()
            
            # Clean up temporary file
            if os.path.exists(temp_data_file):
                os.remove(temp_data_file)
                print(f"Temporary file cleaned up: {temp_data_file}")
            
            return jsonify({
                'success': True,
                'ai_analysis': ai_analysis
            })
            
        except subprocess.TimeoutExpired:
            # Clean up temporary file on error
            if os.path.exists(temp_data_file):
                os.remove(temp_data_file)
            raise Exception("AI analysis timed out after 60 seconds")
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(temp_data_file):
                os.remove(temp_data_file)
            raise e
        
    except Exception as e:
        print(f"Error in get_ai_analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error generating AI analysis: {str(e)}'
        })

# API Routes for saving data
@app.route('/api/save_basics', methods=['POST'])
def save_basics():
    """Save basic information"""
    try:
        data = request.get_json()
        session['basic_info'] = data
        return jsonify({'success': True, 'message': 'Basic information saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save_additional', methods=['POST'])
def save_additional():
    """Save additional lifestyle information"""
    try:
        data = request.get_json()
        session['additional_info'] = data
        return jsonify({'success': True, 'message': 'Additional information saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save_family', methods=['POST'])
def save_family():
    """Save family information"""
    try:
        data = request.get_json()
        session['family_info'] = data
        return jsonify({'success': True, 'message': 'Family information saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save_finances', methods=['POST'])
def save_finances():
    """Save financial information"""
    try:
        data = request.get_json()
        session['financial_info'] = data
        return jsonify({'success': True, 'message': 'Financial information saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save_coverage', methods=['POST'])
def save_coverage():
    """Save coverage information"""
    try:
        data = request.get_json()
        session['coverage_info'] = data
        return jsonify({'success': True, 'message': 'Coverage information saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save_medical', methods=['POST'])
def save_medical():
    """Save medical information"""
    try:
        data = request.get_json()
        session['medical_info'] = data
        return jsonify({'success': True, 'message': 'Medical information saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save_preferences', methods=['POST'])
def save_preferences():
    """Save preferences information"""
    try:
        data = request.get_json()
        session['preferences_info'] = data
        return jsonify({'success': True, 'message': 'Preferences saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_all_data')
def get_all_data():
    """Get all saved data for assessment"""
    try:
        all_data = {
            'basic_info': session.get('basic_info', {}),
            'additional_info': session.get('additional_info', {}),
            'family_info': session.get('family_info', {}),
            'financial_info': session.get('financial_info', {}),
            'coverage_info': session.get('coverage_info', {}),
            'medical_info': session.get('medical_info', {}),
            'preferences_info': session.get('preferences_info', {})
        }
        return jsonify({'success': True, 'data': all_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clear_session')
def clear_session():
    """Clear all session data"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Session cleared successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate_pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF report with all collected data"""
    try:
        data = request.get_json()
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        story.append(Paragraph("Underwriting Risk Assessment Report", title_style))
        story.append(Spacer(1, 20))
        
        # Date
        date_style = ParagraphStyle(
            'Date',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", date_style))
        story.append(Spacer(1, 30))
        
        # Basic Information
        story.append(Paragraph("Personal Information", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        basic_data = [
            ['Field', 'Value'],
            ['Full Name', data.get('basicInfo', {}).get('fullName', 'Not provided')],
            ['Age', str(data.get('basicInfo', {}).get('age', 'Not provided'))],
            ['Gender', data.get('basicInfo', {}).get('gender', 'Not provided')],
            ['Marital Status', data.get('basicInfo', {}).get('maritalStatus', 'Not provided')],
            ['Email', data.get('basicInfo', {}).get('email', 'Not provided')],
            ['Phone', data.get('basicInfo', {}).get('phone', 'Not provided')],
            ['City', data.get('basicInfo', {}).get('city', 'Not provided')],
            ['State', data.get('basicInfo', {}).get('state', 'Not provided')],
            ['Pincode', data.get('basicInfo', {}).get('pincode', 'Not provided')],
            ['Nationality', data.get('basicInfo', {}).get('nationality', 'Not provided')]
        ]
        
        basic_table = Table(basic_data, colWidths=[2*inch, 4*inch])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(basic_table)
        story.append(Spacer(1, 20))
        
        # Lifestyle Information
        story.append(Paragraph("Lifestyle Details", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        lifestyle_data = [
            ['Field', 'Value'],
            ['Occupation', data.get('additionalInfo', {}).get('occupation', 'Not provided')],
            ['Working Type', data.get('additionalInfo', {}).get('workingType', 'Not provided')],
            ['Daily Steps', str(data.get('additionalInfo', {}).get('steps_per_day', 'Not provided'))],
            ['Sleep Hours', str(data.get('additionalInfo', {}).get('sleep', 'Not provided'))],
            ['BMI', str(data.get('additionalInfo', {}).get('bmi', 'Not provided'))],
            ['Smoker', data.get('additionalInfo', {}).get('smoker', 'Not provided')],
            ['Alcohol Consumption', data.get('additionalInfo', {}).get('alcohol', 'Not provided')],
            ['Hobbies', data.get('additionalInfo', {}).get('hobbies', 'Not provided')],
            ['Commute Type', data.get('additionalInfo', {}).get('commute', 'Not provided')]
        ]
        
        lifestyle_table = Table(lifestyle_data, colWidths=[2*inch, 4*inch])
        lifestyle_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(lifestyle_table)
        story.append(Spacer(1, 20))
        
        # Financial Information
        story.append(Paragraph("Financial Information", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        financial_data = [
            ['Field', 'Value'],
            ['Employment Status', data.get('financialInfo', {}).get('employmentStatus', 'Not provided')],
            ['Total CTC (Annual)', 'Rs. ' + str(data.get('financialInfo', {}).get('totalCTC', 'Not provided'))],
            ['Monthly Salary', 'Rs. ' + str(data.get('financialInfo', {}).get('monthlySalary', 'Not provided'))],
            ['Income Stability', data.get('financialInfo', {}).get('incomeStability', 'Not provided')],
            ['Monthly EMIs', 'Rs. ' + str(data.get('financialInfo', {}).get('existingEMIs', 'Not provided'))],
            ['Monthly Expenses', 'Rs. ' + str(data.get('financialInfo', {}).get('monthlyExpenses', 'Not provided'))],
            ['Disposable Income', 'Rs. ' + str(data.get('financialInfo', {}).get('disposableIncome', 'Not provided'))]
        ]
        
        financial_table = Table(financial_data, colWidths=[2*inch, 4*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(financial_table)
        story.append(Spacer(1, 20))
        
        # Medical Information
        story.append(Paragraph("Medical Information", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        medical_data = [
            ['Field', 'Value'],
            ['Pre-existing Conditions', data.get('medicalInfo', {}).get('preExistingConditions', 'Not provided')],
            ['Height (cm)', str(data.get('medicalInfo', {}).get('height', 'Not provided'))],
            ['Weight (kg)', str(data.get('medicalInfo', {}).get('weight', 'Not provided'))],
            ['Calculated BMI', str(data.get('medicalInfo', {}).get('bmi', 'Not provided'))],
            ['Last Health Checkup', data.get('medicalInfo', {}).get('lastCheckup', 'Not provided')],
            ['Allergies', data.get('medicalInfo', {}).get('allergies', 'Not provided')]
        ]
        
        medical_table = Table(medical_data, colWidths=[2*inch, 4*inch])
        medical_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(medical_table)
        story.append(Spacer(1, 20))
        
        # Preferences
        story.append(Paragraph("Preferences & Risk Appetite", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        preferences_data = [
            ['Field', 'Value'],
            ['Monthly Premium Budget', 'Rs. ' + str(data.get('preferencesInfo', {}).get('premiumBudget', 'Not provided'))],
            ['Budget Flexibility', data.get('preferencesInfo', {}).get('budgetFlexibility', 'Not provided')],
            ['Primary Insurance Interest', data.get('preferencesInfo', {}).get('primaryInterest', 'Not provided')],
            ['Willing to Buy Riders', data.get('preferencesInfo', {}).get('willingToBuyRiders', 'Not provided')],
            ['Flexible Deductibles', data.get('preferencesInfo', {}).get('flexibleDeductibles', 'Not provided')],
            ['Coverage Priority', data.get('preferencesInfo', {}).get('coveragePriority', 'Not provided')],
            ['Investment Horizon', data.get('preferencesInfo', {}).get('investmentHorizon', 'Not provided')],
            ['Risk Tolerance', data.get('preferencesInfo', {}).get('riskTolerance', 'Not provided')]
        ]
        
        preferences_table = Table(preferences_data, colWidths=[2*inch, 4*inch])
        preferences_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(preferences_table)
        story.append(Spacer(1, 20))
        
        # Expected Risk Assessment Summary
        story.append(Paragraph("Expected Risk Assessment Summary", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Calculate risk score
        scoring_result = calculate_detailed_scoring(data)
        risk_percentage = scoring_result['risk_percentage']
        risk_class = determine_risk_class(risk_percentage)
        
        risk_data = [
            ['Field', 'Value'],
            ['Risk Score', f"{scoring_result['total_score']}/53"],
            ['Risk Percentage', f"{risk_percentage}%"],
            ['Risk Level', risk_class['class']],
            ['Risk Rating', risk_class['rating']],
            ['Recommended Cover', risk_class['recommended_cover']],
            ['Suggested Premium', risk_class['suggested_premium']],
            ['Description', risk_class['description']]
        ]
        
        risk_table = Table(risk_data, colWidths=[2*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(risk_table)
        story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name='underwriting_assessment_report.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download_ai_analysis_pdf', methods=['POST'])
def download_ai_analysis_pdf():
    """Generate and download PDF of AI analysis report"""
    try:
        data = request.get_json()
        ai_analysis = data.get('ai_analysis', '')
        
        if not ai_analysis:
            return jsonify({'success': False, 'error': 'No analysis content provided'}), 400
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        story.append(Paragraph("AI Risk Assessment Report", title_style))
        
        # Date
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", date_style))
        story.append(Spacer(1, 20))
        
        # Process AI analysis text to remove asterisks and format properly
        formatted_analysis = format_ai_analysis_for_pdf(ai_analysis)
        
        # Add formatted analysis with better structure
        analysis_style = ParagraphStyle(
            'AnalysisStyle',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            leading=16,
            textColor=colors.black,
            alignment=TA_LEFT
        )
        
        bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leading=16,
            textColor=colors.black,
            leftIndent=20,
            alignment=TA_LEFT
        )
        
        # Split analysis into sections and format each
        sections = formatted_analysis.split('\n\n')
        for section in sections:
            if section.strip():
                # Check if it's a header (all caps or ends with colon)
                if section.isupper() or section.strip().endswith(':'):
                    header_style = ParagraphStyle(
                        'SectionHeader',
                        parent=styles['Heading2'],
                        fontSize=14,
                        spaceAfter=8,
                        spaceBefore=15,
                        textColor=colors.darkblue,
                        fontName='Helvetica-Bold'
                    )
                    story.append(Paragraph(section.strip(), header_style))
                else:
                    # Regular content - check if it contains bullet points
                    if '•' in section:
                        # Split into bullet points
                        bullet_points = section.split('•')
                        for i, point in enumerate(bullet_points):
                            point = point.strip()
                            if point:
                                if i == 0 and not point.startswith('•'):
                                    # First item might not be a bullet point
                                    story.append(Paragraph(point, analysis_style))
                                else:
                                    # Add bullet point
                                    story.append(Paragraph(f"• {point}", bullet_style))
                    else:
                        # Regular paragraph
                        story.append(Paragraph(section.strip(), analysis_style))
                story.append(Spacer(1, 8))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph("This report was generated by AI-powered underwriting risk assessment system", footer_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"AI_Risk_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating AI analysis PDF: {str(e)}")
        return jsonify({'success': False, 'error': f'Error generating PDF: {str(e)}'}), 500

def format_ai_analysis_for_pdf(analysis_text):
    """Format AI analysis text for PDF with proper formatting and no asterisks"""
    # Remove asterisks
    formatted_text = analysis_text.replace('*', '')
    
    # Replace rupee symbols with "Rs."
    formatted_text = formatted_text.replace('₹', 'Rs.')
    formatted_text = formatted_text.replace('₹', 'Rs.')  # Handle different rupee symbol variants
    
    # Clean up extra whitespace
    formatted_text = '\n'.join(line.strip() for line in formatted_text.split('\n') if line.strip())
    
    # Structure the content into proper sections
    sections = []
    current_section = ""
    
    # Split by double newlines to identify sections
    parts = formatted_text.split('\n\n')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Check if this is a header (all caps or ends with colon)
        if part.isupper() or part.strip().endswith(':'):
            # Save previous section if exists
            if current_section.strip():
                sections.append(current_section.strip())
            # Start new section
            current_section = part
        else:
            # Add to current section
            if current_section:
                current_section += '\n\n' + part
            else:
                current_section = part
    
    # Add the last section
    if current_section.strip():
        sections.append(current_section.strip())
    
    # Format each section properly
    formatted_sections = []
    for section in sections:
        if section.isupper() or section.strip().endswith(':'):
            # This is a header
            formatted_sections.append(section)
        else:
            # This is content - break into paragraphs
            paragraphs = section.split('\n')
            formatted_paragraphs = []
            
            for para in paragraphs:
                para = para.strip()
                if para:
                    # Clean up bullet points
                    if para.startswith('•') or para.startswith('-'):
                        para = '• ' + para[1:].strip()
                    formatted_paragraphs.append(para)
            
            # Join paragraphs with proper spacing
            formatted_sections.append('\n\n'.join(formatted_paragraphs))
    
    # Join sections with double newlines
    return '\n\n'.join(formatted_sections)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 