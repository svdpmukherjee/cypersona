"""
Step 3: Test interventions against AI personas

"""

import streamlit as st
import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
import uuid
from datetime import datetime
import together

load_dotenv()

class InterventionTester:
    def __init__(self):
        self.model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        self.together_client = None
        self.together_api_key = os.getenv("TOGETHER_API_KEY")

    def check_api_connection(self):
        """Check if Together AI API is accessible"""
        if not self.together_api_key:
            st.error("🔑 Together AI API key required. Set TOGETHER_API_KEY environment variable.")
            return False
        
        try:
            self.together_client = together.Together(api_key=self.together_api_key)
            return True
        except Exception as e:
            st.error(f"Failed to connect to Together AI: {e}")
            return False

    def test_intervention(self, intervention_description, persona_description, knowledge_base):
        """Test intervention against persona using knowledge base"""
        prompt = f"""
        You are a cybersecurity research expert. Predict intervention outcomes.

        INTERVENTION DESCRIPTION:
        {intervention_description}

        TARGET PERSONA:
        {persona_description}

        RESEARCH KNOWLEDGE BASE:
        {knowledge_base}

        Analyze and predict:
        1. ENGAGEMENT LIKELIHOOD (0-100%): How likely will this persona engage with the intervention?
        2. BEHAVIORAL CHANGE PREDICTION: What specific changes in phishing behavior?
        3. SUCCESS FACTORS: What aspects would work well for this persona?
        4. RESISTANCE FACTORS: What might cause the intervention to fail?
        5. EFFECTIVENESS SCORE (0-10): Overall intervention effectiveness
        6. RECOMMENDATIONS: How to optimize the intervention for this persona?

        Format response as structured analysis with clear sections and specific percentages/scores.
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
                max_tokens=600,
                temperature=0.7,
                stream=False
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

def render_intervention_testing_ui():
    """Linear single page UI for intervention testing"""
    
    st.title("Intervention Testing Lab")
    st.markdown("Test cybersecurity interventions against AI personas using research-backed predictions")
    
    # Check prerequisites
    if not st.session_state.get('processing_complete', False):
        st.warning("⚠️ Complete Step 1 data processing first")
        return
    
    if not st.session_state.get('generated_personas', []):
        st.warning("⚠️ Generate personas in Step 2 first")
        return
    
    if not os.getenv("TOGETHER_API_KEY"):
        st.error("🔑 Together AI API key required. Configure in main app sidebar.")
        return
    
    tester = InterventionTester()
    
    # Initialize test results
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    
    # SECTION 1: Design Intervention
    st.markdown("## 1. Design Your Intervention")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        intervention_text = st.text_area(
            "Describe Your Intervention:",
            placeholder="Example: A gamified phishing training program where employees earn points for correctly identifying and reporting phishing emails. The program includes weekly challenges, leaderboards, and rewards for top performers. Training modules use interactive scenarios based on real attack patterns.",
            height=120,
            help="Be specific about content, delivery method, and expected outcomes"
        )
        
        # Quick intervention parameters
        param_col1, param_col2, param_col3 = st.columns(3)
        
        with param_col1:
            intervention_type = st.selectbox("Type", [
                "Training Program", "Awareness Campaign", "Technical Control",
                "Policy Change", "Gamification", "Social Engineering Defense"
            ])
        
        with param_col2:
            target_behavior = st.selectbox("Target", [
                "Phishing Recognition", "Reporting Behavior", "Security Awareness",
                "Risk Assessment", "Help-Seeking", "General Security Habits"
            ])
        
        with param_col3:
            delivery_method = st.selectbox("Delivery", [
                "Online Training", "In-Person Workshop", "Email Campaign",
                "Mobile App", "Peer-to-Peer", "Manager-Led"
            ])
    
    with col2:
        st.markdown("**Knowledge Base Context**")
        kb_summary = st.text_area("Research Context:", 
            value="Research shows 22% average click rate, executives 6%, admin 22%. Time pressure increases risk 40%. Training reduces susceptibility 30%.",
            height=120,
            help="This context will inform the AI predictions")
    
    # SECTION 2: Select Personas
    st.markdown("---")
    st.markdown("## 2. Select Target Personas")
    
    # Persona selection with preview
    persona_options = {p['id']: f"{p['name']} ({p['industry']})" 
                     for p in st.session_state.generated_personas}
    
    selected_personas = st.multiselect(
        "Choose personas to test against:",
        list(persona_options.keys()),
        format_func=lambda x: persona_options[x],
        help="Select one or more personas for testing"
    )
    
    # Show selected persona previews
    if selected_personas:
        st.markdown("**Selected Personas Preview:**")
        for persona_id in selected_personas:
            persona = next(p for p in st.session_state.generated_personas if p['id'] == persona_id)
            with st.expander(f"📄 {persona['name']} ({persona['industry']})", expanded=False):
                # Show first 200 characters of persona description
                preview_text = persona['llm_output'][:200] + "..." if len(persona['llm_output']) > 200 else persona['llm_output']
                st.write(preview_text)
    
    # SECTION 3: Run Tests
    st.markdown("---")
    st.markdown("## 3. Execute Tests")
    
    # Test execution interface
    can_run_test = bool(intervention_text.strip() and selected_personas)
    
    if not can_run_test:
        if not intervention_text.strip():
            st.info("💡 Describe your intervention above to enable testing")
        elif not selected_personas:
            st.info("💡 Select personas to test against")
    else:
        st.markdown("**Ready to Test:**")
        st.info(f"Intervention: {intervention_text[:100]}{'...' if len(intervention_text) > 100 else ''}")
        st.info(f"Target Personas: {len(selected_personas)} selected")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Run Intervention Tests", type="primary", use_container_width=True):
                with st.spinner("Running AI-powered intervention analysis..."):
                    
                    # Create test record
                    test_id = str(uuid.uuid4())[:8]
                    test_results = {
                        'test_id': test_id,
                        'intervention': intervention_text,
                        'intervention_type': intervention_type,
                        'target_behavior': target_behavior,
                        'delivery_method': delivery_method,
                        'personas_tested': len(selected_personas),
                        'results': {},
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Run tests for each persona
                    for i, persona_id in enumerate(selected_personas):
                        persona = next(p for p in st.session_state.generated_personas if p['id'] == persona_id)
                        
                        # Update progress
                        progress = (i + 1) / len(selected_personas)
                        progress_bar.progress(progress)
                        status_text.text(f"Testing against {persona['name']}... ({i+1}/{len(selected_personas)})")
                        
                        # Run prediction
                        result = tester.test_intervention(
                            intervention_text,
                            persona['description'] + "\n" + persona['llm_output'],
                            kb_summary
                        )
                        
                        test_results['results'][persona_id] = {
                            'persona_name': persona['name'],
                            'persona_industry': persona['industry'],
                            'prediction': result
                        }
                    
                    # Complete
                    progress_bar.progress(1.0)
                    status_text.text("Analysis complete!")
                    
                    # Store results
                    st.session_state.test_results.append(test_results)
                    
                    st.success(f"✅ Tests completed! Test ID: {test_id}")
                    st.balloons()
                    
                    # Auto-scroll to results
                    st.session_state.show_latest_results = True
        
        with col2:
            # Test settings
            st.markdown("**Settings**")
            confidence_level = st.selectbox("Confidence", 
                ["Standard", "Detailed", "Quick"], index=0)
    
    # SECTION 4: Results
    st.markdown("---")
    st.markdown("## 4. Test Results")
    
    if not st.session_state.test_results:
        st.info("No test results yet. Run some tests above to see predictions here.")
    else:
        # Show latest results first if just completed
        if st.session_state.get('show_latest_results', False):
            latest_test = st.session_state.test_results[-1]
            st.session_state.selected_test_id = latest_test['test_id']
            st.session_state.show_latest_results = False
        
        # Test selection
        test_options = {r['test_id']: f"{r['test_id']} - {r['intervention_type']} ({r['personas_tested']} personas) - {r['timestamp'][:10]}" 
                       for r in st.session_state.test_results}
        
        selected_test = st.selectbox(
            "Select test results to view:", 
            list(test_options.keys()),
            format_func=lambda x: test_options[x],
            index=len(test_options)-1 if st.session_state.get('selected_test_id') else 0
        )
        
        if selected_test:
            test_data = next(r for r in st.session_state.test_results if r['test_id'] == selected_test)
            
            # Test overview metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Test ID", test_data['test_id'])
            with col2:
                st.metric("Type", test_data['intervention_type'])
            with col3:
                st.metric("Personas", test_data['personas_tested'])
            with col4:
                st.metric("Date", test_data['timestamp'][:10])
            
            # Intervention summary
            st.markdown("**Tested Intervention:**")
            st.info(test_data['intervention'])
            
            # Results display
            st.markdown("**Prediction Results:**")
            
            for persona_id, result_data in test_data['results'].items():
                with st.expander(f"{result_data['persona_name']} ({result_data['persona_industry']})", expanded=True):
                    st.write(result_data['prediction'])
            
            # Export functionality
            st.markdown("**Export Results:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # JSON export
                results_json = json.dumps(test_data, indent=2)
                st.download_button(
                    "📄 Export JSON",
                    results_json,
                    f"test_results_{test_data['test_id']}.json",
                    "application/json",
                    use_container_width=True
                )
            
            with col2:
                # CSV export
                csv_data = []
                for persona_id, result in test_data['results'].items():
                    csv_data.append({
                        'Test_ID': test_data['test_id'],
                        'Persona': result['persona_name'],
                        'Industry': result['persona_industry'],
                        'Intervention_Type': test_data['intervention_type'],
                        'Result_Length': len(result['prediction']),
                        'Date': test_data['timestamp'][:10]
                    })
                
                csv_df = pd.DataFrame(csv_data)
                csv_string = csv_df.to_csv(index=False)
                
                st.download_button(
                    "📊 Export CSV",
                    csv_string,
                    f"test_summary_{test_data['test_id']}.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col3:
                # Delete test
                if st.button("🗑️ Delete Test", use_container_width=True):
                    if st.checkbox(f"Confirm delete test {test_data['test_id']}", key=f"delete_{test_data['test_id']}"):
                        st.session_state.test_results = [
                            r for r in st.session_state.test_results if r['test_id'] != selected_test
                        ]
                        st.success("Test results deleted!")
                        st.rerun()
    
    # SECTION 5: Test History Summary
    if len(st.session_state.test_results) > 1:
        st.markdown("---")
        st.markdown("## 📋 5. Test History Summary")
        
        # Create summary table
        history_data = []
        for test in st.session_state.test_results:
            history_data.append({
                'Test ID': test['test_id'],
                'Type': test['intervention_type'],
                'Target': test.get('target_behavior', 'N/A'),
                'Personas': test['personas_tested'],
                'Date': test['timestamp'][:10],
                'Time': test['timestamp'][11:16]
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        # History actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        with col2:
            # Export all history
            all_history_json = json.dumps(st.session_state.test_results, indent=2)
            st.download_button(
                "📦 Export All",
                all_history_json,
                f"all_test_results_{datetime.now().strftime('%Y%m%d')}.json",
                "application/json"
            )
        
        with col3:
            if st.button("🗑️ Clear All"):
                if st.checkbox("Confirm clear all test history"):
                    st.session_state.test_results = []
                    st.success("All test history cleared!")
                    st.rerun()

if __name__ == "__main__":
    render_intervention_testing_ui()