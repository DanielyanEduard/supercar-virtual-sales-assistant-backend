from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


def check_appointment_availability(dealership_id: str, date: str) -> Dict[str, Any]:
    """
    Checks available appointment slots for a test drive at a specific dealership and date.

    Args:
        dealership_id: The ID of the dealership
        date: The date to check in YYYY-MM-DD format

    Returns:
        Dict containing available time slots
    """
    # Validate date format
    # try:
    #     datetime.strptime(date, "%Y-%m-%d")
    # except ValueError:
    #     return {
    #         "error": "Invalid date format. Please use YYYY-MM-DD format."
    #     }

    # Generate some random available slots (in a real implementation, this would query a database)
    all_possible_slots = [
        "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
        "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
        "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"
    ]

    # Use dealership_id as a seed for reproducible randomness
    seed = sum(ord(c) for c in f"{dealership_id}{date}")
    random.seed(seed)

    # Randomly select some slots as "available"
    num_available = random.randint(5, 10)
    available_slots = random.sample(all_possible_slots, num_available)
    available_slots.sort()

    return available_slots


def schedule_appointment(user_id: str, dealership_id: str, date: str, time: str, car_model: str) -> Dict[str, Any]:
    """
    Schedules a test drive appointment.

    Args:
        user_id: The ID of the user scheduling the appointment
        dealership_id: The ID of the dealership
        date: The date of the appointment in YYYY-MM-DD format
        time: The time of the appointment in HH:MM format
        car_model: The car model for the test drive

    Returns:
        Dict containing confirmation details
    """
    # Validate date and time formats
    try:
        appointment_date = datetime.strptime(date, "%Y-%m-%d")
        appointment_time = datetime.strptime(time, "%H:%M")
    except ValueError:
        return {
            "error": "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."
        }

    # Generate a confirmation number
    confirmation_code = f"SC-{dealership_id}-{user_id[:4]}-{int(datetime.now().timestamp()) % 10000}"

    # Get dealership name (would be from database in real implementation)
    dealership_names = {
        "NYC001": "SuperCar Manhattan",
        "LA002": "SuperCar Beverly Hills",
        "CHI003": "SuperCar Chicago",
        "HOU004": "SuperCar Houston",
        "MIA005": "SuperCar Miami"
    }
    dealership_name = dealership_names.get(dealership_id, "SuperCar Dealership")

    # Format date and time for display
    formatted_date = appointment_date.strftime("%A, %B %d, %Y")
    formatted_time = appointment_time.strftime("%I:%M %p")

    return {
        "confirmation_code": confirmation_code,
        "user_id": user_id,
        "dealership": {
            "id": dealership_id,
            "name": dealership_name
        },
        "appointment": {
            "date": formatted_date,
            "time": formatted_time,
            "car_model": car_model
        },
        "instructions": "Please arrive 15 minutes before your appointment and bring your driver's license.",
        "cancellation_policy": "You can reschedule or cancel your appointment up to 24 hours before the scheduled time."
    }