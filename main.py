import os, sys, inspect
from qtpy.QtWidgets import QApplication

from nodeeditor.node_editor_window import NodeEditorWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = NodeEditorWindow()
    wnd.nodeeditor.addNodes()
    module_path = os.path.dirname( inspect.getfile(wnd.__class__) )

    sys.exit(app.exec_())