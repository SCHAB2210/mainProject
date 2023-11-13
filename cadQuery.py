import cadquery as cq

# Parameters
ball_radius = 10.0  # Radius of the ball
small_circle_radius = 5.0  # Radius of the smaller circle
connection_length = 10.0  # Length of the connection

# Create the ball
ball = cq.Workplane("XY").sphere(ball_radius)

# Create the smaller circle
small_circle = (
    cq.Workplane("XY")
    .circle(small_circle_radius)
    .extrude(connection_length)
)

# Combine the ball and the smaller circle
raindrop = ball.union(small_circle)
