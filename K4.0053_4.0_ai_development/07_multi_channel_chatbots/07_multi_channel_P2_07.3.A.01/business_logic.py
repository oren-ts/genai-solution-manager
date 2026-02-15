import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    """
    Fetch weather information for a given city.
    
    Args:
        city (str): Name of the city
        
    Returns:
        str: Formatted weather message or error message
    """
    # Validation: Check if city is provided
    if not city or city.strip() == "":
        return "❌ Please provide a city name."
    
    # Prepare API request
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Get temperature in Celsius
    }
    
    try:
        # Call OpenWeatherMap API
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract weather information
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            city_name = data["name"]
            
            # Return formatted message
            return f"🌤 Weather in {city_name}: {temperature}°C, {description.capitalize()}"
        
        elif response.status_code == 404:
            return f"❌ City '{city}' not found. Please check the spelling."
        
        else:
            return f"❌ Weather service unavailable (Error {response.status_code})."
    
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: Unable to fetch weather data."
    
    except KeyError:
        return "❌ Unexpected response format from weather service."


def confirm_appointment(date, time):
    """
    Create a fictitious appointment confirmation.
    
    Args:
        date (str): Appointment date (e.g., "2024-03-15")
        time (str): Appointment time (e.g., "14:00")
        
    Returns:
        str: Confirmation message or error message
    """
    # Validation: Check if date and time are provided
    if not date or date.strip() == "":
        return "❌ Please provide a date."
    
    if not time or time.strip() == "":
        return "❌ Please provide a time."
    
    # Return confirmation message
    return f"✅ Appointment confirmed for {date} at {time}."


# Test functions (only runs when script is executed directly)
if __name__ == "__main__":
    print("Testing Business Logic Functions\n")
    
    # Test weather function
    print("--- Weather Tests ---")
    print(get_weather("Berlin"))
    print(get_weather("Stockholm"))
    print(get_weather(""))  # Empty city
    print(get_weather("XYZ123NonExistentCity"))  # Invalid city
    print()
    
    # Test appointment function
    print("--- Appointment Tests ---")
    print(confirm_appointment("2024-03-15", "14:00"))
    print(confirm_appointment("", "14:00"))  # Missing date
    print(confirm_appointment("2024-03-15", ""))  # Missing time