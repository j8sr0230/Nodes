# -*- coding: utf-8 -*-
###################################################################################
#
#  main.py
#
#  Copyright (c) 2022 Ronny Scharf-Wildenhain <ronny.scharf08@gmail.com>
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
import sys

from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Qt

import FreeCAD
import FreeCADGui

from editor.nodes_window import FCNWindow


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # Enable high dpi scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # Use high dpi icons


if __name__ == '__main__':
    if hasattr(FreeCADGui, "getMainWindow"):
        # Start app embedded in FreeCAD
        node_editor_wnd = FCNWindow()
        FreeCAD.fc_nodes_window = node_editor_wnd
        node_editor_wnd.show()
    else:
        # Start app in standalone mode
        app = QApplication(sys.argv)
        wnd = FCNWindow()
        wnd.show()
        sys.exit(app.exec_())
