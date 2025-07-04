"""
Step 2: Simplified AI-Powered Persona Generation
Single page view using Together AI with Llama 3.1 8B and vector knowledge base
"""

import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import together
import plotly.express as px

class PersonaGenerator:
    def __init__(self):
        self.model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        self.together_client = None
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        
    def check_api_connection(self):
        """Check if Together AI API is accessible"""
        if not self.together_api_key:
            return False
        
        try:
            self.together_client = together.Together(api_key=self.together_api_key)
            return True
        except Exception as e:
            st.error(f"API connection failed: {e}")
            return False
    
    def query_knowledge_base(self, query, vector_db):
        """Query the vector knowledge base for relevant context"""
        if vector_db and hasattr(vector_db, 'query'):
            results = vector_db.query(query, top_k=5)
            context = "\n".join([result['text'] for result in results])
            return context
        return "No knowledge base available"
    
    def generate_persona_from_description(self, description, knowledge_context):
        """Generate detailed persona using Llama 3.1 8B with knowledge base context"""
        prompt = f"""
Based on cybersecurity research data, create a detailed persona:

RESEARCH CONTEXT:
{knowledge_context}

USER REQUEST: "{description}"

Generate a comprehensive persona with:
1. BASIC PROFILE:
   - Name, age, role, experience level
   - Industry and department
   - Technical background

2. BEHAVIORAL TRAITS (rate 0-10):
   - Phishing susceptibility: X/10
   - Security awareness: X/10  
   - Reporting likelihood: X/10
   - Stress response: X/10
   - Training receptiveness: X/10

3. PSYCHOLOGICAL PROFILE:
   - Risk tolerance and decision-making style
   - Stress triggers and coping mechanisms
   - Motivation factors and communication preferences

4. TYPICAL BEHAVIORS:
   - Email handling patterns
   - Security practices and habits
   - Response to training and warnings

5. VULNERABILITIES & STRENGTHS:
   - Key security weaknesses
   - Natural protective behaviors
   - Potential improvement areas

Format as structured text, not JSON. Be specific and realistic based on the research context provided.
        """
        
        return self._query_llm(prompt)

    def _query_llm(self, prompt):
        """Query Together AI LLM"""
        if not self.together_client:
            if not self.check_api_connection():
                return "API connection failed"
        
        try:
            response = self.together_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7,
                stream=False
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

def render_persona_generation_ui():
    """Simplified single-page persona generation UI"""
    
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
        
        # Natural language input
        persona_description = st.text_area(
            "Describe the persona you want to create:",
            placeholder="Example: Create a persona for a busy healthcare administrator in their 40s who is moderately tech-savvy but often rushes through emails due to workload pressure and has limited cybersecurity training.",
            height=120,
            help="Be specific about role, industry, experience level, and behavioral characteristics"
        )
        
        # Parameters row
        param_col1, param_col2, param_col3 = st.columns(3)
        
        with param_col1:
            industry = st.selectbox("Industry Context", 
                ["Healthcare", "Finance", "Education", "Technology", "Government", "Any"])
        
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
                if vector_db:
                    # Query knowledge base for relevant context
                    knowledge_context = generator.query_knowledge_base(
                        f"{persona_description} {industry} cybersecurity behavior", 
                        vector_db
                    )
                else:
                    knowledge_context = "Knowledge base not available - using general cybersecurity patterns"
                
                # Show context being used
                with st.expander("Knowledge Base Context Used", expanded=False):
                    st.text_area("Research context:", knowledge_context, height=100, disabled=True)
                
                # Generate personas
                for i in range(persona_count):
                    # Generate persona
                    persona_response = generator.generate_persona_from_description(
                        persona_description, knowledge_context
                    )
                    
                    # Create persona object
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
                fig = px.pie(
                    values=industry_counts.values, 
                    names=industry_counts.index,
                    title="Distribution by Industry"
                )
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
            if st.button("Export All", use_container_width=True):
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
    
    # Generated Personas Display
    if st.session_state.generated_personas:
        st.markdown("---")
        st.subheader("Generated Personas")
        
        # Persona selection and actions
        persona_options = {p['id']: f"{p['name']} ({p['industry']}) - {p['generated_at'][:10]}" 
                          for p in st.session_state.generated_personas}
        
        selected_persona_id = st.selectbox(
            "Select persona to view/edit:", 
            list(persona_options.keys()),
            format_func=lambda x: persona_options[x],
            key="persona_selector"
        )
        
        if selected_persona_id:
            persona = next(p for p in st.session_state.generated_personas if p['id'] == selected_persona_id)
            
            # Persona details in columns
            detail_col1, detail_col2 = st.columns([3, 1])
            
            with detail_col1:
                # Editable name
                new_name = st.text_input("Persona Name:", persona['name'], key=f"name_{persona['id']}")
                if new_name != persona['name']:
                    persona['name'] = new_name
                
                # Original description
                st.markdown("**Original Request:**")
                st.info(persona['description'])
                
                # Display persona profile with edit capability
                st.markdown("**Persona Profile:**")
                
                # Edit toggle
                edit_mode = st.toggle("Edit Mode", key=f"edit_{persona['id']}")
                
                if edit_mode:
                    # Editable text area
                    edited_profile = st.text_area(
                        "Edit Profile:",
                        value=persona['llm_output'],
                        height=400,
                        key=f"edit_profile_{persona['id']}"
                    )
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("💾 Save Changes", key=f"save_{persona['id']}"):
                            persona['llm_output'] = edited_profile
                            st.success("Profile updated!")
                            st.rerun()
                    
                    with col_cancel:
                        if st.button("↩️ Revert", key=f"revert_{persona['id']}"):
                            st.rerun()
                else:
                    # Display full profile
                    st.write(persona['llm_output'])
                
                # Knowledge context used
                with st.expander("Research Context Used", expanded=False):
                    st.write(persona.get('knowledge_context', 'No context available'))
            
            
            with detail_col2:
                st.markdown("**Actions**")
                
                # Clone persona
                if st.button("📋 Clone", use_container_width=True):
                    cloned = persona.copy()
                    cloned['id'] = str(uuid.uuid4())[:8]
                    cloned['name'] = f"{persona['name']} (Copy)"
                    cloned['generated_at'] = datetime.now().isoformat()
                    st.session_state.generated_personas.append(cloned)
                    st.success("Persona cloned!")
                    st.rerun()
                
                # Delete persona
                if st.button("🗑️ Delete", use_container_width=True):
                    if st.checkbox(f"Confirm delete {persona['name']}", key=f"delete_{persona['id']}"):
                        st.session_state.generated_personas = [
                            p for p in st.session_state.generated_personas if p['id'] != selected_persona_id
                        ]
                        st.success("Persona deleted!")
                        st.rerun()
                
                # Export single persona
                persona_json = json.dumps(persona, indent=2)
                st.download_button(
                    "📤 Export",
                    persona_json,
                    f"persona_{persona['id']}.json",
                    "application/json",
                    use_container_width=True
                )
                
                # Metadata
                st.markdown("**Metadata**")
                st.caption(f"ID: {persona['id']}")
                st.caption(f"Created: {persona['generated_at'][:16]}")
                st.caption(f"Industry: {persona['industry']}")
                st.caption(f"Detail: {persona.get('complexity', 'Standard')}")
    
    # Next step navigation
    if st.session_state.generated_personas:
        st.markdown("---")
        st.subheader("Next Step")
        if st.button("Go to Intervention Testing", type="primary", use_container_width=True):
            st.session_state.current_page = "Intervention Testing"
            st.rerun()

if __name__ == "__main__":
    render_persona_generation_ui()