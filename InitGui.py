# -*- coding: utf-8 -*-
###################################################################################
#
#  InitGui.py
#
#  Copyright (c) 2022 Florian Foinant-Willig <ffw@2f2v.fr>
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
# TODO: Class names should be CamelCase, function names should be lowercase (if possible).

class FCNodesWorkbench(Workbench):

    import sys
    import fcn_locator as locator
    sys.path.append(locator.lib())

    import qtpy
    qtpy.API = "pyqt5"

    def QT_TRANSLATE_NOOP(scope, text):
        return text

    MenuText = "FCNodes"
    ToolTip = QT_TRANSLATE_NOOP("FCNodes", "A visual scripting environment")
    Icon = locator.icon('fcn_wb_icon.svg')

    def Initialize(self):
        # FC needs lazy import at this point
        from fcn_window import FCNWindow

        # Prepare the window
        self.window = FCNWindow()

        # command list
        import fcn_wb_commands
        self.commandList = ["FCNodes_Show"]
        self.appendToolbar("FCNodes", self.commandList)   # creates a new toolbar
        self.appendMenu("FCNodes", self.commandList)      # creates a new menu

    def ContextMenu(self, recipient):
        if recipient == "tree":
            self.appendContextMenu("FCNodes", [])   # add commands to the context menu

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(FCNodesWorkbench())
