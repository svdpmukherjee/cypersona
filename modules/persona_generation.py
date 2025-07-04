"""
Step 2: AI-Powered Persona Generation

"""

import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import together
import plotly.express as px
import base64
from pathlib import Path

class PersonaGenerator:
    def __init__(self):
        self.model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        self.together_client = None
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        
    def check_api_connection(self):
        if not self.together_api_key:
            return False
        try:
            self.together_client = together.Together(api_key=self.together_api_key)
            return True
        except Exception as e:
            st.error(f"API connection failed: {e}")
            return False
    
    def query_knowledge_base(self, query, vector_db):
        if vector_db and hasattr(vector_db, 'query'):
            results = vector_db.query(query, top_k=5)
            return "\n".join([result['text'] for result in results])
        return "No knowledge base available"
    
    def generate_persona_from_description(self, description, knowledge_context):
        prompt = f"""
Create a cybersecurity persona based on research data. Be SPECIFIC and ACTIONABLE, avoid generic statements.

RESEARCH CONTEXT:
{knowledge_context}

USER REQUEST: "{description}"

Generate this exact structure:

1. BASIC PROFILE:
Create a realistic name, age (25-55), specific job title, and 2-4 years experience. Add one specific personality trait that affects security behavior.

2. BEHAVIORAL SCORES:
Rate each 0-10 with ONE specific reason:
- Phishing Susceptibility: X/10 (specific vulnerability reason)
- Security Awareness: X/10 (specific knowledge gap/strength)  
- Reporting Likelihood: X/10 (specific behavioral reason)
- Stress Response: X/10 (specific stress trigger)
- Training Receptiveness: X/10 (specific learning preference)

3. KEY VULNERABILITIES:
• One primary technical/procedural weakness
• One cognitive bias or emotional trigger  
• One workplace pressure that compromises security

4. PROTECTIVE BEHAVIORS:
• One natural security strength they already have
• One positive habit that helps security
• One way they seek help when uncertain

5. INTERVENTION RECOMMENDATIONS:
Design a SPECIFIC intervention for THIS persona:
• Exact communication style (formal/casual, email/face-to-face, etc.)
• Specific training format (micro-learning, hands-on, gamified, etc.)
• Precise timing and delivery method
• One concrete intervention example that would work for them

Make every detail specific to this persona's role, industry, and psychology. No generic advice.
        """
        return self._query_llm(prompt)

    def _query_llm(self, prompt):
        if not self.together_client and not self.check_api_connection():
            return "API connection failed"
        
        try:
            response = self.together_client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

def parse_persona_content(llm_output):
    """Parse LLM output into structured components with better section detection"""
    sections = {'basic_profile': '', 'behavioral_scores': '', 'vulnerabilities': '', 
               'protective_behaviors': '', 'recommendations': ''}
    
    current_section = None
    lines = llm_output.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect section headers with more specific patterns
        line_upper = line.upper()
        if ('BASIC PROFILE' in line_upper or line_upper.startswith('1.')) and 'BASIC' in line_upper:
            current_section = 'basic_profile'
            continue
        elif ('BEHAVIORAL SCORE' in line_upper or line_upper.startswith('2.')) and ('BEHAVIORAL' in line_upper or 'SCORE' in line_upper):
            current_section = 'behavioral_scores'
            continue
        elif ('VULNERABILITIES' in line_upper or line_upper.startswith('3.')) and 'VULNERABILITIES' in line_upper:
            current_section = 'vulnerabilities'
            continue
        elif ('PROTECTIVE' in line_upper or 'BEHAVIORS' in line_upper or line_upper.startswith('4.')) and ('PROTECTIVE' in line_upper or 'BEHAVIORS' in line_upper):
            current_section = 'protective_behaviors'
            continue
        elif ('RECOMMENDATION' in line_upper or 'INTERVENTION' in line_upper or line_upper.startswith('5.')) and ('RECOMMENDATION' in line_upper or 'INTERVENTION' in line_upper):
            current_section = 'recommendations'
            continue
        
        # Add content to current section
        if current_section:
            sections[current_section] += line + '\n'
    
    return sections

