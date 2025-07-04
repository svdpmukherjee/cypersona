import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_knowbe4_dataset(n_records=5000):
    """Generate realistic KnowBe4 dataset with actual KnowBe4 columns"""
    
    data = []
    
    # KnowBe4 campaign templates and difficulty levels
    campaign_templates = [
        'Account Verification', 'Account Suspended', 'Security Alert', 
        'Password Expiration', 'Document Share', 'Financial Request',
        'IT Support', 'Software Update', 'Survey Request', 'Meeting Invitation',
        'Package Delivery', 'HR Communication', 'VPN Access', 'System Maintenance'
    ]
    
    # Employee roles and departments
    roles = ['Employee', 'Manager', 'Director', 'Admin', 'Executive', 'Contractor']
    departments = ['Finance', 'HR', 'IT', 'Sales', 'Operations', 'Marketing', 'Legal', 'R&D']
    locations = ['New York', 'London', 'Tokyo', 'San Francisco', 'Chicago', 'Frankfurt', 'Sydney']
    
    # Generate base employee pool
    n_employees = 1200
    employees = []
    for i in range(n_employees):
        employees.append({
            'employee_id': f'EMP_{i+1:04d}',
            'department': np.random.choice(departments),
            'role': np.random.choice(roles, p=[0.55, 0.25, 0.08, 0.08, 0.03, 0.01]),
            'location': np.random.choice(locations),
            'hire_date': datetime.now() - timedelta(days=np.random.randint(30, 2000)),
            'training_completed': np.random.choice([True, False], p=[0.75, 0.25])
        })
    
    # Generate campaigns over time
    start_date = datetime.now() - timedelta(days=365)
    
    for record_id in range(n_records):
        employee = np.random.choice(employees)
        
        # Campaign details
        campaign_date = start_date + timedelta(days=np.random.randint(0, 365))
        template = np.random.choice(campaign_templates)
        difficulty = np.random.choice(['Low', 'Medium', 'High'], p=[0.4, 0.45, 0.15])
        
        # Role-based click susceptibility
        role_click_rates = {
            'Employee': 0.18, 'Manager': 0.12, 'Director': 0.08, 
            'Admin': 0.22, 'Executive': 0.06, 'Contractor': 0.25
        }
        base_click_rate = role_click_rates[employee['role']]
        
        # Difficulty adjustment
        difficulty_multiplier = {'Low': 1.4, 'Medium': 1.0, 'High': 0.6}
        adjusted_click_rate = base_click_rate * difficulty_multiplier[difficulty]
        
        # Training effect
        if employee['training_completed']:
            adjusted_click_rate *= 0.7
        
        # Time-based factors (end of day, Monday mornings more vulnerable)
        hour = np.random.randint(9, 18)
        if hour >= 16 or campaign_date.weekday() == 0:  # After 4pm or Monday
            adjusted_click_rate *= 1.3
        
        # Determine if clicked
        clicked = np.random.random() < adjusted_click_rate
        
        # Reporting behavior
        if clicked:
            reported = np.random.random() < 0.15  # Low report rate after clicking
            time_to_report = np.random.exponential(300) if reported else None
        else:
            reported = np.random.random() < 0.45  # Higher report rate if didn't click
            time_to_report = np.random.exponential(180) if reported else None
        
        # Time to click (if clicked)
        if clicked:
            # Urgent templates = faster clicks
            urgent_templates = ['Account Suspended', 'Security Alert', 'Password Expiration']
            if template in urgent_templates:
                time_to_click = np.random.lognormal(2.5, 0.8)  # Faster
            else:
                time_to_click = np.random.lognormal(3.2, 1.0)  # Normal
        else:
            time_to_click = None
        
        # Awareness score (KnowBe4's proprietary score)
        base_awareness = 65
        if employee['training_completed']:
            base_awareness += 15
        if employee['role'] in ['Director', 'Executive']:
            base_awareness += 10
        if clicked:
            base_awareness -= 20
        if reported and not clicked:
            base_awareness += 10
            
        awareness_score = max(0, min(100, base_awareness + np.random.normal(0, 10)))
        
        # Previous 12 months stats
        phish_prone_percentage = max(0, min(100, adjusted_click_rate * 100 + np.random.normal(0, 5)))
        
        data.append({
            'User ID': employee['employee_id'],
            'Email': f"{employee['employee_id'].lower()}@company.com",
            'First Name': f"User{employee['employee_id'][-4:]}",
            'Last Name': f"LastName{employee['employee_id'][-3:]}",
            'Department': employee['department'],
            'Title': employee['role'],
            'Location': employee['location'],
            'Campaign Name': f"Q{np.random.randint(1,5)} {campaign_date.year} - {template}",
            'Template': template,
            'Sent Date': campaign_date.strftime('%m/%d/%Y %H:%M'),
            'Opened': np.random.choice([True, False], p=[0.8, 0.2]),
            'Clicked': clicked,
            'Replied': np.random.choice([True, False], p=[0.02, 0.98]) if clicked else False,
            'Attachment Opened': np.random.choice([True, False], p=[0.3, 0.7]) if clicked else False,
            'Macro Enabled': np.random.choice([True, False], p=[0.1, 0.9]) if clicked else False,
            'Data Entered': np.random.choice([True, False], p=[0.4, 0.6]) if clicked else False,
            'Reported': reported,
            'Time to Click (seconds)': int(time_to_click) if time_to_click else None,
            'Time to Report (seconds)': int(time_to_report) if time_to_report else None,
            'IP Address': f"192.168.{np.random.randint(1,255)}.{np.random.randint(1,255)}",
            'Browser': np.random.choice(['Chrome', 'Firefox', 'Edge', 'Safari'], p=[0.6, 0.2, 0.15, 0.05]),
            'Operating System': np.random.choice(['Windows 10', 'Windows 11', 'macOS', 'Linux'], p=[0.5, 0.3, 0.15, 0.05]),
            'Delivery Status': np.random.choice(['Delivered', 'Bounced'], p=[0.95, 0.05]),
            'Difficulty': difficulty,
            'Phish-prone Percentage': round(phish_prone_percentage, 1),
            'Current Risk Score': round(awareness_score, 1),
            'Previous Training Completed': employee['training_completed'],
            'Training Completion Date': (employee['hire_date'] + timedelta(days=30)).strftime('%m/%d/%Y') if employee['training_completed'] else None,
            'Groups': f"{employee['department']} - {employee['location']}",
            'Manager Email': f"manager_{employee['department'].lower()}@company.com",
            'Employee ID': employee['employee_id'],
            'Hire Date': employee['hire_date'].strftime('%m/%d/%Y'),
            'Active Directory': True,
            'Division': np.random.choice(['North America', 'Europe', 'Asia-Pacific']),
            'Cost Center': f"CC-{np.random.randint(1000, 9999)}",
            'Custom Field 1': np.random.choice(['Level 1', 'Level 2', 'Level 3']),
            'Custom Field 2': np.random.choice(['Remote', 'Hybrid', 'On-site']),
            'Baseline Test Score': np.random.randint(60, 95),
            'Last Training Score': np.random.randint(70, 100) if employee['training_completed'] else None,
            'Security Awareness Proficiency': np.random.choice(['Novice', 'Intermediate', 'Advanced']),
            'Risk Level': 'High' if phish_prone_percentage > 20 else 'Medium' if phish_prone_percentage > 10 else 'Low',
            'Failure Count (12 months)': np.random.randint(0, 8),
            'Success Count (12 months)': np.random.randint(2, 15),
            'Last Failure Date': (campaign_date - timedelta(days=np.random.randint(0, 365))).strftime('%m/%d/%Y') if clicked else None,
            'Campaign Type': np.random.choice(['Phishing', 'Vishing', 'Smishing'], p=[0.8, 0.15, 0.05]),
            'Industry Template': np.random.choice(['Generic', 'Financial', 'Healthcare', 'Technology']),
            'Language': np.random.choice(['English', 'Spanish', 'French', 'German'], p=[0.7, 0.15, 0.1, 0.05]),
            'Time Zone': np.random.choice(['EST', 'PST', 'GMT', 'JST']),
            'Mobile Device': np.random.choice([True, False], p=[0.3, 0.7]),
            'VPN Connection': np.random.choice([True, False], p=[0.4, 0.6]),
            'Two Factor Enabled': np.random.choice([True, False], p=[0.65, 0.35]),
            'Password Manager': np.random.choice([True, False], p=[0.45, 0.55])
        })
    
    return pd.DataFrame(data)

# Generate dataset
df = generate_knowbe4_dataset(5000)
df.to_csv('../data/knowbe4.csv', index=False)