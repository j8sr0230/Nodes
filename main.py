import sys

from qtpy.QtWidgets import QApplication, QMainWindow
from nodeeditor.node_editor_window import NodeEditorWindow
import FreeCADGui


if __name__ == '__main__':
    if hasattr(FreeCADGui, "getMainWindow"):
        container = QMainWindow(parent=FreeCADGui.getMainWindow())
        ne_wnd = NodeEditorWindow()
        ne_wnd.nodeeditor.addNodes()
        container.setCentralWidget(ne_wnd)
        container.show()
    else:
        app = QApplication(sys.argv)
        wnd = NodeEditorWindow()
        wnd.nodeeditor.addNodes()
        sys.exit(app.exec_())
