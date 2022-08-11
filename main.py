import sys

from qtpy.QtWidgets import QApplication, QMainWindow
import FreeCADGui

from fc_nodes_window import FCNodesWindow


if __name__ == '__main__':
    if hasattr(FreeCADGui, "getMainWindow"):
        # Start app embedded in FreeCAD
        container = QMainWindow(parent=FreeCADGui.getMainWindow())
        ne_wnd = FCNodesWindow()
        ne_wnd.nodeeditor.addNodes()
        container.setCentralWidget(ne_wnd)
        container.show()
    else:
        # Start app in standalone mode
        app = QApplication(sys.argv)
        wnd = FCNodesWindow()
        wnd.nodeeditor.addNodes()
        sys.exit(app.exec_())
