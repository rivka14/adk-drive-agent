"""
Utility functions for Drive operations.
"""

import logging
import re
from typing import Optional
from google.auth import default
from googleapiclient.discovery import build

from ..config import DRIVE_SCOPES, EXPORT_MIME_TYPES

logger = logging.getLogger(__name__)

# Cache Drive service to avoid recreating it
_drive_service = None


def get_drive_service():
    """
    Get authenticated Drive API service using Application Default Credentials.

    Returns:
        Resource: The Drive API service object
    """
    global _drive_service

    if _drive_service is None:
        logger.info("Creating new Drive API service with ADC authentication")
        logger.debug(f"Using scopes: {DRIVE_SCOPES}")
        credentials, project = default(scopes=DRIVE_SCOPES)
        _drive_service = build('drive', 'v3', credentials=credentials)
        logger.info(f"Drive API service created successfully (project: {project})")
    else:
        logger.debug("Returning cached Drive API service")

    return _drive_service


def extract_file_id(url: str) -> Optional[str]:
    """
    Extract file ID from various Google Drive and Docs URL formats.

    Supports:
    - https://drive.google.com/file/d/{FILE_ID}/view
    - https://drive.google.com/open?id={FILE_ID}
    - https://docs.google.com/document/d/{FILE_ID}/edit
    - https://docs.google.com/spreadsheets/d/{FILE_ID}/edit
    - https://docs.google.com/presentation/d/{FILE_ID}/edit

    Args:
        url (str): The Google Drive or Docs URL

    Returns:
        Optional[str]: The file ID if found, None otherwise
    """
    logger.debug(f"Extracting file ID from URL: {url}")
    # Pattern matches both /d/FILE_ID and id=FILE_ID formats
    pattern = r'(?:id=|/d/)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)

    if match:
        file_id = match.group(1)
        logger.debug(f"Successfully extracted file ID: {file_id}")
        return file_id
    else:
        logger.warning(f"Could not extract file ID from URL: {url}")
        return None


def get_export_mime_type(google_mime_type: str) -> str:
    """
    Map Google Workspace MIME types to export formats.

    Args:
        google_mime_type (str): The Google Workspace MIME type

    Returns:
        str: The export MIME type to use
    """
    export_type = EXPORT_MIME_TYPES.get(google_mime_type, 'application/pdf')
    logger.debug(f"Mapped '{google_mime_type}' to export type '{export_type}'")
    return export_type


def is_google_workspace_file(mime_type: str) -> bool:
    """
    Check if a file is a Google Workspace file (Docs, Sheets, Slides, etc.).

    Args:
        mime_type (str): The file's MIME type

    Returns:
        bool: True if it's a Google Workspace file, False otherwise
    """
    is_workspace = mime_type.startswith('application/vnd.google-apps')
    logger.debug(f"MIME type '{mime_type}' is{'' if is_workspace else ' not'} a Google Workspace file")
    return is_workspace
