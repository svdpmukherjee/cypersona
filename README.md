# CyPersona: AI-Powered Cybersecurity Persona Generation

Create realistic cybersecurity personas using behavioral data and LLMs for safe intervention testing without involving real employees.

## Overview

CyPersona helps organizations test cybersecurity interventions (training, policies, tools) against AI-powered personas instead of real employees. This eliminates deceptive testing, data safety concerns, and operational friction while maintaining behavioral authenticity.

### Key Features

- **Data-driven personas**: Built from real behavioral datasets
- **Natural language generation**: Describe personas in plain English
- **Intervention testing**: Predict responses to security training/policies
- **Privacy-first**: No real employee data required for testing

## Quick Start

### 1. Setup Environment

```bash
# Clone or download the project
git clone <repository-url>
cd cypersona

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
conda create -n cypersona_env python=3.8

```

### 2. Configure API Keys

You'll need API keys for:

- **Together AI**: For persona generation (Llama 3.1 8B)
- **OpenAI**: For embeddings and vector search

Add to `.env` file:

```bash
TOGETHER_API_KEY=your_together_ai_key_here
OPENAI_API_KEY=your_openai_key_here
```

Or set via the app sidebar after launching.

### 3. Launch Application

```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`

## Usage Guide

### Step 1: Data Processing

1. **Option A**: Upload your datasets (CSV files with behavioral data)
2. **Option B**: Load existing knowledge base (.pkl file)
3. Process data to create vector embeddings
4. Export knowledge base for reuse

### Step 2: Persona Generation

1. Describe desired persona in natural language
2. Select industry context and detail level
3. Generate 1-3 persona variants
4. Edit, clone, or export personas

### Step 3: Intervention Testing

1. Describe your security intervention
2. Select target personas
3. Run AI-powered predictions
4. Export results and analysis

## Sample Data Included

The repository includes sample datasets:

- `knowbe4.csv`: Phishing simulation data (5,000 records)
- `survey_*.csv`: Behavioral surveys (365+ responses)
- `transcript_*.csv`: Interview transcripts (8 qualitative interviews)

## File Structure

```
cypersona/
├── main.py                 # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .env                   # API keys (create this)
├── data/                  # Sample datasets
├── modules/                 # Core modules
│   ├── data_pipeline.py      # Step 1: Data processing
│   ├── persona_generation.py # Step 2: Persona creation
│   └── intervention_testing.py # Step 3: Testing
└── README.md
```

## API Requirements

### Together AI (Required)

- Used for persona generation with Llama 3.1 8B
- Get key: https://api.together.ai/
- Free tier available

### OpenAI (Required)

- Used for embeddings and vector search
- Get key: https://platform.openai.com/
- Pay-per-use pricing

## Example Workflows

### Healthcare Organization

1. Upload employee phishing simulation data
2. Create personas: "Busy ER nurse", "IT administrator", "Hospital executive"
3. Test intervention: "Mobile security awareness app with push notifications"
4. Predict adoption and effectiveness

### Financial Services

1. Load existing knowledge base
2. Generate personas for different risk profiles
3. Test policy: "Mandatory 2FA for all email access"
4. Assess compliance and resistance factors

## Version Info

- Current version: 1.0
- Streamlit: 1.28+
- Python: 3.8+
- Together AI: Llama 3.1 8B Instruct Turbo
- OpenAI: text-embedding-3-small
