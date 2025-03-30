from typing import Dict, Any


def get_dealership_address(dealership_id: str) -> str:
    """
    Returns the address of a dealership based on its ID.

    Args:
        dealership_id: The ID of the dealership

    Returns:
        Dict containing the dealership information
    """
    # Mock dealership data - in a real implementation this would query a database
    dealerships = {
        "NYC001": {
            "name": "SuperCar Manhattan",
            "address": "123 Luxury Lane, Manhattan, NY 10001",
            "phone": "+1 (212) 555-7890",
            "hours": "Mon-Fri: 9am-7pm, Sat: 10am-5pm, Sun: Closed"
        },
        "LA002": {
            "name": "SuperCar Beverly Hills",
            "address": "456 Prestige Drive, Beverly Hills, CA 90210",
            "phone": "+1 (310) 555-1234",
            "hours": "Mon-Fri: 10am-8pm, Sat-Sun: 11am-6pm"
        },
        "CHI003": {
            "name": "SuperCar Chicago",
            "address": "789 Elite Street, Chicago, IL 60611",
            "phone": "+1 (312) 555-4567",
            "hours": "Mon-Sat: 9am-6pm, Sun: 11am-4pm"
        },
        "HOU004": {
            "name": "SuperCar Houston",
            "address": "321 Premium Parkway, Houston, TX 77056",
            "phone": "+1 (713) 555-8901",
            "hours": "Mon-Fri: 9am-7pm, Sat: 10am-6pm, Sun: Closed"
        },
        "MIA005": {
            "name": "SuperCar Miami",
            "address": "555 Luxury Avenue, Miami, FL 33139",
            "phone": "+1 (305) 555-2345",
            "hours": "Mon-Sun: 10am-8pm"
        }
    }

    # Return the dealership info or a message if not found
    if dealership_id in dealerships:
        dealership_info = dealerships[dealership_id]
        print(f"Name: {dealership_info['name']}. Address: {dealership_info['address']}. Phone: {dealership_info['phone']}. Hours: {dealership_info['hours']}.")
        return f"Name: {dealership_info['name']}. Address: {dealership_info['address']}. Phone: {dealership_info['phone']}. Hours: {dealership_info['hours']}."
    else:
        print("Name: Unknown Dealership. Message: No dealership found with ID {dealership_id}. Suggestion: Please visit our website to find the nearest dealership.")
        return "Name: Unknown Dealership. Message: No dealership found with ID {dealership_id}. Suggestion: Please visit our website to find the nearest dealership."