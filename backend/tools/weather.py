def get_weather(city: str) -> str:
    """
    Simulates getting weather information for a city.

    Args:
        city: Name of the city

    Returns:
        Dict containing weather information
    """
    # Mock weather data - in a real implementation this would call a weather API
    weather_data = {
        "New York": {"temperature": "32°C", "condition": "sunny"},
        "Los Angeles": {"temperature": "27°C", "condition": "clear"},
        "Chicago": {"temperature": "24°C", "condition": "cloudy"},
        "Houston": {"temperature": "36°C", "condition": "sunny"},
        "Miami": {"temperature": "30°C", "condition": "rainy"}
    }

    # Default weather data for cities not in our mock database
    default_data = {"temperature": "25°C", "condition": "clear"}

    # Return the weather data for the requested city or default data
    weather = weather_data.get(city, default_data)
    return f"The weather in {city} is {weather['temperature']} and it's {weather['condition']}."

