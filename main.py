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
