# -*- coding: utf-8 -*-
###################################################################################
#
#  InitGui.py
#
#  Copyright 2022 Florian Foinant-Willig <ffw@2f2v.fr>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###################################################################################

class FCNodesWorkbench(Workbench):

    import fcnodes_locator as locator

    def QT_TRANSLATE_NOOP(scope, text):
        return text

    MenuText = "FCNodes"
    ToolTip = QT_TRANSLATE_NOOP("FCNodes", "A visual scripting environment")
    Icon = locator.icon('fcnodes.svg')

    def Initialize(self):
        # FC needs lazzy import at this point
        from PySide2.QtWidgets import QMainWindow
        from fcn_window import FCNWindow

        # Prepare the window
        ne_wnd = FCNWindow()
        self.container = QMainWindow(parent=FreeCADGui.getMainWindow())
        self.container.setCentralWidget(ne_wnd)

        # command list
        import fcnodes_commands
        self.commandList = ["FCNodes_Show"]
        self.appendToolbar("FCNodes", self.commandList)   # creates a new toolbar
        self.appendMenu("FCNodes", self.commandList)      # creates a new menu

    def ContextMenu(self, recipient):
        if recipient == "tree":
            self.appendContextMenu("FCNodes", [])   # add commands to the context menu

    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(FCNodesWorkbench())
