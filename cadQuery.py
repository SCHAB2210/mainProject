import cadquery as cq
import math

# Create a 3D model of the sun emoji
def create_sun_emoji():
    # Create the main sun circle
    sun = cq.Workplane("XY").circle(10).extrude(2)

    # Create the sun rays as separate rectangles and rotate them
    rays = cq.Workplane("XY")
    for angle in range(0, 360, 30):
        ray = rays.rect(3, 20).extrude(0.2)  # Extrude each ray
        ray = ray.rotate((0, 0, 0), (0, 0, 1), math.radians(angle))  # Rotate the ray
        sun = sun.union(ray)  # Union each ray with the main sun

    return sun

# Export the sun emoji to an STL file
sun_emoji_model = create_sun_emoji()
sun_emoji_model = sun_emoji_model.translate((0, 0, 10))  # Adjust the z-coordinate for visibility

# Export the model to an STL file using CadQuery
cq.exporters.export(sun_emoji_model, "sun_emoji.stl")
