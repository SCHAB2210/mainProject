import tkinter as tk
import requests
import os
from datetime import datetime
import cadquery as cq
from emoji_dict import icon_to_emoji
import pythreejs as p3

# First script to obtain latitude and longitude
def get_coordinates(location):
    url = 'https://api.geoapify.com/v1/geocode/search'
    params = dict(
        text=location,
        apiKey='fa45cefd445b4a24b395696597c7f6a3'  # Replace with your actual API key
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
    api_key = "bebddd365caebcd2e486c63d5a6a57f4"  # Replace with your actual API key
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Error retrieving weather information"

# Function to preview the STL file in a 3D window
def preview_stl(stl_filename):
    # Load the STL file
    geometry = p3.STLLoader().load(stl_filename)

    # Create a scene with the loaded geometry
    scene = p3.Scene(children=[p3.Mesh(geometry)])

    # Create a perspective camera
    camera = p3.PerspectiveCamera(position=[0, 0, 10], up=[0, 1, 0], aspect=1)

    # Create a renderer
    renderer = p3.Renderer(camera=camera, scene=scene, controls=[p3.OrbitControls(controlling=camera)])

    # Create a window to display the 3D view
    preview_window = p3.Viewer(renderers=[renderer])

    # Show the preview window
    preview_window.show()

# Create the main window
window = tk.Tk()
window.title("Weather & STL Generator")

# City input label and entry
city_label = tk.Label(window, text="Enter City:")
city_label.grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(window)
city_entry.grid(row=0, column=1, padx=10, pady=10)

# Weather and STL generation button
def get_weather_and_generate_stl():
    location = city_entry.get()

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
                weather_emoji = "❓"

            result_label.config(
                text=f"Location: {location_name}\nTemperature: {temperature_celsius}°C\nWeather Icon: {weather_emoji}")

            # Generate and export the 3D model
            stl_filename = create_stl_from_icon(weather_icon, location_name)
            result_label.config(text=result_label.cget("text") + f"\nSTL file saved as: {stl_filename}")

            # Preview the generated STL file
            preview_stl(stl_filename)
        else:
            result_label.config(text="Error retrieving weather information")
    else:
        result_label.config(text="Location data not found in the response")

generate_button = tk.Button(window, text="Generate Weather and STL", command=get_weather_and_generate_stl)
generate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Display result label
result_label = tk.Label(window, text="", wraplength=400)
result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Configure column and row weights for resizing
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(2, weight=1)

# Create a directory for STL files if it doesn't exist
stl_directory = "STL_Files"
os.makedirs(stl_directory, exist_ok=True)

# Update the create_stl_from_icon function
def create_stl_from_icon(icon_code, city_name):
    # Define the size of the emoji
    emoji_size = 10.0  # You can adjust this as needed

    # Create a CadQuery workplane
    workplane = cq.Workplane("XY")

    # Add geometry for the emoji based on the icon_code
    if icon_code == '01d':  # Sunny
        # Example: Draw a sun
        workplane.circle(emoji_size)

    elif icon_code == '02d':  # Partly cloudy
        # Example: Draw a sun
        workplane.circle(emoji_size)

        # Create a cloud workplane
        cloud_workplane = cq.Workplane("XY")
        cloud_workplane.circle(emoji_size / 2)

        # Translate and combine the cloud with the main workplane
        workplane = workplane.translate((0, 0, emoji_size / 2)).add(cloud_workplane)

    elif icon_code == '13d':  # Snowy
        # Example: Draw a snowflake
        workplane.circle(emoji_size / 3)
        snowflake_workplane = cq.Workplane("XY")
        snowflake_workplane.circle(emoji_size / 3)

        # Translate and combine the snowflake with the main workplane
        workplane = workplane.translate((0, 0, emoji_size / 3)).add(snowflake_workplane)

    elif icon_code == '03d':  # Cloudy
        # Example: Draw a cloud
        cloud_workplane = cq.Workplane("XY")
        cloud_workplane.circle(emoji_size / 2)

        # Combine the cloud with the main workplane
        workplane = workplane.add(cloud_workplane)

    else:
        # Default emoji for unknown weather condition
        workplane.circle(emoji_size / 2)

    # Extrude the emoji to create a 3D model
    emoji_3d = workplane.extrude(1.0)

    # Generate a unique filename using city name and date and time
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    stl_filename = f"{stl_directory}/{city_name}_{now}.STL"

    # Export the CadQuery 3D model as an STL file
    cq.exporters
