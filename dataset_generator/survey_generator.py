import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_survey_1_psychological_stress():
    """
    Survey 1: Psychological Stress and Cognitive Load in Phishing Detection
    Focus: Stress responses, cognitive load, anxiety, decision-making under pressure
    """
    n = 120
    data = []
    
    # Demographics
    roles = ['Healthcare Worker', 'Teacher', 'Engineer', 'Manager', 'Analyst', 'Technician']
    age_groups = ['25-34', '35-44', '45-54', '55-64']
    education = ['Bachelor', 'Master', 'PhD', 'High School']
    
    for i in range(n):
        # Baseline characteristics
        role = np.random.choice(roles)
        age_group = np.random.choice(age_groups)
        work_exp = np.random.randint(1, 25)
        
        # Pre/Post intervention measures (7-point Likert)
        # Stress & Anxiety measures
        pre_email_anxiety = np.random.randint(1, 8)
        post_email_anxiety = max(1, min(7, pre_email_anxiety + np.random.randint(-2, 3)))
        
        pre_decision_stress = np.random.randint(1, 8)
        post_decision_stress = max(1, min(7, pre_decision_stress + np.random.randint(-3, 2)))
        
        # Cognitive Load measures
        pre_mental_effort = np.random.randint(1, 8)
        post_mental_effort = max(1, min(7, pre_mental_effort + np.random.randint(-2, 4)))
        
        pre_confusion_level = np.random.randint(1, 8)
        post_confusion_level = max(1, min(7, pre_confusion_level + np.random.randint(-3, 1)))
        
        # Time pressure perception
        pre_time_pressure = np.random.randint(1, 8)
        post_time_pressure = max(1, min(7, pre_time_pressure + np.random.randint(-2, 2)))
        
        # Emotional regulation
        emotional_control = np.random.randint(1, 8)
        frustration_tolerance = np.random.randint(1, 8)
        
        # Intervention type
        intervention = np.random.choice(['Mindfulness Training', 'Stress Reduction', 'Cognitive Load Training', 'Control'])
        
        data.append({
            'participant_id': f'PSY_{i+1:03d}',
            'role': role,
            'age_group': age_group,
            'work_experience_years': work_exp,
            'education_level': np.random.choice(education),
            'intervention_type': intervention,
            'pre_email_opening_anxiety': pre_email_anxiety,
            'post_email_opening_anxiety': post_email_anxiety,
            'pre_decision_making_stress': pre_decision_stress,
            'post_decision_making_stress': post_decision_stress,
            'pre_cognitive_mental_effort': pre_mental_effort,
            'post_cognitive_mental_effort': post_mental_effort,
            'pre_information_confusion': pre_confusion_level,
            'post_information_confusion': post_confusion_level,
            'pre_time_pressure_perception': pre_time_pressure,
            'post_time_pressure_perception': post_time_pressure,
            'emotional_self_control': emotional_control,
            'frustration_tolerance_level': frustration_tolerance,
            'physiological_heart_rate_change': np.random.uniform(-10, 15),
            'cortisol_level_change': np.random.uniform(-20, 30),
            'response_time_seconds': np.random.uniform(5, 120),
            'accuracy_improvement': np.random.uniform(-0.2, 0.6),
            'survey_completion_date': datetime.now() - timedelta(days=np.random.randint(1, 180))
        })
    
    return pd.DataFrame(data)

