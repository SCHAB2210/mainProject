def create_stl_from_icon(icon_code, city_name):
    # Create a CadQuery workplane
    workplane = cq.Workplane("XY")

    # Define the size of the emoji
    emoji_size = 10.0  # You can adjust this as needed

    # Add geometry for the emoji based on the icon_code
    if icon_code == '01d':  # Replace with the appropriate icon code
        # Example: Draw a sun
        workplane.circle(emoji_size)

    elif icon_code == '02d':
        # Example: Draw a sun behind clouds
        workplane.circle(emoji_size)
        workplane = workplane.center(0, 0, 0).rect(2 * emoji_size, emoji_size)

    else:
        # Default emoji (question mark)
        workplane.text("?", 10.0, 0, 0)

    # Extrude the emoji to create a 3D model
    emoji_3d = workplane.extrude(1.0)

    # Generate a unique filename using city name and date and time
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    stl_filename = f"{stl_directory}/{city_name}_{now}.STL"

    # Export the CadQuery 3D model as an STL file
    cq.exporters.export(emoji_3d, stl_filename)

    return stl_filename
