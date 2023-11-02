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

# Function to generate matrix representation of an emoji
def emoji_to_matrix(emoji):
    emoji_matrix = []
    emoji_faces = []
    for row in emoji.split("\n"):
        emoji_matrix_row = [1 if char == "█" else 0 for char in row]
        emoji_matrix.append(emoji_matrix_row)
        emoji_faces.append([1 if sum(emoji_matrix_row) > 0 else 0])

    return emoji_matrix, emoji_faces

# Generate and display matrix representations for all emojis
for code, emoji in icon_to_emoji.items():
    print(f"Matrix representation for {emoji}:")
    matrix, faces = emoji_to_matrix(emoji)
    for row in matrix:
        for pixel in row:
            if pixel:
                print("█", end=" ")
            else:
                print(" ", end=" ")
        print()
    print(f"Vertices Matrix for {emoji}:")
    for row in matrix:
        for pixel in row:
            print(pixel, end=" ")
        print()
    print(f"Faces Matrix for {emoji}:")
    for row in faces:
        for face in row:
            print(face, end=" ")
        print()
    print()
