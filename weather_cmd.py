import argparse
import requests
from emoji_dict import icon_to_emoji

# Create an argument parser
parser = argparse.ArgumentParser(description="Get weather information for a location")

# Add an argument for the location
parser.add_argument("location", help="The location for which you want to get weather information")

# Parse the command-line arguments
args = parser.parse_args()

# Create a function to get weather information
def get_weather(location):
    api_key = "bebddd365caebcd2e486c63d5a6a57f4"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Use the function to get weather information
weather_data = get_weather(args.location)

if weather_data:
    location_name = weather_data['name']
    temperature_celsius = weather_data['main']['temp']
    weather_description = weather_data['weather'][0]['description']

    # Define a mapping of weather descriptions to emojis
    weather_to_emoji = {
        "clear sky": "☀️",
        "few clouds": "🌤️",
        "scattered clouds": "🌥️",
        "broken clouds": "☁️",
        "shower rain": "🌦️",
        "rain": "🌧️",
        "thunderstorm": "⛈️",
        "snow": "❄️",
        "mist": "🌫️",
    }

    # Default emoji for unknown weather conditions
    default_emoji = "❓"

    # Get the emoji for the current weather description
    weather_emoji = weather_to_emoji.get(weather_description, default_emoji)

    print(f"Location: {location_name}")
    print(f"Temperature (Celsius): {temperature_celsius}°C")
    print(f"Weather Description: {weather_description}")
    print(f"Weather Emoji: {weather_emoji}")

else:
    print("Error retrieving weather information")
