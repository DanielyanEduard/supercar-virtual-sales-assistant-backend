from .weather import get_weather
from .dealership import get_dealership_address
from .appointment import check_appointment_availability, schedule_appointment

# Define available tools and their schemas
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather information for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get weather information for"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dealership_address",
            "description": "Get the address of a SuperCar dealership",
            "parameters": {
                "type": "object",
                "properties": {
                    "dealership_id": {
                        "type": "string",
                        "description": "The ID of the dealership"
                    }
                },
                "required": ["dealership_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_appointment_availability",
            "description": "Check available appointment slots for a test drive",
            "parameters": {
                "type": "object",
                "properties": {
                    "dealership_id": {
                        "type": "string",
                        "description": "The ID of the dealership"
                    },
                    "date": {
                        "type": "string",
                        "description": "The date to check in YYYY-MM-DD format"
                    }
                },
                "required": ["dealership_id", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_appointment",
            "description": "Schedule a test drive appointment",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user scheduling the appointment"
                    },
                    "dealership_id": {
                        "type": "string",
                        "description": "The ID of the dealership"
                    },
                    "date": {
                        "type": "string",
                        "description": "The date of the appointment in YYYY-MM-DD format"
                    },
                    "time": {
                        "type": "string",
                        "description": "The time of the appointment in HH:MM format"
                    },
                    "car_model": {
                        "type": "string",
                        "description": "The car model for the test drive"
                    }
                },
                "required": ["user_id", "dealership_id", "date", "time", "car_model"]
            }
        }
    }
]

# Map tool names to their functions
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "get_dealership_address": get_dealership_address,
    "check_appointment_availability": check_appointment_availability,
    "schedule_appointment": schedule_appointment
}
ARGUMENTS_NAMES = {
    "dealership_id": "dealership ID",
    "date": "date (YYYY-MM-DD)",
    "user_id": "user ID",
    "time": "time (HH:MM)",
    "car_model": "car model",
}