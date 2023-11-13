import tkinter as tk
import requests
import os
from datetime import datetime
import cadquery as cq
from emoji_dict import icon_to_emoji
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import subprocess
import math


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

# Function to scale points
def scale_points(points, factor):
    return [(point[0] * factor, point[1] * factor) for point in points]

# Function to preview the STL file in a 3D window
# Function to preview the STL file using the default system viewer on Windows
def preview_stl(stl_filename):
    # Open the STL file using the default system viewer on Windows
    try:
        subprocess.run(['start', stl_filename], check=True, shell=True)
    except subprocess.CalledProcessError:
        print(f"Failed to open {stl_filename}. Please use an external viewer.")
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
        # Draw a sun with short lines radiating around the circle
        sun = cq.Workplane("XY")
        sun = sun.circle(emoji_size)

        # Create short lines radiating from the center, touching the circle
        for i in range(12):
            angle_rad = math.radians(30 * i)
            sun = sun.moveTo(emoji_size * math.cos(angle_rad), emoji_size * math.sin(angle_rad)).circle(0.5)

        emoji_3d = sun.extrude(1.0)

    elif icon_code in ['02d', '03d', '04d']:  # Cloudy
        # Draw a Cloud with filled circles
        cloud = (
            cq.Workplane("XY")
            #.circle(10).center(0, 0)
            .circle(12).moveTo(10, 10)
            .circle(10).moveTo(20, 0)
            .circle(10).moveTo(0, 20)
        )

        emoji_3d = cloud.extrude(1.0)

    elif icon_code in ['09d', '10d', '11d']:  # Rain

        # Parameters

        ball_diameter = 30  # Diameter of the ball

        triangle_side = ball_diameter  # Side length of the triangle

        line_length = 60  # Length of the line from AB to C

        # Create the raindrop shape

        raindrop = (

            cq.Workplane("XY")

            .circle(ball_diameter / 2)  # Circular bottom

            .moveTo(-triangle_side / 2, 0)

            .circle(triangle_side / 2)  # Triangular top

            .mirrorY()

            .extrude(0.1)  # Extrude a small amount to create a solid for lofting

            .faces(">Z")  # Select the top face

            .workplane()  # Create a new workplane on the top face

            .circle(ball_diameter / 2)  # Create a circle on the top face

            .extrude(line_length)  # Extrude to complete the raindrop shape

        )

        emoji_3d = raindrop.extrude(1.0)




    elif icon_code == '13d':  # Snowy
        # Draw a snowflake with filled circles
        snowflake = cq.Workplane("XY")
        # Create six lines radiating from the center with filled circles, touching the circle
        for i in range(6):
            angle_rad = math.radians(60 * i)
            snowflake = snowflake.moveTo(emoji_size * math.cos(angle_rad), emoji_size * math.sin(angle_rad)).circle(2)

        # Create six smaller circles at the end of each line with filled circles, touching the circle
        for i in range(6):
            angle_rad = math.radians(60 * i)
            snowflake = snowflake.moveTo((emoji_size + 5) * math.cos(angle_rad), (emoji_size + 5) * math.sin(angle_rad)).circle(1)

        emoji_3d = snowflake.extrude(1.0)

    else:
        # Default emoji for unknown weather condition with filled circles
        question_mark = (
            cq.Workplane("XY")
            .circle(5).extrude(1.0)  # Circle at the top
            .moveTo(0, 0).circle(2).extrude(1.0)  # Smaller circle at the bottom
            .moveTo(0, 0).circle(1.5).extrude(1.0)  # Even smaller circle at the bottom
            .moveTo(0, 0).rect(2, 12).extrude(1.0)  # Vertical line in the middle
        )
        emoji_3d = question_mark

    # Generate a unique filename using city name and date and time
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    stl_filename = f"{stl_directory}/{city_name}_{now}.STL"

    # Export the CadQuery 3D model as an STL file
    cq.exporters.export(emoji_3d, stl_filename)

    return stl_filename



# Start the main event loop
window.mainloop()