def generate_survey_2_motivation_attitude():
    """
    Survey 2: Motivational Factors and Attitude Change
    Focus: Motivation theories (SDT, TPB), attitude change, behavioral intentions
    """
    n = 135
    data = []
    
    departments = ['Finance', 'HR', 'Operations', 'Marketing', 'IT', 'Legal']
    company_sizes = ['Small (<100)', 'Medium (100-500)', 'Large (>500)']
    
    for i in range(n):
        # Demographics
        department = np.random.choice(departments)
        company_size = np.random.choice(company_sizes)
        tenure = np.random.randint(1, 20)
        
        # Self-Determination Theory measures (5-point Likert)
        autonomy_pre = np.random.randint(1, 6)
        autonomy_post = max(1, min(5, autonomy_pre + np.random.randint(-1, 3)))
        
        competence_pre = np.random.randint(1, 6)
        competence_post = max(1, min(5, competence_pre + np.random.randint(-1, 4)))
        
        relatedness_pre = np.random.randint(1, 6)
        relatedness_post = max(1, min(5, relatedness_pre + np.random.randint(-1, 2)))
        
        # Theory of Planned Behavior
        attitude_towards_reporting = np.random.randint(1, 8)
        subjective_norms_pressure = np.random.randint(1, 8)
        perceived_behavioral_control = np.random.randint(1, 8)
        behavioral_intention_strength = np.random.randint(1, 8)
        
        # Motivation types
        intrinsic_motivation = np.random.randint(1, 8)
        extrinsic_motivation = np.random.randint(1, 8)
        amotivation_level = np.random.randint(1, 8)
        
        # Attitude dimensions
        cognitive_attitude = np.random.randint(1, 8)
        affective_attitude = np.random.randint(1, 8)
        
        # Training approach
        training_method = np.random.choice(['Gamification', 'Social Learning', 'Goal Setting', 'Incentive-based', 'Control'])
        
        data.append({
            'response_id': f'MOT_{i+1:03d}',
            'department': department,
            'company_size': company_size,
            'tenure_months': tenure,
            'training_method': training_method,
            'sdt_autonomy_pre': autonomy_pre,
            'sdt_autonomy_post': autonomy_post,
            'sdt_competence_pre': competence_pre,
            'sdt_competence_post': competence_post,
            'sdt_relatedness_pre': relatedness_pre,
            'sdt_relatedness_post': relatedness_post,
            'tpb_attitude_reporting': attitude_towards_reporting,
            'tpb_subjective_norms': subjective_norms_pressure,
            'tpb_perceived_control': perceived_behavioral_control,
            'tpb_behavioral_intention': behavioral_intention_strength,
            'intrinsic_motivation_score': intrinsic_motivation,
            'extrinsic_motivation_score': extrinsic_motivation,
            'amotivation_score': amotivation_level,
            'cognitive_attitude_change': cognitive_attitude,
            'affective_attitude_change': affective_attitude,
            'goal_commitment_level': np.random.randint(1, 8),
            'social_influence_susceptibility': np.random.randint(1, 8),
            'reward_sensitivity': np.random.randint(1, 8),
            'punishment_sensitivity': np.random.randint(1, 8),
            'engagement_duration_minutes': np.random.uniform(10, 180),
            'motivation_sustainability_weeks': np.random.randint(1, 12),
            'completion_timestamp': datetime.now() - timedelta(days=np.random.randint(1, 90))
        })
    
    return pd.DataFrame(data)

