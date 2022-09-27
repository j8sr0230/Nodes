# -*- coding: utf-8 -*-
###################################################################################
#
#  fcn_wb_commands.py
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
import FreeCADGui

import fcn_locator as locator


def QT_TRANSLATE_NOOP(scope, text):
    return text


class FCNodes_CommandShow:
    """Show FCNodes window"""

    @staticmethod
    def GetResources():
        return {'Pixmap': locator.icon('fcn_wb_icon.svg'),
                'MenuText': QT_TRANSLATE_NOOP("FCNodes_Show", "Show FCNodes window"),
                'ToolTip': QT_TRANSLATE_NOOP("FCNodes_Show", "Show FCNodes window")}

    @staticmethod
    def Activated():
        locator.getFCNodesWorkbench().window.show()

    @staticmethod
    def IsActive():
        return True


FreeCADGui.addCommand('FCNodes_Show', FCNodes_CommandShow())


class FCNodes_CommandRefresh:
    """Refresh nodes list"""

    @staticmethod
    def GetResources():
        return {'Pixmap': locator.icon('fcn_wb_icon.svg'),
                'MenuText': QT_TRANSLATE_NOOP("FCNodes_Show", "Show FCNodes window"),
                'ToolTip': QT_TRANSLATE_NOOP("FCNodes_Show", "Show FCNodes window")}

    @staticmethod
    def Activated():
        from fcn_conf import NodesStore
        NodesStore.refresh_nodes_list()

    @staticmethod
    def IsActive():
        return True


FreeCADGui.addCommand('FCNodes_Refresh', FCNodes_CommandRefresh())
