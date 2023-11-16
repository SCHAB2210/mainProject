import cadquery as cq
import jupyter

#parameters
ball_radius = 5.0;
small_circle
#cq.Workplane("XY")

#circle_1 = cq.Workplane("XY").circle(12).extrude(1.0)
#circle_2 = cq.Workplane("XY").circle(10).extrude(1.0)
#circle_3 = cq.Workplane("XY").circle(10).extrude(1.0)
#union = circle_1.union(circle_2)
#cloud = circle_3.union(circle_1)
# Create the ball
ball = cq.Workplane("XY").sphere(ball_radius)

# Create the smaller circle
small_circle = (
    cq.Workplane("XY")
    .circle(small_circle_radius)
    .extrude(connection_length)
)

cq.exporters.export(cloud, "cloud.STL")