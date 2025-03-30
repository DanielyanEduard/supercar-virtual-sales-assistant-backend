from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from typing import Dict, List, Any
from dotenv import load_dotenv

from models import QueryRequest
from llm import LLMClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="SuperCar Virtual Sales Assistant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you'd want to specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck():
    """Health check endpoint."""
    return {
        "status": "OK",
        "message": "SuperCar Virtual Sales Assistant API is running! Replace this with your implementation."
    }

# Initialize LLM client
llm_client = LLMClient()

# Store conversation history by session ID
conversation_histories: Dict[str, List[Dict[str, Any]]] = {}

# Define system prompt with context about SuperCar dealerships
SYSTEM_PROMPT = """
You are Lex, a virtual sales assistant for SuperCar dealerships. Your role is to help customers with information about weather, our luxury vehicles, schedule test drives, and provide dealership information.

IMPORTANT: If a user initiates a tool-based request without specifying required parameters (such as dates, identification numbers, or location data), maintain empty string values for the corresponding argument fields rather than attempting to infer or populate these values. Wait for the user to provide the necessary information through follow-up interaction.
"""


@app.post("/query")
async def query(request: QueryRequest):
    """
    Process a user query and stream the response using Server-Sent Events.

    Args:
        request: The query request containing query text and session_id

    Returns:
        EventSourceResponse: A streaming response with AI assistant's message
    """
    # Initialize conversation history for new sessions
    session_id = request.session_id
    if session_id not in conversation_histories:
        conversation_histories[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # Limit conversation history to prevent context window issues
    conversation_history = conversation_histories[session_id][-10:]

    # Create an async generator for the streamed response
    async def event_generator():
        async for event in llm_client.process_query(
                request.query, conversation_history
        ):
            yield event
            print("event", event)

            # If this is a chunk event, save it for conversation history
            if event["event"] == "chunk":
                # After streaming completes, add the assistant's response to history
                if session_id in conversation_histories:
                    conversation_histories[session_id].append({
                        "role": "assistant",
                        "content": event["data"]
                    })

    # Add user query to conversation history
    conversation_histories[session_id].append({
        "role": "user",
        "content": request.query
    })

    # Return SSE response
    return EventSourceResponse(event_generator())


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)