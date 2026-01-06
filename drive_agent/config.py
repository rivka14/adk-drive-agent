"""
Configuration settings for the Drive Agent.
"""

import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

MAX_FILE_SIZE_MB = 10

EXPORT_MIME_TYPES = {
    'application/vnd.google-apps.document': 'text/plain',
    'application/vnd.google-apps.spreadsheet': 'text/csv',
    'application/vnd.google-apps.presentation': 'text/plain',
}

SUPPORTED_TEXT_TYPES = [
    'text/plain',
    'text/csv',
    'text/html',
    'application/pdf',
]
