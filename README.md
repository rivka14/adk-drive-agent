# Drive Agent

A Google ADK-based agent that provides intelligent Q&A capabilities for Google Drive files using Gemini 2.5 Pro.

## Overview

Drive Agent allows you to load Google Drive files and ask questions about their content through natural language conversation. It supports multiple file types including Google Workspace documents (Docs, Sheets, Slides), PDFs, images, and text files.

### Key Features

- **Multi-format Support**: Works with Google Docs, Google Sheets, Google Slides
- **Intelligent Q&A**: Ask questions about file content using natural language
- **Multi-file Analysis**: Load and compare multiple documents simultaneously
- **Specialized Workflows**: Includes domain-specific capabilities like disability percentage assessment for Bituach Leumi (National Insurance) documentation
- **Multimodal Processing**: Handles both text and image content
- **Session Persistence**: Files remain loaded throughout your session for repeated queries

## Prerequisites

- Python 3.11+
- Google Cloud Project with the following APIs enabled:
  - AI Platform (Vertex AI)
  - Google Drive API
- Google Cloud Application Default Credentials (ADC) configured

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rivka14/adk-drive-agent.git
   cd adk-drive-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   Create a `.env` file in the project root:
   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

4. **Authenticate with Google Cloud**
   ```bash
   gcloud auth login
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable drive.googleapis.com
   ```

## Usage

### Running the Agent

**Web Interface (Recommended)**
```bash
adk web
```

**Command Line Interface**
```bash
adk run
```

### Example Interactions

**Loading a File**
```
You: Load this file: https://drive.google.com/file/d/ABC123XYZ/view

Agent: I've successfully loaded 'Project Report.docx' (45 KB). What would you like to know about it?
```

**Asking Questions**
```
You: What are the main findings in this report?

Agent: Based on 'Project Report.docx', the main findings are...
```

**Working with Multiple Files**
```
You: Load these two files:
     - https://drive.google.com/file/d/FILE1/view
     - https://drive.google.com/file/d/FILE2/view

Agent: I've loaded both files:
       1. Budget_2024.xlsx (23 KB)
       2. Budget_2023.xlsx (21 KB)

       What would you like to compare?

You: How does the 2024 budget compare to 2023?

Agent: Comparing the two budget files...
```

### Specialized Use Case: Disability Assessment

For Bituach Leumi disability percentage assessment:

```
You: I'm uploading a National Insurance percentage definitions file
     and case medical documentation. Please assess the disability percentage.

Agent: [Loads both files]

       Based on comparison between the medical documentation and Bituach Leumi
       criteria, I estimate a disability percentage of 40-50%.

       Matching criteria:
       - [Specific criteria from definitions file]
       - [Medical findings that match]

       This is an estimated assessment. Final determinations are made by
       official medical committees.
```

## Project Structure

```
adk-drive-agent/
├── drive_agent/
│   ├── __init__.py        
│   ├── agent.py             
│   ├── config.py            
│   └── tools/
│       ├── __init__.py
│       ├── get_drive_file.py      
│       ├── list_loaded_files.py  
│       └── utils.py              
├── .env.example            
├── .gitignore
├── README.md
└── requirements.txt
```

## Configuration

### Environment Variables

- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID (required)
- `GOOGLE_CLOUD_LOCATION`: Region for Vertex AI (default: us-central1)

### Agent Settings (`drive_agent/config.py`)

- `MAX_FILE_SIZE_MB`: Maximum file size to load (default: 10 MB)
- `DRIVE_SCOPES`: Google Drive API scopes (default: readonly)
- `EXPORT_MIME_TYPES`: MIME type mappings for Google Workspace exports






