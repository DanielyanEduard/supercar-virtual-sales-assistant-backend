import os
import json
import groq
from typing import Dict, List, Any, AsyncGenerator
from tools import TOOLS, TOOL_FUNCTIONS, ARGUMENTS_NAMES
from utils import *


class LLMClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = groq.AsyncGroq(api_key=api_key)
        self.model = os.getenv("MODEL_NAME")

    async def process_query(
            self,
            query: str,
            conversation_history: List[Dict[str, Any]]
    ) -> AsyncGenerator[Dict[str, str], None]:
        """
        Process a query using the Groq API with tool calling capabilities.

        Args:
            query: The user's query
            conversation_history: Previous conversation messages

        Yields:
            SSE events for streaming to the client
        """
        # Add the user's message to the conversation
        messages = conversation_history + [{"role": "user", "content": query}]
        print("messages", messages)
        try:
            # Stream the response from Groq API
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                stream=True,
                max_tokens=4096,
                temperature=0.7
            )

            collected_content = ""
            current_tool_calls = []

            async for chunk in stream:
                delta = chunk.choices[0].delta
                # If there's text content, emit a chunk event
                if delta.content:
                    collected_content += delta.content
                    yield format_chunk_event(delta.content)

                # Handle tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        # Initialize a new tool call
                        if tool_call.index >= len(current_tool_calls):
                            current_tool_calls.append({
                                "id": tool_call.id or "",
                                "type": tool_call.type or "",
                                "function": {
                                    "name": tool_call.function.name or "",
                                    "arguments": tool_call.function.arguments or ""
                                }
                            })
                        else:
                            # Append to existing tool call's arguments
                            if tool_call.function and tool_call.function.arguments:
                                current_tool_calls[tool_call.index]["function"][
                                    "arguments"] += tool_call.function.arguments

            # Process completed tool calls
            if current_tool_calls:
                for tool_call in current_tool_calls:
                    function_name = tool_call["function"]["name"]
                    try:
                        arguments = json.loads(tool_call["function"]["arguments"])
                    except json.JSONDecodeError:
                        # If arguments can't be parsed, continue
                        continue

                    empty_values = [ARGUMENTS_NAMES.get(key, key) for key, value in arguments.items() if
                                    value == '' or value == 'required']

                    if not empty_values:
                        # Let the frontend know we're using a tool
                        yield format_tool_use_event(function_name)

                        # Execute the tool function
                        tool_result = TOOL_FUNCTIONS[function_name](**arguments)

                        # Yield the tool output event
                        yield format_tool_output_event(function_name, tool_result)

                        # Add the tool result to conversation history for context
                        messages.append({
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [tool_call]
                        })
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": function_name,
                            "content": json.dumps(tool_result)
                        })

                # Get a final response that incorporates the tool results
                final_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=False,
                    max_tokens=1024,
                    temperature=0.7
                )

                # Send the final response content
                final_content = final_response.choices[0].message.content
                if final_content:
                    yield format_chunk_event(final_content)

            # Signal the end of the response
            yield format_end_event()

        except Exception as e:
            # In case of an error, send an error message and end the stream
            error_message = f"An error occurred: {str(e)}"
            yield format_chunk_event(error_message)
            yield format_end_event()