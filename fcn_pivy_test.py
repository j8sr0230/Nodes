# -*- coding: utf-8 -*-
###################################################################################
#
#  fcn_pivy_test.py
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
"""Test module for exploring Coin3D.
"""

import FreeCADGui as Gui
import pivy.coin as coin


def make_markers():
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()

    marker = coin.SoMarkerSet()
    marker.markerIndex = coin.SoMarkerSet.CIRCLE_FILLED_9_9

    data = coin.SoCoordinate3()
    data.point.setValues(0, 2, [[0, 0, 0], [1., 1., 0.]])

    color = coin.SoMaterial()
    color.diffuseColor = (1., 1., 1.)

    myCustomNode = coin.SoSeparator()
    myCustomNode.addChild(color)
    myCustomNode.addChild(data)
    myCustomNode.addChild(marker)
    sg.addChild(myCustomNode)

    return myCustomNode


def remove_node(node):
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.removeChild(node)


# node = make_markers()
# remove_node(node)
