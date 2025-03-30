import json
from typing import Dict


def format_chunk_event(text: str) -> Dict[str, str]:
    """Format a text chunk as an SSE event."""
    return {
        "event": "chunk",
        "data": text
    }


def format_tool_use_event(tool_name: str) -> Dict[str, str]:
    """Format a tool use event."""
    return {
        "event": "tool_use",
        "data": tool_name
    }


def format_tool_output_event(tool_name: str, output: str) -> Dict[str, str]:
    """Format a tool output event."""
    output_data = {
        "name": tool_name,
        "output": output
    }
    return {
        "event": "tool_output",
        "data": json.dumps(output_data)
    }


def format_end_event() -> Dict[str, str]:
    """Format an end event."""
    return {
        "event": "end",
        "data": ""
    }