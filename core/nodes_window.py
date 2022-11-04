import json
from fnmatch import fnmatch

from qtpy.QtGui import QIcon, QKeySequence
from qtpy.QtWidgets import QApplication, QMdiArea, QWidget, QDockWidget, QAction, QMessageBox, QFileDialog, QMenu
from qtpy.QtCore import Qt, QSignalMapper

from nodeeditor.node_editor_window import NodeEditorWindow
from nodeeditor.node_edge import Edge
from nodeeditor.utils import dumpException, pp
from nodeeditor.node_edge_validators import (  # Enabling edge validators
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node,
)

from core.nodes_base_node import FCNSocket
from core.nodes_sub_window import FCNSubWindow
from core.nodes_drag_listbox import QDMDragListbox
from core.nodes_conf import NodesStore


Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)


DEBUG = False


class FCNWindow(NodeEditorWindow):
    name_company: str
    name_product: str
    empty_icon: QIcon
    mdi_area: QMdiArea
    window_mapper: QSignalMapper
    act_close: QAction
    act_close_all: QAction
    act_tile: QAction
    act_cascade: QAction
    act_next: QAction
    act_previous: QAction
    act_separator: QAction
    act_about: QAction
    window_menu: QMenu
    help_menu: QMenu
    nodes_list_widget: QDMDragListbox
    # nodes_dock: QDockWidget

    # noinspection PyUnresolvedReferences
    def initUI(self):
        self.name_company = 'j8sr0230'
        self.name_product = 'Nodes'
        self.empty_icon = QIcon(".")

        NodesStore.refresh_nodes_list()

        if DEBUG:
            print("Registered nodes:")
            pp(NodesStore.nodes)

        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setViewMode(QMdiArea.TabbedView)
        self.mdi_area.setDocumentMode(True)
        self.mdi_area.setTabsClosable(True)
        self.mdi_area.setTabsMovable(True)
        self.setCentralWidget(self.mdi_area)
        self.mdi_area.subWindowActivated.connect(self.update_menus)
        self.window_mapper = QSignalMapper(self)
        self.window_mapper.mapped[QWidget].connect(self.set_active_sub_window)

        # self.create_nodes_dock()
        self.createActions()
        self.createMenus()
        self.create_tool_bars()
        self.createStatusBar()
        self.update_menus()
        self.readSettings()
        self.setWindowTitle("Nodes")

    def closeEvent(self, event):
        self.mdi_area.closeAllSubWindows()
        if self.mdi_area.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def createActions(self):
        super().createActions()
        self.act_close = QAction("Close", self, statusTip="Close the active window",
                                 triggered=self.mdi_area.closeActiveSubWindow)
        self.act_close_all = QAction("Close All", self, statusTip="Close all the windows",
                                     triggered=self.mdi_area.closeAllSubWindows)
        self.act_tile = QAction("Tile", self, statusTip="Tile the windows",
                                triggered=self.mdi_area.tileSubWindows)
        self.act_cascade = QAction("Cascade", self, statusTip="Cascade the windows",
                                   triggered=self.mdi_area.cascadeSubWindows)
        self.act_next = QAction("Next", self, shortcut=QKeySequence.NextChild,
                                statusTip="Move the focus to the next window",
                                triggered=self.mdi_area.activateNextSubWindow)
        self.act_previous = QAction("Previous", self, shortcut=QKeySequence.PreviousChild,
                                    statusTip="Move the focus to the previous window",
                                    triggered=self.mdi_area.activatePreviousSubWindow)
        self.act_separator = QAction(self)
        self.act_separator.setSeparator(True)
        self.act_about = QAction("About", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        active_sub_window = self.mdi_area.activeSubWindow()
        if active_sub_window:
            return active_sub_window.widget()
        return None

    def onFileNew(self):
        try:
            sub_wnd = self.create_mdi_child()
            sub_wnd.widget().fileNew()
            sub_wnd.show()
        except Exception as e:
            dumpException(e)

    def onFileOpen(self):
        file_names, file_filter = QFileDialog.getOpenFileNames(self, 'Open graph from file',
                                                               self.getFileDialogDirectory(),
                                                               self.getFileDialogFilter())
        try:
            for file_name in file_names:
                if file_name:
                    existing = self.find_mdi_child(file_name)
                    if existing:
                        self.mdi_area.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = FCNSubWindow()
                        if nodeeditor.fileLoad(file_name):
                            self.statusBar().showMessage("File %s loaded" % file_name, 5000)
                            nodeeditor.setTitle()
                            sub_wnd = self.create_mdi_child(nodeeditor)
                            sub_wnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e:
            dumpException(e)

    # noinspection PyArgumentList
    def about(self):
        QMessageBox.about(self, "Nodes by j8sr0230 et al.", "A visual scripting workbench for "
                          "<a href='https://www.freecad.org/'>FreeCAD</a> using "
                          "<a href='https://gitlab.com/pavel.krupala/pyqt-node-editor'>pyqt-node-editor</a>. For more "
                          "information visit the "
                          "<a href='https://github.com/j8sr0230/Nodes'>Nodes</a> project at github.")

    # noinspection PyUnresolvedReferences
    def createMenus(self):
        super().createMenus()
        self.window_menu = self.menuBar().addMenu("&Window")
        self.update_window_menu()
        self.window_menu.aboutToShow.connect(self.update_window_menu)
        self.menuBar().addSeparator()
        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.act_about)
        self.editMenu.aboutToShow.connect(self.update_edit_menu)

    def update_menus(self):
        # print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        has_mdi_child = (active is not None)

        self.actSave.setEnabled(has_mdi_child)
        self.actSaveAs.setEnabled(has_mdi_child)
        self.act_close.setEnabled(has_mdi_child)
        self.act_close_all.setEnabled(has_mdi_child)
        self.act_tile.setEnabled(has_mdi_child)
        self.act_cascade.setEnabled(has_mdi_child)
        self.act_next.setEnabled(has_mdi_child)
        self.act_previous.setEnabled(has_mdi_child)
        self.act_separator.setVisible(has_mdi_child)

        self.update_edit_menu()

    def update_edit_menu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            has_mdi_child = (active is not None)

            self.actPaste.setEnabled(has_mdi_child)

            self.actCut.setEnabled(has_mdi_child and active.hasSelectedItems())
            self.actCopy.setEnabled(has_mdi_child and active.hasSelectedItems())
            self.actDelete.setEnabled(has_mdi_child and active.hasSelectedItems())

            self.actUndo.setEnabled(has_mdi_child and active.canUndo())
            self.actRedo.setEnabled(has_mdi_child and active.canRedo())
        except Exception as e:
            dumpException(e)

    def update_window_menu(self):
        self.window_menu.clear()

        # toolbar_nodes = self.window_menu.addAction("Nodes Toolbar")
        # toolbar_nodes.setCheckable(True)
        # toolbar_nodes.triggered.connect(self.on_window_nodes_toolbar)
        # toolbar_nodes.setChecked(self.nodes_dock.isVisible())

        self.window_menu.addSeparator()

        self.window_menu.addAction(self.act_close)
        self.window_menu.addAction(self.act_close_all)
        self.window_menu.addSeparator()
        self.window_menu.addAction(self.act_tile)
        self.window_menu.addAction(self.act_cascade)
        self.window_menu.addSeparator()
        self.window_menu.addAction(self.act_next)
        self.window_menu.addAction(self.act_previous)
        self.window_menu.addAction(self.act_separator)

        windows = self.mdi_area.subWindowList()
        self.act_separator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.window_menu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.window_mapper.map)
            self.window_mapper.setMapping(action, window)

    # def on_window_nodes_toolbar(self):
    #     if self.nodes_dock.isVisible():
    #         self.nodes_dock.hide()
    #     else:
    #         self.nodes_dock.show()

    def create_tool_bars(self):
        pass

    # def create_nodes_dock(self):
    #     sub_lists: dict = dict()
    #     op_codes = list(NodesStore.nodes.keys())
    #     op_codes.sort()
    #     for op_code in op_codes:
    #         node = NodesStore.nodes[op_code]
    #         if node.op_category not in sub_lists.keys():
    #             sub_lists[node.op_category] = []
    #         sub_lists[node.op_category].append(op_code)
    #
    #     node_categories = list(sub_lists.keys())
    #     node_categories.sort()
    #     for node_category in node_categories:
    #         op_codes = sub_lists[node_category]
    #         self.nodes_list_widget = QDMDragListbox(op_codes, self)
    #         self.nodes_dock = QDockWidget(node_category)
    #         self.nodes_dock.setWidget(self.nodes_list_widget)
    #         self.nodes_dock.setFloating(False)
    #         self.addDockWidget(Qt.RightDockWidgetArea, self.nodes_dock)

    # def refresh_nodes_dock(self):
    #     refresh_nodes_list()
    #     self.nodes_list_widget.refresh_ui()

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def create_mdi_child(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else FCNSubWindow()
        sub_wnd = self.mdi_area.addSubWindow(nodeeditor)
        sub_wnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.update_edit_menu)
        # nodeeditor.scene.addItemsDeselectedListener(self.update_edit_menu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.update_edit_menu)
        nodeeditor.add_close_event_listener(self.on_sub_wnd_close)
        return sub_wnd

    def on_sub_wnd_close(self, widget, event):
        existing = self.find_mdi_child(widget.filename)
        self.mdi_area.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()

            # Removes all nodes from FreeCAD scene graph
            scene = existing.widget().scene
            node_list_copy = scene.nodes[:]
            while node_list_copy:
                node = node_list_copy.pop(-1)
                node.remove()
        else:
            event.ignore()

    def find_mdi_child(self, filename):
        for window in self.mdi_area.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def set_active_sub_window(self, window):
        if window:
            self.mdi_area.setActiveSubWindow(window)

    def onEditCut(self):
        """Handle Edit Cut to clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=True)
            str_data = json.dumps(data, indent=4)
            QApplication.clipboard().setText(str_data)

    def onEditCopy(self):
        """Handle Edit Copy to clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=False)
            str_data = json.dumps(data, indent=4)
            QApplication.clipboard().setText(str_data)

    def onEditPaste(self):
        """Handle Edit Paste from clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            raw_data = QApplication.clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return

            return self.getCurrentNodeEditorWidget().scene.clipboard.deserializeFromClipboard(data)
