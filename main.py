"""
CyPersona: AI-Powered Cybersecurity Persona Generation
Main application entry point for Streamlit web app
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add both root and modules directory to Python path
root_dir = Path(__file__).parent
modules_dir = root_dir / "modules"
sys.path.append(str(root_dir))
sys.path.append(str(modules_dir))

# Import page modules
try:
    import importlib.util
    
    # Dynamic import of modules
    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    # Load modules dynamically (avoid name conflicts with Streamlit)
    dp_module = load_module("data_pipeline_mod", "modules/data_pipeline.py")
    pg_module = load_module("persona_generation_mod", "modules/persona_generation.py")
    it_module = load_module("intervention_testing_mod", "modules/intervention_testing.py")
    
    # Get the render functions
    render_step1_ui = getattr(dp_module, 'render_step1_ui', None)
    render_persona_generation_ui = getattr(pg_module, 'render_persona_generation_ui', None)
    render_intervention_testing_ui = getattr(it_module, 'render_intervention_testing_ui', None)
    
    # Check if functions exist
    if not render_step1_ui:
        st.error("Function 'render_step1_ui' not found in data_pipeline.py")
        st.stop()
    if not render_persona_generation_ui:
        st.error("Function 'render_persona_generation_ui' not found in persona_generation.py")
        st.stop()
    if not render_intervention_testing_ui:
        st.error("Function 'render_intervention_testing_ui' not found in intervention_testing.py")
        st.stop()
    
except Exception as e:
    st.error(f"Error loading modules: {e}")
    st.info("Check that all Python files are valid and functions are defined correctly")
    st.stop()

def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title="CyPersona - AI-based Data Driven Personas",
        page_icon="👥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'generated_personas' not in st.session_state:
        st.session_state.generated_personas = []
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    
    # Sidebar navigation
    with st.sidebar:
        # st.title("CyPersona")
        # st.markdown("AI-Powered Cybersecurity Persona Generation")
        
        # API Configuration section
        with st.expander("🔑 API Configuration", expanded=not (os.getenv("TOGETHER_API_KEY") and os.getenv("OPENAI_API_KEY"))):
            # Together AI API Key
            together_key = st.text_input(
                "Together AI API Key",
                type="password",
                value=os.getenv("TOGETHER_API_KEY", ""),
                help="Get your API key from https://api.together.ai/"
            )
            
            # OpenAI API Key  
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password", 
                value=os.getenv("OPENAI_API_KEY", ""),
                help="Required for embeddings and vector search. Get from https://platform.openai.com/"
            )
            
            # Set environment variables
            if together_key:
                os.environ["TOGETHER_API_KEY"] = together_key
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
            
            # Status indicators
            col1, col2 = st.columns(2)
            with col1:
                if together_key:
                    st.success("✅ Together AI configured")
                else:
                    st.warning("⚠️ Together AI key needed")
            
            with col2:
                if openai_key:
                    st.success("✅ OpenAI configured") 
                else:
                    st.warning("⚠️ OpenAI key needed")
        
        st.markdown("---")
        
        # Navigation
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Overview"
        
        page = st.selectbox(
            "Navigate to:",
            ["Overview", "Data Processing", "Persona Generation", "Intervention Testing"],
            index=["Overview", "Data Processing", "Persona Generation", "Intervention Testing"].index(st.session_state.current_page)
        )
        
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.rerun()
        
        st.markdown("---")
        
        # Pipeline status indicators
        st.markdown("### Pipeline Status")
        
        # Step 1 status
        if st.session_state.processing_complete:
            st.success("✅ Step 1: Data Processing")
        else:
            st.info("Step 1: Data Processing")
        
        # Step 2 status
        if st.session_state.generated_personas:
            st.success(f"✅ Step 2: Personas ({len(st.session_state.generated_personas)})")
        else:
            st.info("Step 2: Persona Generation")
        
        # Step 3 status
        if st.session_state.test_results:
            st.success(f"✅ Step 3: Tests ({len(st.session_state.test_results)})")
        else:
            st.info("Step 3: Intervention Testing")
        
        st.markdown("---")
        
        # Quick stats
        if st.session_state.processing_complete or st.session_state.generated_personas:
            st.markdown("### Quick Stats")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Personas", len(st.session_state.generated_personas))
            with col2:
                st.metric("Tests", len(st.session_state.test_results))
    
    # Main content area
    page = st.session_state.current_page
    if page == "Overview":
        render_overview()
    elif page == "Data Processing":
        render_step1_ui()
    elif page == "Persona Generation":
        render_persona_generation_ui()
    elif page == "Intervention Testing":
        render_intervention_testing_ui()

def render_overview():
    """Render the overview/landing page"""
    
    st.title("👥 CyPersona: an AI-based Data Driven Persona Framework")
    st.markdown(
    "Phishing attacks are getting smarter, and traditional simulations can harm trust and wellbeing. "
    "What if we could test security interventions safely using data-driven personas instead of real human beings?"
)  
    # Pipeline visualization
    st.markdown("---")
    st.markdown("### CyPersona Pipeline")
    
    steps_col1, steps_col2, steps_col3 = st.columns(3)
    
    with steps_col1:
        status = "✅" if st.session_state.processing_complete else "⏸️"
        st.markdown(f"""
        **{status} Step 1: Preprocessing of Existing Datasets**
        - LLM analyzes behavioral datasets
        - Extracts psychological patterns
        - Creates knowledge base
        """)
        
        if st.button("Go to Data Processing", key="overview_step1"):
            st.session_state.current_page = "Data Processing"
            st.rerun()
    
    with steps_col2:
        status = "✅" if st.session_state.generated_personas else "⏳" if st.session_state.processing_complete else "⏸️"
        st.markdown(f"""
        **{status} Step 2: Persona Generation**
        - Natural language persona creation
        - RAG-based behavioral modeling
        - Psychological profile generation
        """)
        
        if st.button("Go to Persona Generation", key="overview_step2"):
            st.session_state.current_page = "Persona Generation"
            st.rerun()
    
    with steps_col3:
        status = "✅" if st.session_state.test_results else "⏳" if st.session_state.generated_personas else "⏸️"
        st.markdown(f"""
        **{status} Step 3: Intervention Testing**
        - Test security interventions
        - Predict behavioral responses
        - Measure effectiveness
        """)
        
        if st.button("Go to Intervention Testing", key="overview_step3"):
            st.session_state.current_page = "Intervention Testing"
            st.rerun()
    
    
    # Dataset overview
    if st.session_state.processing_complete:
        st.markdown("---")
        st.markdown("### 📈 Current Data Status")
        
        # Mock dataset statistics
        data_col1, data_col2, data_col3, data_col4 = st.columns(4)
        
        with data_col1:
            st.metric("KnowBe4 Records", "5,000", help="Phishing simulation data")
        with data_col2:
            st.metric("Survey Responses", "365", help="Behavioral and psychological surveys")
        with data_col3:
            st.metric("Interview Transcripts", "8", help="Qualitative research data")
        with data_col4:
            st.metric("Knowledge Entries", "247", help="Extracted behavioral patterns")

def check_environment():
    """Check if required files and environment are set up"""
    
    required_files = [
        "modules/data_pipeline.py",
        "modules/persona_generation.py", 
        "modules/intervention_testing.py",
        "data/knowbe4.csv"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        st.error("Missing required files:")
        for file in missing_files:
            st.write(f"❌ {file}")
        st.stop()
    
    # Check for Together AI API token
    together_api_key = os.getenv("TOGETHER_API_KEY")
    if not together_api_key:
        st.info("ℹ️ Together AI API key not found. Configure in sidebar to enable LLM functionality.")

if __name__ == "__main__":
    # Check environment before starting
    check_environment()
    
    # Run main app
    main()