# Drive Agent

A Google ADK-based agent that provides intelligent Q&A capabilities for Google Drive files using Gemini 2.5 Pro.

## Overview

Drive Agent allows you to load Google Drive files and ask questions about their content through natural language conversation. It supports multiple file types including Google Workspace documents (Docs, Sheets, Slides), PDFs, images, and text files.

### Key Features

- **Multi-format Support**: Works with Google Docs, Sheets, Slides, PDFs, images, and text files
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
  - Generative Language API (Gemini)
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
   gcloud auth application-default login
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

## Tools

### get_drive_file

Downloads and loads a Google Drive file into the session.

**Parameters:**
- `file_url` (str): Google Drive URL

**Returns:**
- File metadata and status
- Content stored in session state

**Supported URL Formats:**
- `https://drive.google.com/file/d/FILE_ID/view`
- `https://docs.google.com/document/d/FILE_ID/edit`
- `https://docs.google.com/spreadsheets/d/FILE_ID/edit`
- `https://docs.google.com/presentation/d/FILE_ID/edit`

### list_loaded_files

Lists all files currently loaded in the session.

**Parameters:** None

**Returns:**
- Array of loaded files with metadata
- File count and session information

## Authentication

The agent uses Google Cloud Application Default Credentials (ADC). Ensure you have:

1. **Authenticated locally:**
   ```bash
   gcloud auth application-default login
   ```

2. **Required IAM permissions:**
   - `aiplatform.*` (Vertex AI access)
   - `drive.files.read` (Google Drive read access)
   - `generativelanguage.*` (Gemini API access)

## Development

### Before Pushing Changes

```bash
# Unset GITHUB_TOKEN to avoid conflicts
unset GITHUB_TOKEN

# Authenticate with GitHub CLI
gh auth login
```

### Running Tests

```bash
# Run agent in CLI mode for testing
adk run

# Run web interface for interactive testing
adk web
```

## Limitations

- Maximum file size: 10 MB (configurable)
- PDF text extraction is limited (requires additional processing)
- Files are stored in session state (not persisted across sessions)
- Requires appropriate Google Drive sharing permissions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Add your license here]

## Support

For issues and questions:
- Open an issue on GitHub
- Check CLAUDE.md for development guidelines

---

Built with [Google ADK](https://github.com/google/adk) and Gemini 2.5 Pro
