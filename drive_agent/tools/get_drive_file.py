"""
Tool for downloading and loading Google Drive files into the session.
"""

import io
import base64
import logging
from datetime import datetime
from typing import Optional

from google.adk.tools.tool_context import ToolContext
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from ..config import MAX_FILE_SIZE_MB
from .utils import (
    get_drive_service,
    extract_file_id,
    get_export_mime_type,
    is_google_workspace_file,
)

logger = logging.getLogger(__name__)


def get_drive_file(
    file_url: str,
    tool_context: ToolContext,
) -> dict:
    """
    Download content from a Google Drive file and store it in the session.

    Supports all file types:
    - Regular files (PDF, text, etc.) - downloaded directly
    - Google Docs/Sheets/Slides - exported to appropriate formats
    - Images - downloaded and encoded for multimodal processing

    The file content is stored in tool_context.state["loaded_files"] for
    use in answering questions.

    Args:
        file_url (str): Google Drive URL (e.g., https://drive.google.com/file/d/FILE_ID/view)
        tool_context (ToolContext): The tool context for state management

    Returns:
        dict: File information and status
    """
    logger.info(f"get_drive_file called with URL: {file_url}")

    try:
        file_id = extract_file_id(file_url)
        if not file_id:
            logger.error(f"Failed to extract file ID from URL: {file_url}")
            return {
                "status": "error",
                "message": (
                    f"Invalid Google Drive URL: {file_url}. "
                    "Expected format: https://drive.google.com/file/d/FILE_ID/view"
                ),
                "file_url": file_url,
            }

        logger.info(f"Extracted file ID: {file_id}")
        service = get_drive_service()
        logger.debug("Drive service obtained")

        logger.info(f"Fetching metadata for file ID: {file_id}")
        file_metadata = service.files().get(
            fileId=file_id,
            fields="id, name, mimeType, size, createdTime, modifiedTime, webViewLink"
        ).execute()

        mime_type = file_metadata.get('mimeType', '')
        file_name = file_metadata['name']
        file_size = int(file_metadata.get('size', 0)) if file_metadata.get('size') else 0

        logger.info(f"File metadata retrieved: name='{file_name}', mime_type='{mime_type}', size={file_size} bytes")

        if file_size > 0 and file_size > (MAX_FILE_SIZE_MB * 1024 * 1024):
            logger.warning(f"File '{file_name}' exceeds size limit: {file_size / (1024*1024):.1f} MB > {MAX_FILE_SIZE_MB} MB")
            return {
                "status": "error",
                "message": (
                    f"File '{file_name}' is too large ({file_size / (1024*1024):.1f} MB). "
                    f"Maximum supported size is {MAX_FILE_SIZE_MB} MB."
                ),
                "file_id": file_id,
                "file_name": file_name,
            }

        if is_google_workspace_file(mime_type):
            export_mime_type = get_export_mime_type(mime_type)
            logger.info(f"Google Workspace file detected. Exporting from '{mime_type}' to '{export_mime_type}'")
            request = service.files().export_media(
                fileId=file_id,
                mimeType=export_mime_type
            )
            processing_note = f"Exported from {mime_type} to {export_mime_type}"
        else:
            logger.info(f"Regular file detected. Downloading directly (mime_type: {mime_type})")
            request = service.files().get_media(fileId=file_id)
            processing_note = "Downloaded directly"

        logger.info(f"Starting download of '{file_name}'")
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logger.debug(f"Download progress: {int(status.progress() * 100)}%")

        file_content_bytes = file_buffer.getvalue()
        logger.info(f"Download complete: {len(file_content_bytes)} bytes received")

        content_text = None
        if mime_type.startswith('text/') or mime_type in ['application/pdf', 'text/csv']:
            try:
                content_text = file_content_bytes.decode('utf-8')
                logger.info(f"Successfully decoded text content ({len(content_text)} characters)")
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode content as UTF-8 for mime_type: {mime_type}")
                if mime_type == 'application/pdf':
                    content_text = "[PDF file - text extraction would require additional processing]"
                else:
                    content_text = None

        content_base64 = None
        if mime_type.startswith('image/'):
            content_base64 = base64.b64encode(file_content_bytes).decode('utf-8')
            logger.info(f"Encoded image as base64 ({len(content_base64)} characters)")

        if "loaded_files" not in tool_context.state:
            tool_context.state["loaded_files"] = {}
            logger.debug("Initialized loaded_files in tool context state")

        tool_context.state["loaded_files"][file_id] = {
            "name": file_name,
            "mime_type": mime_type,
            "size_bytes": len(file_content_bytes),
            "content_text": content_text,
            "content_bytes": file_content_bytes,
            "content_base64": content_base64,
            "loaded_at": datetime.now().isoformat(),
            "processing_note": processing_note,
            "metadata": file_metadata,
        }

        total_loaded = len(tool_context.state["loaded_files"])
        logger.info(f"File '{file_name}' stored in session state. Total loaded files: {total_loaded}")

        return {
            "status": "success",
            "message": (
                f"Successfully loaded file: {file_name} "
                f"({len(file_content_bytes) / 1024:.1f} KB). "
                f"{processing_note}."
            ),
            "file_id": file_id,
            "file_name": file_name,
            "mime_type": mime_type,
            "size_bytes": len(file_content_bytes),
            "has_text_content": content_text is not None,
            "has_image_content": content_base64 is not None,
            "loaded_files_count": len(tool_context.state["loaded_files"]),
        }

    except HttpError as e:
        if e.resp.status == 404:
            error_msg = (
                f"File not found. Check that the file ID '{file_id}' exists "
                "and is accessible with your Google Cloud credentials."
            )
            logger.error(f"404 error for file_id '{file_id}': {error_msg}")
        elif e.resp.status == 403:
            error_msg = (
                f"Permission denied. The authenticated user does not have access to this file. "
                f"Share the file with your Google Cloud user or service account."
            )
            logger.error(f"403 error for file_id '{file_id}': {error_msg}")
        else:
            error_msg = f"Google Drive API error: {str(e)}"
            logger.error(f"Drive API error ({e.resp.status}): {error_msg}")

        return {
            "status": "error",
            "message": error_msg,
            "file_url": file_url,
        }

    except Exception as e:
        error_msg = f"Error accessing Drive file: {str(e)}"
        logger.exception(f"Unexpected error in get_drive_file: {error_msg}")
        return {
            "status": "error",
            "message": error_msg,
            "file_url": file_url,
        }
