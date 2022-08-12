import os

from qtpy.QtGui import QIcon, QKeySequence
from qtpy.QtWidgets import QMdiArea, QWidget, QDockWidget, QAction, QMessageBox, QFileDialog, QMenu
from qtpy.QtCore import Qt, QSignalMapper
from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import (  # Enabling edge validators
    edge_validator_debug,
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)
import qss.nodeeditor_dark_resources  # Images for the dark skin

from fcn_sub_window import FCNSubWindow
from fcn_drag_listbox import QDMDragListbox
from nodeeditor.utils import dumpException, pp
from fcn_conf import FC_NODES

Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)

DEBUG = False


class FCNWindow(NodeEditorWindow):
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

    def initUI(self):
        self.name_company = 'j8sr0230'
        self.name_product = 'FreeCAD Nodes (fc_nodes)'

        # self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        # loadStylesheets(
        #     os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
        #     self.stylesheet_filename
        # )

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            pp(FC_NODES)

        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setViewMode(QMdiArea.TabbedView)
        self.mdi_area.setDocumentMode(True)
        self.mdi_area.setTabsClosable(True)
        self.mdi_area.setTabsMovable(True)
        self.setCentralWidget(self.mdi_area)
        self.mdi_area.subWindowActivated.connect(self.updateMenus)
        self.window_mapper = QSignalMapper(self)
        self.window_mapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.readSettings()
        self.setWindowTitle("FreeCAD Nodes (fc_nodes)")

    def closeEvent(self, event):
        self.mdi_area.closeAllSubWindows()
        if self.mdi_area.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)

    def createActions(self):
        super().createActions()
        self.act_close = QAction("Cl&ose", self, statusTip="Close the active window",
                                 triggered=self.mdi_area.closeActiveSubWindow)
        self.act_close_all = QAction("Close &All", self, statusTip="Close all the windows",
                                     triggered=self.mdi_area.closeAllSubWindows)
        self.act_tile = QAction("&Tile", self, statusTip="Tile the windows",
                                triggered=self.mdi_area.tileSubWindows)
        self.act_cascade = QAction("&Cascade", self, statusTip="Cascade the windows",
                                   triggered=self.mdi_area.cascadeSubWindows)
        self.act_next = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                                statusTip="Move the focus to the next window",
                                triggered=self.mdi_area.activateNextSubWindow)
        self.act_previous = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                    statusTip="Move the focus to the previous window",
                                    triggered=self.mdi_area.activatePreviousSubWindow)
        self.act_separator = QAction(self)
        self.act_separator.setSeparator(True)
        self.act_about = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        active_sub_window = self.mdi_area.activeSubWindow()
        if active_sub_window:
            return active_sub_window.widget()
        return None

    def onFileNew(self):
        try:
            sub_wnd = self.createMdiChild()
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
                    existing = self.findMdiChild(file_name)
                    if existing:
                        self.mdi_area.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = FCNSubWindow()
                        if nodeeditor.fileLoad(file_name):
                            self.statusBar().showMessage("File %s loaded" % file_name, 5000)
                            nodeeditor.setTitle()
                            sub_wnd = self.createMdiChild(nodeeditor)
                            sub_wnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e:
            dumpException(e)

    def about(self):
        QMessageBox.about(self, "FreeCAD Nodes by j8sr0230 et al.", "A visual scripting environment for "
                          "<a href='https://www.freecad.org/'>FreeCAD</a> using "
                          "<a href='https://gitlab.com/pavel.krupala/pyqt-node-editor'>pyqt-node-editor</a> "
                          "from Pavel Křupala. For more information visit the "
                          "<a href='https://github.com/j8sr0230/fc_nodes'>fc_nodes</a> project at github.")

    def createMenus(self):
        super().createMenus()

        self.window_menu = self.menuBar().addMenu("&Window")
        self.update_window_menu()
        self.window_menu.aboutToShow.connect(self.update_window_menu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.act_about)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.act_close.setEnabled(hasMdiChild)
        self.act_close_all.setEnabled(hasMdiChild)
        self.act_tile.setEnabled(hasMdiChild)
        self.act_cascade.setEnabled(hasMdiChild)
        self.act_next.setEnabled(hasMdiChild)
        self.act_previous.setEnabled(hasMdiChild)
        self.act_separator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e:
            dumpException(e)

    def update_window_menu(self):
        self.window_menu.clear()

        toolbar_nodes = self.window_menu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

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

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        pass

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else FCNSubWindow()
        subwnd = self.mdi_area.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.add_close_event_listener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdi_area.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, filename):
        for window in self.mdi_area.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdi_area.setActiveSubWindow(window)
