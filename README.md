# SuperCar Virtual Sales Assistant - Backend Implementation

This is the implementation of the FastAPI backend for the SuperCar Virtual Sales Assistant. The backend uses Server-Sent Events (SSE) to stream AI responses and implements tool calling functionality with the Groq API.

## Features

- FastAPI application with a `/query` endpoint that accepts POST requests
- Server-Sent Events (SSE) streaming for real-time AI responses
- Tool calling functionality using Groq API with Llama 3.3 70B Versatile model
- Implementation of four required tools:
  - `get_weather`: Provides weather information for a city
  - `get_dealership_address`: Returns the address of a dealership
  - `check_appointment_availability`: Checks available appointment slots
  - `schedule_appointment`: Books an appointment for a test drive
- Session-based conversation history management
- CORS handling for frontend integration

## Getting Started

### Using Docker Compose (Recommended)

1. Create a free Groq API account at https://console.groq.com/ and get your API key

2. Navigate to the `backend` directory and create a `.env` file:
```bash
cd backend
cp .env.sample .env
```

3. Edit the `.env` file with your configuration:
```
# Groq API Key (get from https://console.groq.com/keys)
GROQ_API_KEY=your_groq_api_key_here

# Model Configuration
MODEL_NAME=llama3-70b-8192  # Llama 3.3 70B Versatile model

# Optional Configuration
DEBUG=false
```

4. Run the development environment using Docker Compose:
```bash
cd ../infrastructure
docker-compose up
```

This will:
- Start the backend FastAPI service on http://localhost:8000
- Start the frontend Next.js application on http://localhost:3000
- Set up volume mounts so your code changes are reflected immediately

### Running Without Docker

1. Install the required dependencies:
```bash
pip install fastapi uvicorn sse-starlette pydantic python-dotenv groq
```

2. Create a `.env` file with your configuration:
```
# Groq API Key (get from https://console.groq.com/keys)
GROQ_API_KEY=your_groq_api_key_here

# Model Configuration
MODEL_NAME=llama3-70b-8192  # Llama 3.3 70B Versatile model

# Optional Configuration
DEBUG=false
```

3. Run the FastAPI application:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /query

Process a user query and stream the response using Server-Sent Events.

**Request Body:**
```json
{
  "query": "What's the weather in New York?",
  "session_id": "user123"
}
```

**Response:**
Server-Sent Events with the following event types:
- `chunk`: Text chunks from the AI assistant
- `tool_use`: When the AI decides to use a tool
- `tool_output`: The result of a tool execution
- `end`: Signals the end of the response stream

### GET /health

Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Tool Implementation

The backend implements four tools as specified in the requirements:

1. **get_weather**
   - Simulates getting weather information for a city
   - Parameters: `city` (string)

2. **get_dealership_address**
   - Returns information about a SuperCar dealership
   - Parameters: `dealership_id` (string)

3. **check_appointment_availability**
   - Checks available appointment slots for a specific date at a dealership
   - Parameters: `dealership_id` (string), `date` (YYYY-MM-DD format)

4. **schedule_appointment**
   - Books a test drive appointment
   - Parameters: `user_id` (string), `dealership_id` (string), `date` (YYYY-MM-DD format), `time` (HH:MM format), `car_model` (string)

## Architecture

The backend follows a modular architecture:
- `main.py`: FastAPI application and endpoints
- `models.py`: Pydantic models for request/response
- `llm.py`: Groq API integration
- `tools/`: Tool implementations
- `utils/stream.py`: SSE streaming utilities

## Testing

You can test the API endpoint using tools like curl:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in New York?", "session_id": "test-session"}'
```

Or you can use the provided frontend at http://localhost:3000 to interact with the virtual sales assistant.
