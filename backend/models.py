from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    session_id: str


class ToolParameter(BaseModel):
    name: str
    description: str
    type: str
    required: bool = True


class Tool(BaseModel):
    name: str
    description: str
    parameters: Dict[str, ToolParameter]


class Message(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class ToolCall(BaseModel):
    id: str
    type: str
    function: Dict[str, Any]


class ToolOutput(BaseModel):
    name: str
    output: Dict[str, Any]