"""
Tool for listing currently loaded Drive files in the session.
"""

import logging
from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)


def list_loaded_files(
    tool_context: ToolContext,
) -> dict:
    """
    List all Google Drive files currently loaded in the session.

    Returns information about each file including name, size, type,
    and when it was loaded.

    Args:
        tool_context (ToolContext): The tool context for state management

    Returns:
        dict: List of loaded files with their metadata
    """
    logger.info("list_loaded_files called")

    loaded_files = tool_context.state.get("loaded_files", {})

    if not loaded_files:
        logger.info("No files currently loaded in session")
        return {
            "status": "success",
            "message": "No files currently loaded in this session.",
            "files": [],
            "count": 0,
        }

    files_list = []
    for file_id, file_data in loaded_files.items():
        file_name = file_data.get("name", "Unknown")
        logger.debug(f"Including file in list: {file_name} (ID: {file_id})")
        files_list.append({
            "file_id": file_id,
            "name": file_name,
            "mime_type": file_data.get("mime_type", "Unknown"),
            "size_kb": file_data.get("size_bytes", 0) / 1024,
            "loaded_at": file_data.get("loaded_at", "Unknown"),
            "has_text": file_data.get("content_text") is not None,
            "has_image": file_data.get("content_base64") is not None,
        })

    logger.info(f"Returning {len(files_list)} loaded file(s)")
    return {
        "status": "success",
        "message": f"Currently loaded {len(files_list)} file(s) in this session.",
        "files": files_list,
        "count": len(files_list),
    }