def get_persona_image_base64(gender):
    """Get base64 encoded image for persona display"""
    import random
    
    try:
        # Look for variation files
        variations = []
        for i in range(1, 5):
            for ext in ['.png', '.jpg', '.jpeg']:
                image_path = Path(f"images/{gender}_{i}{ext}")
                if image_path.exists():
                    variations.append(image_path)
        
        if variations:
            selected_image = random.choice(variations)
            with open(selected_image, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        
        # Fallback
        for ext in ['.png', '.jpg', '.jpeg']:
            image_path = Path(f"images/{gender}_persona{ext}")
            if image_path.exists():
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        return None
    except Exception:
        return None

def create_gradient_avatar(gender):
    """Create CSS gradient avatar as fallback"""
    if gender == 'female':
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        emoji = "👩‍💼"
    else:
        gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        emoji = "👨‍💼"
    
    return f"""
    <div class="persona-avatar" style="
        background: {gradient}; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        font-size: 50px;
        color: white;
        font-weight: bold;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 0 auto 20px auto;
        border: 4px solid #007bff;
        box-shadow: 0 8px 25px rgba(0,123,255,0.3);
    ">{emoji}</div>
    """

def get_card_css():
    """Return CSS styles for persona cards"""
    return """
    <style>
    .persona-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px; padding: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef; margin-bottom: 25px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .persona-header {
        text-align: center; margin-bottom: 30px; padding-bottom: 20px;
        border-bottom: 2px solid #f1f3f4;
    }
    .persona-avatar {
        width: 120px; height: 120px; border-radius: 50%;
        margin: 0 auto 20px auto; border: 4px solid #007bff;
        box-shadow: 0 8px 25px rgba(0,123,255,0.3); object-fit: cover; display: block;
    }
    .persona-name {
        font-size: 32px; font-weight: 700; color: #2c3e50;
        margin-bottom: 8px; text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .persona-role {
        font-size: 18px; color: #6c757d; font-style: italic; font-weight: 500;
    }
    .section-header {
        font-size: 20px; font-weight: 700; color: #495057;
        margin: 25px 0 15px 0; padding: 10px 15px;
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        border-radius: 10px; border-left: 5px solid #007bff; display: flex; align-items: center;
    }
    .section-content {
        background: #f8f9fa; padding: 20px; border-radius: 12px;
        font-size: 15px; line-height: 1.7; border: 1px solid #e9ecef; margin-bottom: 20px;
    }
    .behavioral-scores {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px; margin: 15px 0;
    }
    .score-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px; border-radius: 12px; color: white; text-align: center;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    .score-label {
        font-weight: 600; font-size: 13px; margin-bottom: 5px; opacity: 0.9;
    }
    .score-value {
        font-size: 28px; font-weight: 800; margin-bottom: 5px;
    }
    .score-reason {
        font-size: 11px; opacity: 0.8; font-style: italic;
    }
    .vulnerability-section {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 20px; border-radius: 12px; border-left: 5px solid #e17055; margin: 15px 0;
    }
    .strength-section {
        background: linear-gradient(135deg, #a8e6cf 0%, #81c784 100%);
        padding: 20px; border-radius: 12px; border-left: 5px solid #4caf50; margin: 15px 0;
    }
    .recommendation-section {
        background: linear-gradient(135deg, #ddd6fe 0%, #c084fc 100%);
        padding: 20px; border-radius: 12px; border-left: 5px solid #8b5cf6; margin: 15px 0;
    }
    .icon { font-size: 24px; margin-right: 12px; }
    </style>
    """

def render_persona_card(persona):
    """Render beautiful persona card with enhanced styling"""
    parsed = parse_persona_content(persona['llm_output'])
    
    # Extract name
    basic_profile = parsed['basic_profile'].strip()
    extracted_name = None
    if basic_profile:
        for line in basic_profile.split('\n'):
            # Look for patterns like "Name: Dr. Sarah Johnson" or "Dr. Sarah Johnson"
            if 'name' in line.lower() and ':' in line:
                name_part = line.split(':')[-1].strip()
                words = name_part.split()
            else:
                words = line.split()
            
            # Extract full name including titles
            name_parts = []
            for i, word in enumerate(words):
                clean_word = word.rstrip('.,').strip()
                if clean_word and (clean_word.istitle() or clean_word.startswith('Dr') or clean_word.startswith('Mr') or clean_word.startswith('Ms')):
                    name_parts.append(clean_word)
                    # Continue collecting until we hit a non-name word
                    if len(name_parts) >= 3:  # Title + First + Last is enough
                        break
                elif name_parts:  # If we started collecting names but hit a non-name, stop
                    break
            
            if len(name_parts) >= 2:  # At least first and last name
                extracted_name = ' '.join(name_parts)
                break
    
    display_name = extracted_name or persona['name']
    
    # Determine gender
    female_names = ['Sarah', 'Maria', 'Jennifer', 'Lisa', 'Michelle', 'Amanda', 'Jessica', 
                   'Rachel', 'Emily', 'Ashley', 'Anna', 'Patricia', 'Laura', 'Elizabeth', 'Karen']
    gender = 'female' if any(name in display_name for name in female_names) else 'male'
    
    # Get image or create avatar
    img_base64 = get_persona_image_base64(gender)
    avatar_html = (f'<img src="data:image/png;base64,{img_base64}" class="persona-avatar" alt="{display_name}">' 
                  if img_base64 else create_gradient_avatar(gender))
    
    # Parse behavioral scores
    scores_html = ""
    if parsed['behavioral_scores']:
        score_lines = [line.strip() for line in parsed['behavioral_scores'].split('\n') 
                      if line.strip() and ('/' in line or 'score' in line.lower())]
        
        if score_lines:
            scores_html = '<div class="behavioral-scores">'
            for line in score_lines[:5]:
                if '/' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        label = parts[0].strip().replace('-', '').replace('•', '').strip()
                        rest = parts[1].strip()
                        score_match = rest.split('(')
                        score = score_match[0].strip()
                        reason = score_match[1].replace(')', '').strip() if len(score_match) > 1 else "See profile"
                        
                        scores_html += f'''
                        <div class="score-item">
                            <div class="score-label">{label}</div>
                            <div class="score-value">{score}</div>
                            <div class="score-reason">{reason}</div>
                        </div>
                        '''
            scores_html += '</div>'
    
    # Build card HTML
    card_html = f"""
    {get_card_css()}
    <div class="persona-card">
        <div class="persona-header">
            {avatar_html}
            <div class="persona-name">{display_name}</div>
            <div class="persona-role">{persona['industry']} Professional</div>
        </div>
        
        <div class="section-header">
            <span class="icon">👤</span>Profile Overview
        </div>
        <div class="section-content">
            {basic_profile if basic_profile else "Profile information not available"}
        </div>
    """
    
    if scores_html:
        card_html += f"""
        <div class="section-header">Behavioral Assessment</div>
        {scores_html}
        """
    
    if parsed['vulnerabilities']:
        card_html += f"""
        <div class="section-header"><span class="icon">⚠️</span>Key Vulnerabilities</div>
        <div class="vulnerability-section">{parsed['vulnerabilities']}</div>
        """
    
    if parsed['protective_behaviors']:
        card_html += f"""
        <div class="section-header"><span class="icon">🛡️</span>Protective Behaviors</div>
        <div class="strength-section">{parsed['protective_behaviors']}</div>
        """
    
    if parsed['recommendations']:
        card_html += f"""
        <div class="section-header"><span class="icon">💡</span>Targeted Intervention Strategy</div>
        <div class="recommendation-section">
            <strong>Personalized Approach:</strong><br>
            {parsed['recommendations']}
        </div>
        """
    
    return card_html + "</div>"

def render_persona_generation_ui():
    """Enhanced persona generation UI with beautiful cards"""
    
    st.title("STEP 2: AI Persona Generation")
    st.markdown("Create realistic cybersecurity personas using natural language and research data")
    
    # Check prerequisites
    if not st.session_state.get('processing_complete', False):
        st.warning("⚠️ Complete Step 1 data processing first")
        return
    
    if not os.getenv("TOGETHER_API_KEY"):
        st.error("🔑 Together AI API key not configured. Please set it in the main app sidebar.")
        return
    
    generator = PersonaGenerator()
    
    # Initialize session state
    if 'generated_personas' not in st.session_state:
        st.session_state.generated_personas = []
    
    # Main content in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Create New Persona")
        
        persona_description = st.text_area(
            "Describe the persona you want to create:",
            placeholder="Example: Create a persona for a busy research scientist in their early 40s who is moderately tech-savvy but often rushes through emails due to workload pressure and has limited cybersecurity training.",
            height=120,
            help="Be specific about role, industry, experience level, and behavioral characteristics"
        )
        
        # Parameters row
        param_col1, param_col2, param_col3 = st.columns(3)
        
        with param_col1:
            industry = st.selectbox("Industry Context", 
                ["Education", "Finance", "Healthcare", "Technology", "Government", "Any"])
        with param_col2:
            complexity = st.selectbox("Behavioral Detail", 
                ["Basic", "Detailed", "Comprehensive"])
        with param_col3:
            persona_count = st.number_input("Generate", 1, 3, 1, help="Number of persona variants")
        
        # Generate button
        if st.button("Generate Persona(s)", type="primary", use_container_width=True):
            if not persona_description.strip():
                st.error("Please provide a persona description")
                return
                
            with st.spinner("Creating AI persona using research knowledge..."):
                # Get knowledge base context
                vector_db = st.session_state.get('vector_knowledge_base')
                knowledge_context = generator.query_knowledge_base(
                    f"{persona_description} {industry} cybersecurity behavior", 
                    vector_db
                ) if vector_db else "Knowledge base not available - using general cybersecurity patterns"
                
                # Show context being used
                with st.expander("Knowledge Base Context Used", expanded=False):
                    st.text_area("Research context:", knowledge_context, height=100, disabled=True)
                
                # Generate personas
                for i in range(persona_count):
                    persona_response = generator.generate_persona_from_description(
                        persona_description, knowledge_context
                    )
                    
                    persona = {
                        'id': str(uuid.uuid4())[:8],
                        'name': f"Persona {len(st.session_state.generated_personas) + 1}",
                        'description': persona_description,
                        'generated_at': datetime.now().isoformat(),
                        'llm_output': persona_response,
                        'industry': industry,
                        'complexity': complexity,
                        'knowledge_context': knowledge_context[:500] + "..." if len(knowledge_context) > 500 else knowledge_context
                    }
                    
                    st.session_state.generated_personas.append(persona)
                
                st.success(f"✅ Generated {persona_count} persona(s)!")
                st.rerun()
    
    with col2:
        st.subheader("Current Personas")
        
        if not st.session_state.generated_personas:
            st.info("No personas created yet")
        else:
            # Quick stats
            total_personas = len(st.session_state.generated_personas)
            industries = [p['industry'] for p in st.session_state.generated_personas]
            unique_industries = len(set(industries))
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Total", total_personas)
            with metric_col2:
                st.metric("Industries", unique_industries)
            
            # Industry distribution chart
            if total_personas > 1:
                industry_counts = pd.Series(industries).value_counts()
                fig = px.pie(values=industry_counts.values, names=industry_counts.index,
                           title="Distribution by Industry")
                fig.update_layout(height=250, margin=dict(t=30, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🔄 Clear All", use_container_width=True):
            if st.checkbox("Confirm clearing all personas"):
                st.session_state.generated_personas = []
                st.success("All personas cleared!")
                st.rerun()
        
        if st.session_state.generated_personas:
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_personas': len(st.session_state.generated_personas),
                'personas': st.session_state.generated_personas
            }
            export_json = json.dumps(export_data, indent=2)
            st.download_button(
                "Download JSON",
                export_json,
                f"cypersona_export_{datetime.now().strftime('%Y%m%d')}.json",
                "application/json",
                use_container_width=True
            )
    
    # Generated Personas Display - Enhanced Cards
    if st.session_state.generated_personas:
        st.markdown("---")
        st.subheader("Generated Personas")
        
        persona_options = {p['id']: f"{p['name']} ({p['industry']}) - {p['generated_at'][:10]}" 
                          for p in st.session_state.generated_personas}
        
        selected_persona_id = st.selectbox(
            "Select persona to view/edit:", 
            list(persona_options.keys()),
            format_func=lambda x: persona_options[x]
        )
        
        if selected_persona_id:
            persona = next(p for p in st.session_state.generated_personas if p['id'] == selected_persona_id)
            
            # Display the beautiful persona card
            card_html = render_persona_card(persona)
            st.components.v1.html(card_html, height=1000, scrolling=True)
            
            # Action buttons
            action_col1, action_col2, action_col3, action_col4 = st.columns(4)
            
            with action_col1:
                new_name = st.text_input("Edit Name:", persona['name'])
                if new_name != persona['name']:
                    persona['name'] = new_name
                    st.rerun()
            
            with action_col2:
                if st.button("📋 Clone", use_container_width=True):
                    cloned = persona.copy()
                    cloned['id'] = str(uuid.uuid4())[:8]
                    cloned['name'] = f"{persona['name']} (Copy)"
                    cloned['generated_at'] = datetime.now().isoformat()
                    st.session_state.generated_personas.append(cloned)
                    st.success("Persona cloned!")
                    st.rerun()
            
            with action_col3:
                persona_json = json.dumps(persona, indent=2)
                st.download_button(
                    "📤 Export",
                    persona_json,
                    f"persona_{persona['id']}.json",
                    "application/json",
                    use_container_width=True
                )
            
            with action_col4:
                if st.button("🗑️ Delete", use_container_width=True):
                    if st.checkbox(f"Confirm delete {persona['name']}"):
                        st.session_state.generated_personas = [
                            p for p in st.session_state.generated_personas if p['id'] != selected_persona_id
                        ]
                        st.success("Persona deleted!")
                        st.rerun()
            
            # Advanced editing section
            with st.expander("Advanced Editing", expanded=False):
                st.markdown("**Edit Raw Persona Data:**")
                
                edited_profile = st.text_area(
                    "Edit Profile:",
                    value=persona['llm_output'],
                    height=300
                )
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 Save Changes"):
                        persona['llm_output'] = edited_profile
                        st.success("Profile updated!")
                        st.rerun()
                
                with col_cancel:
                    if st.button("↩️ Revert"):
                        st.rerun()
                
                # Show metadata
                st.markdown(f"""
                **Metadata:**
                - ID: {persona['id']}
                - Created: {persona['generated_at'][:16]}
                - Industry: {persona['industry']}
                - Complexity: {persona.get('complexity', 'Standard')}
                """)
    
    # Next step navigation
    if st.session_state.generated_personas:
        st.markdown("---")
        if st.button("Go to Intervention Testing", type="primary", use_container_width=True):
            st.session_state.current_page = "Intervention Testing"
            st.rerun()

if __name__ == "__main__":
    render_persona_generation_ui()