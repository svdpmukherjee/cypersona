"""
STEP 1: LLM-Powered Data Processing Pipeline for CyPersona

"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import faiss
import pickle

load_dotenv()

class OpenAIVectorDB:
    """OpenAI-powered vector database for cybersecurity research"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.documents = []
        self.embeddings = []
        self.metadata = []
        self.index = None
        
    def add_document(self, text, metadata):
        """Add document to knowledge base"""
        try:
            # Get embedding from OpenAI
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding
            
            self.documents.append(text)
            self.embeddings.append(embedding)
            self.metadata.append(metadata)
            
        except Exception as e:
            st.error(f"Error creating embedding: {e}")
            
    def build_index(self):
        """Build FAISS index for fast similarity search"""
        if self.embeddings:
            embeddings_array = np.array(self.embeddings).astype('float32')
            dimension = embeddings_array.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
            faiss.normalize_L2(embeddings_array)  # Normalize for cosine similarity
            self.index.add(embeddings_array)
            
    def query(self, query_text, top_k=5):
        """Query knowledge base and return relevant documents"""
        # Check if we have any data
        if not self.documents or len(self.embeddings) == 0:
            st.warning("Knowledge base is empty. No documents to search.")
            return []
            
        # Build index if it doesn't exist
        if self.index is None:
            st.info("Building search index...")
            self.build_index()
            
        if self.index is None:
            st.error("Failed to build search index")
            return []
            
        try:
            # Get query embedding
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=query_text
            )
            query_embedding = np.array([response.data[0].embedding]).astype('float32')
            faiss.normalize_L2(query_embedding)
            
            # Search
            scores, indices = self.index.search(query_embedding, top_k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents) and score > 0.1:  # Lower similarity threshold
                    results.append({
                        'text': self.documents[idx],
                        'metadata': self.metadata[idx],
                        'similarity': float(score)
                    })
            return results
            
        except Exception as e:
            st.error(f"Error querying: {e}")
            return []
        
    def save(self, filepath):
        """Save knowledge base to file"""
        data = {
            'documents': self.documents,
            'metadata': self.metadata,
            'embeddings': self.embeddings
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
            
        # Save FAISS index separately if it exists
        if self.index:
            faiss.write_index(self.index, filepath.replace('.pkl', '.faiss'))
            
    def load(self, filepath):
        """Load knowledge base from file"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.documents = data.get('documents', [])
                self.metadata = data.get('metadata', [])
                self.embeddings = data.get('embeddings', [])
            
            # Try to load FAISS index
            faiss_path = filepath.replace('.pkl', '.faiss')
            if os.path.exists(faiss_path):
                try:
                    self.index = faiss.read_index(faiss_path)
                except Exception as e:
                    st.warning(f"Could not load FAISS index: {e}. Will rebuild when needed.")
                    self.index = None
            else:
                # No FAISS file found, will rebuild when needed
                self.index = None
                
            return True
        except Exception as e:
            st.error(f"Error loading knowledge base: {e}")
            return False

class LLMDataProcessor:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.vector_db = OpenAIVectorDB()
        
    def safe_read_csv(self, file_obj):
        """Safely read CSV from uploaded file object"""
        try:
            file_obj.seek(0)
            df = pd.read_csv(file_obj)
            if df.empty:
                raise ValueError("Empty CSV file")
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
            return None
            
    def extract_knowledge_from_dataframe(self, df, dataset_name):
        """Extract knowledge from dataframe and add to vector database"""
        knowledge_texts = []
        
        # Extract column insights
        for col in df.columns:
            if df[col].dtype in ['object', 'bool']:
                # Categorical analysis
                value_counts = df[col].value_counts().head(5)
                text = f"In {dataset_name}, column {col} shows: {dict(value_counts)}"
                knowledge_texts.append(text)
                self.vector_db.add_document(text, {
                    'type': 'categorical_analysis',
                    'dataset': dataset_name,
                    'column': col
                })
                
            elif df[col].dtype in ['int64', 'float64']:
                # Numerical analysis
                stats = df[col].describe()
                text = f"In {dataset_name}, {col} has mean {stats['mean']:.2f}, std {stats['std']:.2f}, range {stats['min']:.2f}-{stats['max']:.2f}"
                knowledge_texts.append(text)
                self.vector_db.add_document(text, {
                    'type': 'numerical_analysis', 
                    'dataset': dataset_name,
                    'column': col
                })
        
        # Extract behavioral patterns using Together AI
        sample_data = df.head(10).to_string()
        pattern_text = self.analyze_behavioral_patterns(sample_data, dataset_name)
        if pattern_text and "Error:" not in pattern_text:
            self.vector_db.add_document(pattern_text, {
                'type': 'behavioral_patterns',
                'dataset': dataset_name
            })
            knowledge_texts.append(pattern_text)
        
        return knowledge_texts
    
    def analyze_behavioral_patterns(self, sample_data, dataset_name):
        """Analyze behavioral patterns using Together AI Llama 3.1 8B"""
        try:
            import together
            together_client = together.Together(api_key=os.getenv("TOGETHER_API_KEY"))
            
            response = together_client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[{
                    "role": "user",
                    "content": f"""
                    Analyze this cybersecurity research data from {dataset_name}:
                    
                    {sample_data}
                    
                    Extract key behavioral insights about:
                    - Phishing susceptibility patterns
                    - Security awareness behaviors  
                    - Risk factors and protective factors
                    - Training effectiveness indicators
                    
                    Provide 2-3 concise insights in plain text format.
                    """
                }],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

def load_uploaded_knowledge_base(uploaded_file):
    """Load knowledge base from uploaded file - FIXED VERSION"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_kb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Load knowledge base
        vector_db = OpenAIVectorDB()
        success = vector_db.load(temp_path)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Clean up potential FAISS temp file
        temp_faiss = temp_path.replace('.pkl', '.faiss')
        if os.path.exists(temp_faiss):
            os.remove(temp_faiss)
        
        if success and vector_db.documents:
            return vector_db
        else:
            st.error("Knowledge base file appears to be empty or corrupted")
            return None
            
    except Exception as e:
        st.error(f"Error loading knowledge base: {e}")
        return None

def render_step1_ui():
    """Data Upload and Processing UI with upload/export functionality"""
    
    st.title("STEP 1: AI-Powered Data Preprocessing")
    st.markdown("Create or load a vector knowledge base for persona generation")
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("🔑 OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        st.stop()
    
    # Two main options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Load Existing Knowledge Base")
        
        uploaded_kb = st.file_uploader(
            "Upload Knowledge Base (.pkl file)",
            type=['pkl'],
            help="Upload a previously exported FAISS knowledge base"
        )
        
        if uploaded_kb:
            if st.button("Load Knowledge Base", type="primary", use_container_width=True):
                with st.spinner("Loading knowledge base..."):
                    vector_db = load_uploaded_knowledge_base(uploaded_kb)
                    if vector_db:
                        st.session_state.vector_knowledge_base = vector_db
                        st.session_state.processing_complete = True
                        
                        # Show loaded stats
                        col1a, col2a, col3a = st.columns(3)
                        with col1a:
                            st.metric("Documents", len(vector_db.documents))
                        with col2a:
                            st.metric("Embeddings", len(vector_db.embeddings))
                        with col3a:
                            behavioral_docs = sum(1 for meta in vector_db.metadata if meta.get('type') == 'behavioral_patterns')
                            st.metric("Behavioral Patterns", behavioral_docs)
                        
                        st.success("✅ Knowledge base loaded successfully!")
                        
                        # Test the loaded knowledge base immediately
                        test_query = "phishing click rates"
                        test_results = vector_db.query(test_query)
                        if test_results:
                            st.info(f"✅ Knowledge base is functional - found {len(test_results)} results for test query")
                        else:
                            st.warning("⚠️ Knowledge base loaded but no results for test query")
                        
                        st.rerun()
    
    with col2:
        st.subheader("📁 Build New Knowledge Base")
        st.markdown("Upload datasets to create a new vector knowledge base")
        
        if st.button("📤 Upload Data & Build", use_container_width=True):
            st.session_state.show_data_upload = True
            st.rerun()
    
    # Data upload interface (only show when requested)
    if st.session_state.get('show_data_upload', False):
        st.markdown("---")
        st.subheader("📁 Data Ingestion")
        # Cloud storage simulation
        st.info("🌐 All uploaded data will be securely stored in clouds (e.g. **Azure Data Lake Gen2**)")
        
        processor = LLMDataProcessor()
        
        # Initialize session state for uploads
        if 'uploaded_datasets' not in st.session_state:
            st.session_state.uploaded_datasets = {
                'knowbe4': None,
                'surveys': [],
                'transcripts': []
            }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Phishing simulation results**")
            knowbe4_file = st.file_uploader("Upload KnowBe4 CSV", type=['csv'], key="knowbe4_upload")
            if knowbe4_file:
                st.session_state.uploaded_datasets['knowbe4'] = knowbe4_file
                df = processor.safe_read_csv(knowbe4_file)
                if df is not None:
                    st.success(f"✅ {len(df)} records")
        
        with col2:
            st.markdown("**Behavioral surveys**")
            survey_files = st.file_uploader("Upload Survey CSVs", type=['csv'], accept_multiple_files=True, key="survey_upload")
            if survey_files:
                st.session_state.uploaded_datasets['surveys'] = survey_files
                total_records = sum(len(processor.safe_read_csv(f)) for f in survey_files if processor.safe_read_csv(f) is not None)
                st.success(f"✅ {len(survey_files)} files, {total_records} records")
        
        with col3:
            st.markdown("**Interview transcripts**")
            transcript_files = st.file_uploader("Upload Transcript CSVs", type=['csv'], accept_multiple_files=True, key="transcript_upload")
            if transcript_files:
                st.session_state.uploaded_datasets['transcripts'] = transcript_files
                total_transcripts = sum(len(processor.safe_read_csv(f)) for f in transcript_files if processor.safe_read_csv(f) is not None)
                st.success(f"✅ {len(transcript_files)} files, {total_transcripts} transcripts")
        
        # Processing
        has_data = any([
            st.session_state.uploaded_datasets['knowbe4'],
            st.session_state.uploaded_datasets['surveys'],
            st.session_state.uploaded_datasets['transcripts']
        ])
        
        if has_data:
            if st.button("Start Processing", type="primary", use_container_width=True):
                with st.spinner("Processing datasets..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    datasets_processed = 0
                    
                    # Process each dataset type
                    if st.session_state.uploaded_datasets['knowbe4']:
                        status_text.text("Processing KnowBe4 data...")
                        progress_bar.progress(0.3)
                        df = processor.safe_read_csv(st.session_state.uploaded_datasets['knowbe4'])
                        if df is not None:
                            processor.extract_knowledge_from_dataframe(df, "KnowBe4 Data")
                            datasets_processed += 1
                    
                    for i, file in enumerate(st.session_state.uploaded_datasets['surveys']):
                        status_text.text(f"Processing survey {i+1}...")
                        progress_bar.progress(0.3 + (0.3 * (i+1) / len(st.session_state.uploaded_datasets['surveys'])))
                        df = processor.safe_read_csv(file)
                        if df is not None:
                            processor.extract_knowledge_from_dataframe(df, f"Survey_{i+1}")
                            datasets_processed += 1
                    
                    for i, file in enumerate(st.session_state.uploaded_datasets['transcripts']):
                        status_text.text(f"Processing transcript {i+1}...")
                        progress_bar.progress(0.6 + (0.2 * (i+1) / len(st.session_state.uploaded_datasets['transcripts'])))
                        df = processor.safe_read_csv(file)
                        if df is not None and 'transcript_text' in df.columns:
                            for _, row in df.iterrows():
                                if pd.notna(row['transcript_text']) and len(str(row['transcript_text'])) > 50:
                                    processor.vector_db.add_document(
                                        str(row['transcript_text']),
                                        {'type': 'qualitative_transcript', 'dataset': f'transcript_{i+1}'}
                                    )
                            datasets_processed += 1
                    
                    status_text.text("Building vector index...")
                    progress_bar.progress(0.9)
                    processor.vector_db.build_index()
                    
                    status_text.text("Finalizing...")
                    progress_bar.progress(1.0)
                    
                    st.session_state.vector_knowledge_base = processor.vector_db
                    st.session_state.processing_complete = True
                    st.session_state.kb_created = True
                    
                    # Success metrics and export
                    st.success("✅ Knowledge base created successfully!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Datasets", datasets_processed)
                    with col2:
                        st.metric("Documents", len(processor.vector_db.documents))
                    with col3:
                        st.metric("Embeddings", len(processor.vector_db.embeddings))
                    
                    # Export functionality
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    kb_filename = f"cypersona_kb_{timestamp}.pkl"
                    
                    # Save to temporary location for download
                    temp_path = f"temp_{kb_filename}"
                    processor.vector_db.save(temp_path)
                    
                    with open(temp_path, 'rb') as f:
                        kb_data = f.read()
                    
                    st.download_button(
                        "📥 Download Knowledge Base",
                        kb_data,
                        kb_filename,
                        "application/octet-stream",
                        help="Download this file to reuse the knowledge base later",
                        use_container_width=True
                    )
                    
                    # Clean up temp file
                    os.remove(temp_path)
                    if os.path.exists(temp_path.replace('.pkl', '.faiss')):
                        os.remove(temp_path.replace('.pkl', '.faiss'))
                    
                    # st.balloons()
        
        elif not has_data:
            st.info("Upload datasets above to enable processing")
    
    # Knowledge base testing and navigation
    if st.session_state.get('processing_complete', False):
        st.markdown("---")
        st.subheader("Test Knowledge Base")
        
        # Show knowledge base stats
        vector_db = st.session_state.vector_knowledge_base
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Documents", len(vector_db.documents))
        with col2:
            st.metric("Total Embeddings", len(vector_db.embeddings))
        with col3:
            index_status = "✅ Ready" if vector_db.index else "⚠️ Not Built"
            st.metric("Search Index", index_status)
        
        # Query interface
        query = st.text_input("Query:", placeholder="e.g., phishing click rates by role")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_button = st.button("Search", type="secondary")
        with col2:
            if st.button("🔄 Rebuild Index"):
                with st.spinner("Rebuilding search index..."):
                    vector_db.build_index()
                    st.success("Index rebuilt!")
                    st.rerun()
        
        if search_button and query:
            with st.spinner("Searching..."):
                results = vector_db.query(query)
                
                if results:
                    st.success(f"Found {len(results)} results:")
                    for i, result in enumerate(results[:5]):
                        with st.expander(f"Result {i+1} (similarity: {result['similarity']:.3f})", expanded=i==0):
                            st.write(result['text'])
                            st.caption(f"Type: {result['metadata'].get('type', 'Unknown')} | Dataset: {result['metadata'].get('dataset', 'Unknown')}")
                else:
                    st.warning("No results found. Try:")
                    st.write("• Different keywords")
                    st.write("• Broader search terms")
                    st.write("• Rebuilding the search index")
        
        # Next step
        st.markdown("---")
        if st.button("Go to Persona Generation", type="primary", use_container_width=True):
            st.session_state.current_page = "Persona Generation"
            st.rerun()

if __name__ == "__main__":
    render_step1_ui()