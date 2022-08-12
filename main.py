import sys

from qtpy.QtWidgets import QApplication, QMainWindow
import FreeCADGui

from fcn_window import FCNWindow


if __name__ == '__main__':
    if hasattr(FreeCADGui, "getMainWindow"):
        # Start app embedded in FreeCAD
        container = QMainWindow(parent=FreeCADGui.getMainWindow())
        ne_wnd = FCNWindow()
        container.setCentralWidget(ne_wnd)
        container.show()
    else:
        # Start app in standalone mode
        app = QApplication(sys.argv)
        wnd = FCNWindow()
        wnd.show()
        sys.exit(app.exec_())
