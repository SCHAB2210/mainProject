from stl import mesh

# Create a mesh from your 3D model (replace 'emoji.stl' with the path to your 3D model)
your_emoji_mesh = mesh.Mesh.from_file("test.STL")

# Export the mesh to an STL file
your_emoji_mesh.save('output.STL')
