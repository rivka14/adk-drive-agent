"""
Drive Agent

An ADK agent for accessing Google Drive files and answering questions
about their content.
"""

import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

try:
    if PROJECT_ID:
        print(f"Drive Agent initialized with project={PROJECT_ID}")
        print("Using Application Default Credentials for Drive API access")
        print("Drive Agent ready")
    else:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT not set. "
            "Drive API authentication may not work properly."
        )
except Exception as e:
    print(f"Error during Drive Agent initialization: {str(e)}")
    print("Please check your Google Cloud credentials.")

from . import agent
