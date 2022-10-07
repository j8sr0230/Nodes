import FreeCADGui as Gui
import pivy.coin as coin


def make_markers():
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()

    marker = coin.SoMarkerSet()
    marker.markerIndex = coin.SoMarkerSet.CIRCLE_FILLED_9_9

    data = coin.SoCoordinate3()
    # data.point.setValue(0, 0, 0)
    data.point.setValues(0, 2, [[0, 0, 0], [1., 1., 0.]])

    color = coin.SoMaterial()
    color.diffuseColor = (1., 1., 1.)

    myCustomNode = coin.SoSeparator()
    myCustomNode.addChild(color)
    myCustomNode.addChild(data)
    myCustomNode.addChild(marker)
    sg.addChild(myCustomNode)

    return myCustomNode


def remove_node(node):
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.removeChild(node)


# node = make_markers()
# remove_node(node)
