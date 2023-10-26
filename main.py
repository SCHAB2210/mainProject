import requests

# User input for the location
location = 'Cape Town'

# Dictionary mapping weather icon codes to emojis
icon_to_emoji = {
    "01d": "☀️",  # Clear sky (day)
    "01n": "🌙",  # Clear sky (night)
    "02d": "🌤️",  # Few clouds (day)
    "02n": "🌤️",  # Few clouds (night)
    "03d": "🌥️",  # Scattered clouds (day)
    "03n": "🌥️",  # Scattered clouds (night)
    "04d": "☁️",  # Broken clouds (day)
    "04n": "☁️",  # Broken clouds (night)
    "09d": "🌧️",  # Shower rain (day)
    "09n": "🌧️",  # Shower rain (night)
    "10d": "🌦️",  # Rain (day)
    "10n": "🌦️",  # Rain (night)
    "11d": "⛈️",  # Thunderstorm (day)
    "11n": "⛈️",  # Thunderstorm (night)
    "13d": "🌨️",  # Snow (day)
    "13n": "🌨️",  # Snow (night)
    "50d": "🌫️",  # Mist (day)
    "50n": "🌫️",  # Mist (night)
}

# First script to obtain latitude and longitude
def get_coordinates(location):
    url = 'https://api.geoapify.com/v1/geocode/search'
    params = dict(
        text=location,
        apiKey='fa45cefd445b4a24b395696597c7f6a3'
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()
    if 'features' in data and data['features']:
        coordinates = data['features'][0]['geometry']['coordinates']
        return tuple(coordinates)
    else:
        return None

# Second script to get weather information with switched lat and lon
def get_weather(lon, lat):
    api_key = "bebddd365caebcd2e486c63d5a6a57f4"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Error retrieving weather information."

# Use the first script to get coordinates
coordinates = get_coordinates(location)

if coordinates:
    lon, lat = coordinates

    # Use the second script to get weather information
    weather_data = get_weather(lon, lat)

    if weather_data != "Error retrieving weather information":
        location_name = weather_data['name']
        temperature_celsius = weather_data['main']['temp']
        weather_icon = weather_data['weather'][0]['icon']

        # Convert the icon code to emoji
        if weather_icon in icon_to_emoji:
            weather_emoji = icon_to_emoji[weather_icon]
        else:
            weather_emoji = "❓"  # Use a question mark emoji for unknown icons

        print(f"Location: {location_name}")
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
        print(f"Temperature (Celsius): {temperature_celsius}°C")
        print(f"Weather Icon: {weather_emoji}")
    else:
        print("Error retrieving weather information.")
else:
    print("Location data not found in the response.")