def generate_survey_3_emotional_behavioral():
    """
    Survey 3: Emotional Responses and Behavioral Adaptation
    Focus: Emotional intelligence, fear appeals, behavioral change, social factors
    """
    n = 110
    data = []
    
    job_levels = ['Entry Level', 'Mid Level', 'Senior Level', 'Executive']
    industries = ['Healthcare', 'Finance', 'Education', 'Technology', 'Government', 'Manufacturing']
    
    for i in range(n):
        # Demographics
        job_level = np.random.choice(job_levels)
        industry = np.random.choice(industries)
        team_size = np.random.randint(3, 50)
        
        # Emotional Intelligence measures (6-point scale)
        emotional_awareness = np.random.randint(1, 7)
        emotional_regulation = np.random.randint(1, 7)
        empathy_level = np.random.randint(1, 7)
        social_skills = np.random.randint(1, 7)
        
        # Fear Appeal Response (Protection Motivation Theory)
        threat_vulnerability = np.random.randint(1, 8)
        threat_severity = np.random.randint(1, 8)
        response_efficacy = np.random.randint(1, 8)
        self_efficacy = np.random.randint(1, 8)
        fear_arousal = np.random.randint(1, 8)
        
        # Behavioral Change measures
        behavior_pre_score = np.random.randint(1, 11)  # 10-point scale
        behavior_post_score = max(1, min(10, behavior_pre_score + np.random.randint(-2, 5)))
        
        # Social Learning factors
        observational_learning = np.random.randint(1, 7)
        peer_modeling = np.random.randint(1, 7)
        social_reinforcement = np.random.randint(1, 7)
        
        # Emotional responses to interventions
        intervention_approach = np.random.choice(['Fear Appeal', 'Positive Reinforcement', 'Social Proof', 'Narrative', 'Control'])
        
        data.append({
            'participant_code': f'EMO_{i+1:03d}',
            'job_level': job_level,
            'industry_sector': industry,
            'team_size': team_size,
            'intervention_approach': intervention_approach,
            'ei_emotional_awareness': emotional_awareness,
            'ei_emotion_regulation': emotional_regulation,
            'ei_empathy_understanding': empathy_level,
            'ei_social_skills': social_skills,
            'pmt_threat_vulnerability': threat_vulnerability,
            'pmt_threat_severity': threat_severity,
            'pmt_response_efficacy': response_efficacy,
            'pmt_self_efficacy': self_efficacy,
            'fear_arousal_intensity': fear_arousal,
            'phishing_behavior_pre': behavior_pre_score,
            'phishing_behavior_post': behavior_post_score,
            'social_observational_learning': observational_learning,
            'social_peer_modeling': peer_modeling,
            'social_reinforcement_response': social_reinforcement,
            'trust_in_organization': np.random.randint(1, 8),
            'shame_guilt_response': np.random.randint(1, 8),
            'pride_accomplishment': np.random.randint(1, 8),
            'anger_frustration_level': np.random.randint(1, 8),
            'confidence_reporting': np.random.randint(1, 8),
            'habit_formation_strength': np.random.randint(1, 8),
            'behavioral_persistence_days': np.random.randint(1, 180),
            'relapse_incidents': np.random.randint(0, 8),
            'data_collection_date': datetime.now() - timedelta(days=np.random.randint(1, 120))
        })
    
    return pd.DataFrame(data)

# Generate all three datasets
print("Generating Survey 1: Psychological Stress and Cognitive Load...")
survey1 = generate_survey_1_psychological_stress()

print("Generating Survey 2: Motivational Factors and Attitude Change...")
survey2 = generate_survey_2_motivation_attitude()

print("Generating Survey 3: Emotional Responses and Behavioral Adaptation...")
survey3 = generate_survey_3_emotional_behavioral()

# Save to CSV files
survey1.to_csv('../data/survey_psychological_stress.csv', index=False)
survey2.to_csv('../data/survey_motivation_attitude.csv', index=False)
survey3.to_csv('../data/survey_emotional_behavioral.csv', index=False)

print(f"\nDatasets Generated:")
print(f"Survey 1 (Psychological/Stress): {len(survey1)} records, {len(survey1.columns)} columns")
print(f"Survey 2 (Motivation/Attitude): {len(survey2)} records, {len(survey2.columns)} columns")
print(f"Survey 3 (Emotional/Behavioral): {len(survey3)} records, {len(survey3.columns)} columns")

# Display sample data
print("\n" + "="*80)
print("SURVEY 1 SAMPLE - Psychological Stress & Cognitive Load")
print("="*80)
print(survey1.head(3))

print("\n" + "="*80)
print("SURVEY 2 SAMPLE - Motivational Factors & Attitude Change")
print("="*80)
print(survey2.head(3))

print("\n" + "="*80)
print("SURVEY 3 SAMPLE - Emotional Responses & Behavioral Adaptation")
print("="*80)
print(survey3.head(3))

print("\n" + "="*80)
print("COLUMN ANALYSIS")
print("="*80)
print("\nSurvey 1 Columns:")
for i, col in enumerate(survey1.columns, 1):
    print(f"{i:2d}. {col}")

print("\nSurvey 2 Columns:")
for i, col in enumerate(survey2.columns, 1):
    print(f"{i:2d}. {col}")

print("\nSurvey 3 Columns:")
for i, col in enumerate(survey3.columns, 1):
    print(f"{i:2d}. {col}")