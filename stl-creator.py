import vtk
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor


def main():
    reader = vtk.vtkSTLReader()
    reader.SetFileName('test.STL')

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    rendererWindow = vtk.vtkRenderWindow()
    rendererWindow.AddRenderer(renderer)
    rendererWindowInteractor: vtkRenderWindowInteractor = vtk.vtkRenderWindowInteractor()
    rendererWindowInteractor.SetRenderWindow(rendererWindow)

    renderer.AddActor(actor)
    rendererWindowInteractor.SetBackgroundColor(1,1,1)

    rendererWindow.Render()
    rendererWindowInteractor.Start()

    if __name__ == '__main__':
        main()

